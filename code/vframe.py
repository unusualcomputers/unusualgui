import pygame
import init
from gui_config import Config
from widget import Widget
from borders import *
from graphics import Graphics

class ScrollButton(object):
    def __init__(self,config,rect,up=True):
        self.config=config
        self.rect=rect
        
        self.height=2*(config.padding+config.trig_button_radius)
        self.x=(rect.width-2*config.trig_button_radius)/2
        if up:
            self.arrow_func=Graphics.up
            self.y=rect.top+config.padding
        else:
            self.arrow_func=Graphics.down
            self.y=rect.bottom-self.height+config.padding

    def draw_arrow(self,surface,filled=False):
        arrow=arrow_func(self.config,surface,filled)
        suface.blit(arrow,(self.x,self.y))    

class VFrame(Widget):
    def __init__(self,children,x,y,width,height,with_scrolling=False,
            config=Config.default_drawing_conf):
        Widget.__init__(self,x,y,width,height,config)
        self.children=children        
        self.__with_scrolling=with_scrolling
        self.init()

    def init(self):
        x=self.inner_rect.left
        width=self.inner_rect.width
        y=self.inner_rect.top
        if not self.__with_scrolling:
            h=self.inner_rect.height/float(len(self.children))
            i=0
            for c in self.children:
                c.x=x
                c.y=y+i*h
                c.width=width
                c.height=h
                c.init()
                i+=1
        if self.__with_scrolling:
            self.children=[ScrollingWidget(c) for c in self.children]
            if len(self.children)>0: self.first_visible=0
            else:self.first_visible=-1
            self.__up=ScrollButton(self.config,self.rect,True)
            self.__down=ScrollButton(self.config.self.rect,False)
         
        return self

    # Returns a widget that contains point (x,y), if any
    def contains(self,x,y):
        for c in self.children:
            if c.contains(x,y): return c
        return None
   
    # This is for widgets that contain other widgets.
    # They can override this and add their sub-widgets to the focus queue.
    def focus_queue(self):
        return [f for c in self.children for f in c.focus_queue()]     

    # This is for widgets that contain other widgets.
    # They can override this and add their subwidgets to the message queue.
    def message_receivers(self):
        return [self]+[f for c in self.children for f in c.message_receivers()]     
    # Start receiving input
    # Returns False if this widget can't recieve focus True otherwise
    def focus(self):
        return False

    # Stop receiving input
    # Returns False if this widget can't recieve focus True otherwise
    def unfocus(self):
        return False

    # Draw thyself
    # Return updated rectangle if there was an update, None otherwise
    def update(self,surface):
        self._draw_border(surface)
        return self.rect
    
    def _draw_border(self,surface):
        config=self._config
        self.borders.draw(surface,self.rect,
            config.border_radius,config.border_thickness,
            config.border_color,config.bckg_color)
    
    def draw(self,surface):
        self.update(surface)
        self.needs_update=False

    # Handle event, return True if handled
    # If some other widget handled it already 'handled' is True
    def handle(self, event, handled=False):
        for c in self.children:
            if s.handle(event,handled): return True
        return False
