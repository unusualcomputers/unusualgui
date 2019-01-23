import pygame
import init
from singleton import Singleton
from widget import Widget

class NoneWidget(Widget):
    def __init__(self):
        Widget.__init__(self,0,0,0,0)
        self.needs_update=False
    # Does this widget accept focus?
    def accepts_focus(self):
        return False
    # Draw thyself
    # Return updated rectangle if there was an update, None otherwise
    def update(self,surface):
        return self.rect
    
    def draw(self,screen):
        pass

    def undraw(self,screen):
        pass

    # Handle event, return True if handled
    # If some other widget handled it already 'handled' is True
    def handle(self, event, handled=False):
        return False

 
