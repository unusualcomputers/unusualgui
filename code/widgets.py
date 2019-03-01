import init
import pygame
from widget import Widget
from none_widget import NoneWidget
from singleton import Singleton
from events import *
from messages import MessageLoop
from gui_config import Config
import logger

log=logger.get('widgets')
class Widgets:
    __metaclass__ = Singleton
    def __init__(self):
        self.__tabs={}
        self.__active=[]
        self.__focus_queue=[]
        self.__focus_idx=-1
        self.__message_loop=MessageLoop(self)
        self.__screen=None
        self.__config=None
    
    def focused(self):
        if self.__focus_idx==-1:
            return NoneWidget()
        else:
            return self.__focus_queue[self.__focus_idx]

    def run(self,screen,config=Config.default_drawing_conf):
        if self.__screen or self.__config:
            raise Exception("Widgets cannot be initialised twice")
        self.__screen=screen
        self.__config=config
        self.show()
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
        self.__active=self.__get_tab(name)
        for w in widgets:
            self.__active+=w.message_receivers()
            fq=w.focus_queue()
            for f in fq:
                if f not in self.__focus_queue:
                    self.__focus_queue.append(f)

    def __get_tab(self,name="main"):
        if name not in self.__tabs: 
            self.__tabs[name]=[]
        return self.__tabs[name]
           
    def __draw(self):
        surface=self.__screen
        surface.fill(self.__config.bckg_color)
        for w in self.__active:
            w.draw(surface)
        pygame.display.update()
    
    def update(self):
        surface=self.__screen
        update_display=False
        for w in self.__active:
            if w.needs_update:
                w.update(surface)
                update_display=True
        if update_display:
            pygame.display.update()

    def show(self,tab_name="main"):
        surface=self.__screen
        if surface is None: raise Exception("Screen not initialised")
        active=self.__get_tab(tab_name)
        if not active: 
            log.warning("No active tab")
            return
            #raise Exception("Tab %s not found" % tab_name)
        self.__active=active
        self.focused().unfocus()
        self.__focus_queue=[]
        for w in self.__active:
            fq=w.focus_queue()
            for f in fq:
                if f not in self.__focus_queue:
                    self.__focus_queue.append(f)

        self.__set_focus(0)
        self.__draw()
    
    def handle(self,event):
        if isinstance(event,KeyDown) and event.key==pygame.K_TAB:
            if self.focused().handle(event):
                return    
            elif event.mod & (pygame.KMOD_LSHIFT | pygame.KMOD_RSHIFT):
                self.focus_prev()
                return
            else:
                self.focus_next()
                return

        if isinstance(event,Message):
            if len(event.receivers)==0:
                self.broadcast(event)
            else:
                for w in event.receivers:
                    w.handle(event)
        elif isinstance(event,MouseDown):
            for w in self.__active:
                hw=w.contains(event.x,event.y)
                if hw is not None:
                    if not hw.has_focus:
                        self.request_focus(hw)
                    hw.handle(event)
                    return
        else:  
            self.focused().handle(event)
 
    def broadcast(self,message):
        for w in self.__active:
            if w!=message.sender: w.handle(message)

    def __set_focus(self,i):
        if not self.__focus_queue:
            return
        if self.__focus_idx!=-1:
            self.__focus_queue[self.__focus_idx].unfocus()
        self.__focus_idx=i
        self.__focus_queue[i].focus()

    def request_focus(self,widget):
        i=0
        sz=len(self.__focus_queue)
        if sz==0: return
        while(widget!=self.__focus_queue[i]):
            i+=1
            if i==sz: return
        self.__set_focus(i)

    def focus_next(self):
        sz=len(self.__focus_queue)
        if sz:
            i=self.__focus_idx+1
            if(i>=sz): i=0
            self.__set_focus(i)
 
    def focus_prev(self):
        sz=len(self.__focus_queue)
        if sz:
            i=self.__focus_idx-1
            if(i<0): i=sz-1
            self.__set_focus(i)
