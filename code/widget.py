import pygame
import init
from gui_config import Config
from borders import *
from fonts import *

class Widget:
    def __init__(self,x,y,width,height,config=Config.default_drawing_conf):
        self.x=x
        self.y=y
        self.height=height
        self.width=width
        self.rect=pygame.Rect(x,y,width,height)
        self.config=config       
 
        padding=config.border_thickness
        self.inner_rect=self.rect.inflate(-2*padding,-2*padding)
        
        self.has_focus=False
        self.needs_update=True
        
        self.borders=Borders()
        self.fonts=Fonts()

    # True if this widget contains point (x,y)
    def contains(self,x,y):
        return self.rect.collidepoint(x,y)
   
    # This is for widgets that contain other widgets.
    # They can override this and add their sub-widgets to the focus queue.
    def focus_queue(self):
        return [self]
 
    # Start receiving input
    # Returns False if this widget can't recieve focus True otherwise
    def focus(self):
        if not self.has_focus:
            self.needs_update=True
            self.has_focus=True

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
        config=self.config
        self.borders.draw(surface,self.rect,
            config.border_radius,config.border_thickness,
            config.border_color,config.border_fill_color)
    
    def draw(self,screen):
        self.update(screen)
        self.needs_update=False

    # Handle event, return True if handled
    # If some other widget handled it already 'handled' is True
    def handle(self, event, handled=False):
        if isinstance(event,MouseDown): 
            self.__widgets.request_focus(self)
        return False

