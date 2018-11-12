import pygame
from pygame.locals import *
import init
from singleton import Singleton
from events import *
from widgets import Widgets
from Queue import Queue
import time
import logger
from config import Config
from math import sqrt

log=logger.get('messages')

def __millis():
    return int(round(time.time() * 1000))

def __elapsed(start,tm):
    return tm-start

def __distance(start_pos,pos):
    (x1,y1)=start_pos
    (x2,y2)=pos
    return sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))

def __mouse_dist_sp(start_pos,start_time,pos,tm):
    elapsed=__elapsed(start_time,tm)
    distance=__distance(start_pos,pos)
    speed=distance/float(elapsed)
    return (distance,speed)
    
class MessageLoop:
    __metaclass__=Singleton

    def __init__(self):
        self.log=logger.get("MessageLoop")
        self._queue = Queue()
        self._widgets=Widgets()
        # keys
        self.last_key_down=None
        self.last_key_down_time=None
        self.last_key_repeat=None
        # mouse
        self.mouse_down_time=None
        self.mouse_down_pos=None
        self.dragging=False
        self.long_press=False

    def send(self,message):
        self._queue.put(message,True,None)

    def _check_timers(self):
        tm=__millis()
        if self.last_key_down_time is not None:
            if __elapsed(self.last_key_down_time,tm) > key_repeat_start:
                if self.last_key_repeat is None:
                    self.last_key_repeat=tm
                    return KeyUp(self.last_key_down.key, 
                        self.last_key_down.unicode,
                        self.last_key_down.mod)
                elif __elapsed(self.last_key_repeat) > key_repeat:
                    self.last_key_repeat=tm
                    return KeyUp(self.last_key_down.key, 
                        self.last_key_down.unicode,
                        self.last_key_down.mod)
        if not (self.dragging or self.long_click):
            e=__elapsed(self.mouse_down_time)
            if e > config.mouse_long_time:
                self.long_click=True
                return MouseLong(self.mouse_down_pos) 
        return None
 
    def _translate(self,event):
#        QUIT             none
#        ACTIVEEVENT      gain, state
#        KEYDOWN          unicode, key, mod
#        KEYUP            key, mod
#        MOUSEMOTION      pos, rel, buttons
#        MOUSEBUTTONUP    pos, button
#        MOUSEBUTTONDOWN  pos, button
#        JOYAXISMOTION    joy, axis, value
#        JOYBALLMOTION    joy, ball, rel
#        JOYHATMOTION     joy, hat, value
#        JOYBUTTONUP      joy, button
#        JOYBUTTONDOWN    joy, button
#        VIDEORESIZE      size, w, h
#        VIDEOEXPOSE      none
#        USEREVENT        code
        tm=__millis()
        if event.type == QUIT:
            return Quit()
        elif event.type == KEYDOWN:
            self.last_key_down=event
            self.last_key_down_time=tm
            self.last_key_repeat=None
            return KeyUp(self.last_key_down.key, 
                self.last_key_down.unicode,
                self.last_key_down.mod)
        elif event.type == KEYUP:
            self.last_key_down_time=None
            self.last_key_repeat=None
            if event.key != self.last_key_down.key or \
                event.mod != self.last_key_down.mod:
                self.log.error("Key up not matching last Key down event.")
            ev=KeyUp(self.last_key_down.key, 
                self.last_key_down.unicode,
                self.last_key_down.mod)
            self.last_key_down=None
            return ev
        elif event.type == MOUSEBUTTONDOWN:
            p=event.pos
            self.mouse_down_time=None
            self.mouse_down_pos=None
            self.dragging=False
            self.long_press=False
            # buttons 4-7 are scrolling
            if event.button==7:
                return Scroll(p.x,p.y,Direction.right)
            elif event.button==6:
                return Scroll(p.x,p.y,Direction.left)
            elif event.button==5:
                return Scroll(p.x,p.y,Direction.down)
            elif event.button==4:
                return Scroll(p.x,p.y,Direction.up)
            else:# all other buttons are the same
                self.mouse_down_time=tm
                self.mouse_down_pos=p
                return MouseDown(p) 
        elif event.type == MOUSEMOTION:
            bs=sum(event.buttons)
            if bs==0: return None
            p=event.pos
            if self.mouse_down_pos is None:           
                return None 
            if self.dragging:
                return Dragging(self.mouse_down_pos,p) 
            d=__distance(self.mouse_down_pos,p)
            if d > config.drag_min_distance:
                self.dragging=True
                self.long_press=False
                return Dragging(self.mouse_down_pos,p)
            return None 
        elif event.type == MOUSEBUTTONUP:
            elapsed=__elapsed(self.mouse_down_time,tm)
            start_pos=self.mouse_down_pos
            self.dragging=False
            self.long_press=False
            self.mouse_down_pos=None
            self.mouse_down_time=None
            pos=event.pos
            if elapsed < config.click_time:
                return MouseClick(start_pos)
            else:
                return MouseUp(pos,start_pos)
        return None

    def loop(self):
        while True:
            while not self._queue.empty():
                message=self._check_timers()
                if message is not None:
                    self._queue.put(message,True,None)

                event = self._queue.get(True,None)
                if type(event)==type(Quit):
                    self._widgets.broadcast(event)
                    return
                widgets.handle(event)
                self._queue=self._queue[1:]
            
            for event in pygame.event.get():            
                message=self._translate(event)
                if message is not None:
                    self._queue.put(message,True,None)


if __name__ == "__main__":
    while True:
        for event in pygame.event.get():            
            if event.type==QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                log.info('MOUSEBUTTONDOWN %s %s', event.pos,event.button)
            elif event.type == MOUSEMOTION:
                log.info('MOUSEMOTION %s %s %s', 
                    event.pos,event.rel,event.buttons)
            elif event.type == MOUSEBUTTONUP:
                log.info('MOUSEBUTTONUP %s %s', event.pos,event.button)
