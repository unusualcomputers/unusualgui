import pygame
import init
from gui_config import Config
from borders import *
from events import *
from widget import Widget
from button_styles import ButtonStyle

# Behaviour for simple button
class Click:
    def __init__(self,button):
        self.button=button

    def on_mouse_down(self):
        self.button._set_clicked(True)

    def on_mouse_up(self):
        self.button._set_clicked(False)

# Behaviour for On/Off button
class OnOff:
    def __init__(self,button):
        self.button=button

    def on_mouse_down(self):
        self.button._set_clicked(not self.button.is_clicked)

    def on_mouse_up(self):
        pass

class Button(Widget):
    def __init__(self,
            text,
            x,y,width,height,
            clicked_func,
            unclicked_func=None,
            style=ButtonStyle.Default,
            behaviour=Click,
            config=Config.default_drawing_conf):
        
        Widget.__init__(self,x,y,width,height,config)
        
        self.behaviour=behaviour(self)
        self.style=style(self,text)
        self.text=text
        self.is_clicked=False
        self.clicked_func=clicked_func
        self.unclicked_func=unclicked_func
        self.init()
    
    def init(self):
        Widget.init(self)
        self.style.init(self.text)
        return self

    def _set_clicked(self,clicked):
        if clicked!=self.is_clicked:
            self.is_clicked=clicked
            self.needs_update=True
            if clicked and self.clicked_func:
                self.clicked_func(self.text)
            elif self.unclicked_func:
                self.unclicked_func(self.text)
    
    # Draw thyself
    # Return updated rectangle if there was an update, None otherwise
    def update(self,surface):
        if self.is_clicked:
            self.style._draw_clicked(surface)
        else:
            self.style._draw_not_clicked(surface)
        self.needs_update=False
        return self.rect
    

    # Handle event, return True if handled
    # If some other widget handled it already 'handled' is True
    def handle(self, event, handled=False):
        Widget.handle(self,event)
        if isinstance(event,MouseDown) or \
                (isinstance(event,KeyDown) and event.key==pygame.K_SPACE): 
            self.widgets.request_focus(self)
            self.needs_update=True
            self.behaviour.on_mouse_down()
            return True
        elif isinstance(event,MouseUp) or \
                (isinstance(event,KeyUp) and event.key==pygame.K_SPACE):
            self.behaviour.on_mouse_up()
            return True
        else:
            return False

class OnOffButton(Button):
    def __init__(self,
            text,
            x,y,width,height,
            clicked_func,
            unclicked_func=None,
            style=ButtonStyle.Default,
            config=Config.default_drawing_conf):
        Button.__init__(self,text,x,y,width,height,
            clicked_func, unclicked_func,style,
            OnOff,
            config)

if __name__ == "__main__":
    def clicked_test(text): print text + u' clicked'
    def unclicked_test(text): print text + u' unclicked'

    b1=Button(u'Button One',10,10,150,40,clicked_test,unclicked_test)
    c2=Config.default_drawing_conf.with_rect_border()
    b2=Button(u'button two',10,70,150,40,clicked_test,unclicked_test,
        style=ButtonStyle.Borderless)
    b2.configuration = b2.configuration.with_rect_border()
    b2.init()
    b3=OnOffButton(u'Button Three',10,130,150,45,clicked_test,unclicked_test)
    b4=Button(u'Button Four',10,190,150,50,clicked_test,unclicked_test,
        style=ButtonStyle.Text)
    from widgets import Widgets
    scr = pygame.display.set_mode((300,600))
    scr.fill(Config.default_drawing_conf.bckg_color)
    widgets=Widgets();
    widgets.add((b1,b2,b3,b4))
    widgets.run(scr)      
