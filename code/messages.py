import pygame
from pygame.locals import *
import init
from singleton import Singleton
from events import *
from widgets import Widgets
from Queue import Queue
import time
import logger

def __millis():
    return int(round(time.time() * 1000))

def __elapsed(start):
    return (int(round(time.time() * 1000))-start)

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
            

    def send(self,message):
        self._queue.put(message,True,None)

    def _check_timers(self):
        if self.last_key_down_time is not None:
            if __elapsed(self.last_key_down_time) > key_repeat_start:
                if self.last_key_repeat is None:
                    self.last_key_repeat=__millis()
                    return KeyUp(self.last_key_down.key, 
                        self.last_key_down.unicode,
                        self.last_key_down.mod)
                elif __elapsed(self.last_key_repeat) > key_repeat:
                    self.last_key_repeat=__millis()
                    return KeyUp(self.last_key_down.key, 
                        self.last_key_down.unicode,
                        self.last_key_down.mod)

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
        if event.type == QUIT:
            return Quit()
        elif event.type == KEYDOWN:
            self.last_key_down=event
            self.last_key_down_time=__millis()
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
            # handle
        elif event.type == MOUSEMOTION:
            # handle
        elif event.type == MOUSEBUTTONUP:
            # handle
        return None

    def loop(self):
        while True:
            while not self._queue.empty():
                event = self._queue.get(True,None)
                if type(event)==type(Quit):
                    self._widgets.broadcast(event)
                    return
                widgets.handle(event)
                self._queue=self._queue[1:]
            
            message=self._check_timers()
            if message is not None:
                    self._queue.put(message,True,None)

            for event in pygame.event.get():            
                message=self._translate(event)
                if message is not None:
                    self._queue.put(message,True,None)
