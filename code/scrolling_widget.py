import pygame
import init
from gui_config import Config
from widget import Widget

# Scrolling widgets are just like normal except that they don't 
# do much when invisible
class ScrollingWidget(Widget):
    def __init__(self,widget,visible=True):
        self._visible=visible
        self._widget=widget

    # Implentation of decorator pattern as described here
    # https://python-patterns.guide/gang-of-four/decorator-pattern/
    # Offer every other method and property dynamically.
    def __getattr__(self, name):
        return getattr(self.__dict__['_widget'], name)

    def __setattr__(self, name, value):
        if name in ('_widget'):
            self.__dict__[name] = value
        else:
            setattr(self.__dict__['_widget'], name, value)

    def __delattr__(self, name):
        delattr(self.__dict__['_widget'], name)

    def set_visible(visible=True):
        self._visible=visible

    # Start receiving input
    # Returns False if this widget can't recieve focus True otherwise
    def focus(self):
        if not self._visible: return False
        return self._widget.focus()

    # Stop receiving input
    # Returns False if this widget can't recieve focus True otherwise
    def unfocus(self):
        if not self._visible: return False
        return self._widget.unfocus()
    
    # Draw thyself
    # Return updated rectangle if there was an update, None otherwise
    def update(self,surface):
        if not self._visible: return False
        return self._widget.update(surface)
    
    def draw(self,surface):
        if not self._visible: return False
        return self._widget.draw(surface)

    # Handle event, return True if handled
    # If some other widget handled it already 'handled' is True
    def handle(self, event, handled=False):
        if not self._visible: return False
        return self._widget.handle(event,handled)
