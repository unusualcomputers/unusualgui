import init
import pygame
from widget import Widget
from singleton import Singleton
from events import *
from messages import MessageLoop


class Widgets:
    #__metaclass__ = Singleton
    def __init__(self,screen):
        self.__widgets={}
        self.__active=[]
        self.__focus_queue=[]
        self.__focus=None
        self.__message_loop=MessageLoop(self)
        self.__screen=screen

    def run(self):
        self.show()
        self.draw()
        self.__message_loop.loop()

    def add(self,widgets,name="main"):
        t=type(widgets)
        if t==type(()):
            self.__add_widgets(list(widgets),name)
        elif t==type([]):
            self.__add_widgets(widgets,name)
        elif t==type({}):
            self.__add_widgets(widgets.values,name)
        else:
            self.__add_widgets([widgets],name)

    def __add_widgets(self, widgets, name="main"):
        l=len(widgets)
        if l==0: return
        self.__active=self.get(name)
        self.__active+=widgets
        for w in widgets:
            self.__focus_queue+=w.focus_queue()
        

    def get(self,name="main"):
        if name not in self.__widgets: 
            self.__widgets[name]=[]
        return self.__widgets[name]
           
    def draw(self):
        surface=self.__screen
        for w in self.__active:
            w.draw(surface)
        pygame.display.update()
 
    def update(self):
        surface=self.__screen
        for w in self.__active:
            if w.needs_update: 
                w.update(surface)
                w.needs_update=False
        pygame.display.update()

    def show(self,name="main"):
        surface=self.__screen
        active=self.get(name)
        if self.__active == active: return
        for w in self.__focus_queue:
            w.unfocus
        for w in self.__active:
            w.undraw(surface)
        
        self.__active=active
        self.__focus_queue=[]
        for w in self.__active:
            self.__focus_queue+=widgets.focus_queue()

        i=0
        sz= len(self.__focus_queue)
        while i<sz and self.__set_focus(i) is not None:
            i+=1
        self.draw()
     
    def handle(self,event):
        print 'received message ', event
        if isinstance(event,MouseDown):
            self.set_focusPos(event.pos[0],event.pos[1])
        if isinstance(event,KeyDown) and event.key==pygame.K_TAB:
            if self.focused() is not None:
                self.focused().needs_update=True
            if event.mod==pygame.KMOD_SHIFT:
                self.focus_prev()
            else:
                self.focus_next()
            self.focused().needs_update=True
        if isinstance(event,Message):
            if len(event.receivers)==0:
                self.broadcast(event)
            else:
                for w in event.receivers:
                    w.handle(event)
        elif self.focused() is None:
            return False
        else:  
            return self.focused().handle(event)
 
    def broadcast(self,message):
        for w in self.__active:
            if w != message.sender: w.handle(message)

    def __set_focus(self,i,pos=None):
        if i==self.__focus:
            return self.focused()
        if i>len(self.__focus_queue):
            raise Exception("Focus index out of range")
        if not self.__focus_queue[i].accepts_focus():
            return None
        f=self.focused()
        if f is not None:
            f.unfocus()
        self.__focus=i
        self.focused().focus(pos)
        return self.focused()

    def focused(self):
        if self.__focus is None: return None
        return self.__focus_queue[self.__focus]
 
    def focus_next(self):
        sz=len(self.__focus_queue)
        if sz==0: return None
        elif sz==1: return self.__set_focus(0)
        if self.__focus is None:
            i=0
        else:
            i=self.__focus+1
        while(i<sz and self.__set_focus(i) is None):
            i+=1
        if i!=sz: return self.focused()
        i=0        
        while(i<self.__focus and self.__set_focus(i) is None):
            i+=1
        return self.focused()
 
    def focus_prev(self):
        sz=len(self.__focus_queue)
        if sz==0: return None
        elif sz==1: return self.__set_focus(0)
        i=self.__focus-1
        while(i>=0 and self.__set_focus(i) is None):
            i-=1
        if i>0: return self.__focused()
        i=sz-1        
        while(i>self.__focus and self.__set_focus(i) is None):
            i-=1
        return self.focused()

    def find(self,x,y):
        for i in range(len(self.__active)):
            w=self.__active[i]
            if w.contains(x,y): return w
        return None
                    
    def set_focusPos(self,x,y):
        sz=len(self.__focus_queue)
        for i in range(sz):
            w=self.__focus_queue[i]
            if w.contains(x,y):
                return self.__set_focus(i,(x,y))
        return None
                    
    def set_focus(self,widget):
        if widget==self.focused(): return widget
        for i in range(len(self.__focus_queue)):
            w=self.__focus_queue[i]
            if w==widget:
                return self.__set_focus(i)
        return None
