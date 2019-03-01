import pygame
import init
from gui_config import Config
from events import *
from widget import Widget
from borders import *

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
    
    def draw(self,screen):
        self.update(screen)
        self.needs_update=False

    # Handle event, return True if handled
    # If some other widget handled it already 'handled' is True
    def handle(self, event, handled=False):
        for c in self.chldren:
            if s.handle(event,handled): return True
        return False
