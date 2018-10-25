import pygame
import gui_config as config
from borders import *

class Widget:
    def __init__(self,
            x,y,height,width
            border_type=config.border_type,
            border_color=config.border_color,
            border_fill_color=config.border_fill_color,
            border_radius=config.border_radius,
            border_thickness=config.border_thickness):
        self.x=x
        self.y=y
        self.height=height
        self.width=width
        self.rect=pygame.Rect(x,y,height,width)
        
        self.border_type=border_type
        self.border_color=border_color
        self.border_fill_color=border_fill_color
        self.border_radius=border_radius
        self.border_thickness=border_thickness
        
        self.padding=border_radius+border_thickness
        self.inner_rect=self.rect.inflate(-self.padding,-self.padding)
        self.has_focus=False

    # True if this widget contains point (x,y)
    def contains(self,x,y):
        return self.rect.collidepoint(x,y)
    
    # Start receiving input
    def focus(self):
        self.has_focus=True

    # Stop receiving input
    def unfocus(self):
        self.has_focus=False

    # Draw thyself
    # Return updated rectangle if there was an update, None otherwise
    def update(self,screen):
        self._draw_border()
        return self.rect
    
    def _draw_border(self,screen):
        borders.draw(self.border_type,surface,self.rect,
            self.border_color,self.border_fill_color,
            self.border_radius,self.border_thickness)
    
    def draw(self,screen):
        self.update(screen)

    def undraw(self,screen,bckg_color=config.bckg_color):
        screen.fill(bckg_color,self.rect)

    # Handle event, return True if handled
    # If some other widget handled it already 'handled' is True
    def handle(self, event, handled=False):
        return False

