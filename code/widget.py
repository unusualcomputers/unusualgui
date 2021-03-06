import pygame
import init
from gui_config import Config
from borders import *
from fonts import *
from events import *

class Widget(object):
    def __init__(self,x,y,width,height,config=Config.default_drawing_conf):
        self.x=x
        self.y=y
        self.height=height
        self.width=width
        self._config=config       
 
        self.has_focus=False
        self.needs_update=True
        
        self.borders=Borders()
        self.fonts=Fonts()
        from widgets import Widgets
        self.widgets=Widgets()
        Widget.init(self)

    def init_rects(self):
        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
        padding=self._config.padding
        self.inner_rect=self.rect.inflate(-2*padding,-2*padding)

    def init(self):
        self.init_rects()
        return self

    @property
    def configuration(self):
        if self._config==Config.default_drawing_conf:
            self._config=self._config.copy()
        return self._config

    @configuration.setter
    def configuration(self,c):
        self._config=c

    # Returns a widget that contains point (x,y), if any
    def contains(self,x,y):
        if self.rect.collidepoint(x,y): return self
        else: return None
   
    # This is for widgets that contain other widgets.
    # They can override this and add their sub-widgets to the focus queue.
    def focus_queue(self):
        return [self]

    # This is for widgets that contain other widgets.
    # They can override this and add their subwidgets to the message queue.
    def message_receivers(self):
        return [self]
 
    # Start receiving input
    # Returns False if this widget can't recieve focus True otherwise
    def focus(self):
        if not self.has_focus:
            self.needs_update=True
            self.has_focus=True
        return True

    # Stop receiving input
    # Returns False if this widget can't recieve focus True otherwise
    def unfocus(self):
        if self.has_focus:
            self.needs_update=True
            self.has_focus=False

    # Draw thyself
    # Return updated rectangle if there was an update, None otherwise
    def update(self,surface):
        self._draw_border(surface)
        return self.rect
    
    def _draw_border(self,surface):
        config=self._config
        self.borders.draw(surface,self.rect,
            config.border_radius,config.border_thickness,
            config.border_color,config.border_fill_color)
    
    def draw(self,surface):
        self.update(surface)
        self.needs_update=False

    # Handle event, return True if handled
    # If some other widget handled it already 'handled' is True
    def handle(self, event, handled=False):
        if isinstance(event,MouseDown): 
            self.widgets.request_focus(self)
        return False

