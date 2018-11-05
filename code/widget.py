import pygame
import init
from gui_config import Config
from borders import *
from fonts import *

class Widget:
    def __init__(self,
            x,y,width,height,
            border_type=Config.border_type,
            border_color=Config.border_color,
            border_fill_color=Config.border_fill_color,
            border_radius=Config.border_radius,
            border_thickness=Config.border_thickness):
        self.x=x
        self.y=y
        self.height=height
        self.width=width
        self.rect=pygame.Rect(x,y,width,height)
        
        self.border_type=border_type
        self.border_color=border_color
        self.border_fill_color=border_fill_color
        self.border_radius=border_radius
        self.border_thickness=border_thickness
        
        self.padding=border_thickness
        self.inner_rect=self.rect.inflate(-2*self.padding,-2*self.padding)
        
        self.has_focus=False
        self.needs_update=True
        
        self.borders=Borders()
        self.fonts=Fonts()

    # True if this widget contains point (x,y)
    def contains(self,x,y):
        return self.rect.collidepoint(x,y)
   
    # Does this widget accept focus?
    def accepts_focus(self):
        return True
 
    # Start receiving input
    # Returns False if this widget can't recieve focus True otherwise
    def focus(self):
        if not self.acceps_focus(): return False
        if not self.has_focus:
            self.needs_update=True
            self.has_focus=True
        return True

    # Stop receiving input
    # Returns False if this widget can't recieve focus True otherwise
    def unfocus(self):
        if not self.acceps_focus(): return False
        if self.has_focus:
            self.needs_update=True
            self.has_focus=False
        return True

    # Draw thyself
    # Return updated rectangle if there was an update, None otherwise
    def update(self,surface):
        self._draw_border(surface)
        return self.rect
    
    def _draw_border(self,surface):
        self.borders.draw(self.border_type,surface,self.rect,
            self.border_color,self.border_fill_color,
            self.border_radius,self.border_thickness)
    
    def draw(self,screen):
        self.update(screen)

    def undraw(self,screen,bckg_color=Config.bckg_color):
        screen.fill(bckg_color,self.rect)

    # Handle event, return True if handled
    # If some other widget handled it already 'handled' is True
    def handle(self, event, handled=False):
        return False

