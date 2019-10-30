import pygame
from pygame.locals import *
import init
from singleton import Singleton
from events import *
from collections import deque
import time
import logger
from gui_config import Config
from math import sqrt

log=logger.get('messages')

def _millis():
    return int(round(time.time() * 1000))

def _elapsed(start,tm):
    return tm-start

def _distance(start_pos,pos):
    (x1,y1)=start_pos
    (x2,y2)=pos
    return sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))

def _mouse_dist_sp(start_pos,start_time,pos,tm):
    elapsed=_elapsed(start_time,tm)
    distance=_distance(start_pos,pos)
    speed=distance/float(elapsed)
    return (distance,speed)
    
class MessageLoop:
    #__metaclass__=Singleton

    def __init__(self,widgets):
        self.__queue = deque()
        self.__widgets=widgets
        self.__clock = pygame.time.Clock()
        # mouse
        self.mouse_down_time=None
        self.mouse_down_pos=None
        self.dragging=False
        self.long_press=False

    def send(self,message):
        self.__queue.append(message)

    def __check_timers(self):
        if self.mouse_down_time is not None:
            if not (self.dragging or self.long_press):
                tm=_millis()
                e=_elapsed(self.mouse_down_time,tm)
                if e > Config.mouse_long_time:
                    self.long_press=True
                    message=MouseLong(self.mouse_down_pos) 
                    self.__queue.append(message)
 
    def __translate(self,event):
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
        if event.type == QUIT:
            return Quit()
        elif event.type == KEYDOWN:
            return KeyDown(event.key, 
                event.unicode,
                event.mod)
        elif event.type == KEYUP:
            return KeyUp(event.key, 
                event.mod)
        elif event.type == MOUSEBUTTONDOWN:
            p=event.pos
            self.mouse_down_time=None
            self.mouse_down_pos=None
            self.dragging=False
            self.long_press=False
            # buttons 4-7 are scrolling
            if event.button==7:
                return Scroll(p,Direction.right)
            elif event.button==6:
                return Scroll(p,Direction.left)
            elif event.button==5:
                return Scroll(p,Direction.down)
            elif event.button==4:
                return Scroll(p,Direction.up)
            else:# all other buttons are the same
                self.mouse_down_time=_millis()
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
            d=_distance(self.mouse_down_pos,p)
            if d > Config.drag_min_distance:
                self.dragging=True
                self.long_press=False
                return Dragging(self.mouse_down_pos,p)
            return None 
        elif event.type == MOUSEBUTTONUP:
            if self.mouse_down_time is None: return None
            elapsed=_elapsed(self.mouse_down_time,_millis())
            start_pos=self.mouse_down_pos
            self.dragging=False
            self.long_press=False
            self.mouse_down_pos=None
            self.mouse_down_time=None
            pos=event.pos
            return MouseUp(pos,start_pos,elapsed)
        return None

    def loop(self):
        widgets=self.__widgets
        queue=self.__queue
        check_timers=self.__check_timers
        translate=self.__translate
        clock=self.__clock
        fps=self.__fps
        while True:
            empty=len(queue)==0
            if not empty:
                while not len(queue)==0:
                    event = queue.popleft()
                    if isinstance(event,Quit):
                        widgets.broadcast(event)
                        return
                    widgets.handle(event)
                widgets.update()
            
            for event in pygame.event.get():            
                message=translate(event)
                if message is not None:
                    queue.append(message)

            check_timers()
            clock.tick(fps)

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
