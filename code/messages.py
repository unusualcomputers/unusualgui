import pygame
import init
from singleton import Singleton
from events import *
from widgets import Widgets
from Queue import Queue

class MessageLoop:
    __metaclass__=Singleton

    def __init__(self):
        self._queue = Queue()
        self._widgets=Widgets()

    def send(self,message):
        self._queue.put(message,True,None)

    def _translate(self,event):



    def loop(self):
        while True:
            while not self._queue.empty():
                event = self._queue.get(True,None)
                if type(event)==type(Quit):
                    self._widgets.broadcast(event)
                    return
                widgets.handle(event)
                self._queue=self._queue[1:]
            for event in pygame.event.get():            
                self.send(self._translate(event))            
