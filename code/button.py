import pygame
import init
from gui_config import Config
from borders import *
from events import *
from widget import Widget

# Style for a button that will make text bold when clicked 
# and underlined when in focus
class ButtonTextStyle:
    def __init__(self,button,text,font_size):
        self.button=button
        
        font=button.fonts.get_font(Config.font_name,font_size)
        (w,h)=font.size(text)
        inner=button.inner_rect
        if w > inner.width or h > inner.height:
            raise Exception(u'Box too small for button "'+text+'"'+\
                u'required: '+str((w,h))+u' available: '+\
                str((inner.width,inner.height)))
        self.pos=(inner.x+(inner.width-w)/2.0,inner.y+(inner.height-h)/2.0) 
        self.img=font.render(text,Config.font_color,Config.bckg_color)
        self.focus_img=font.render(text,Config.sel_font_color,Config.bckg_color)
        self.clicked_img=font.render(text,Config.clicked_font_color,
            Config.bckg_color)
    
    def _draw_clicked(self,surface):
        self.button._draw_border(surface)
        surface.blit(self.clicked_img,self.pos)
        
    def _draw_not_clicked(self,surface):
        self.button._draw_border(surface)
        if self.button.has_focus:
            surface.blit(self.focus_img,self.pos)
        else:
            surface.blit(self.img,self.pos)
        

# Behaviour for simple button
class ButtonClick:
    def __init__(self,button):
        self.button=button

    def on_mouse_down(self):
        self.button._set_clicked(True)

    def on_mouse_up(self):
        self.button._set_clicked(False)

# Behaviour for On/Off button
class ButtonOnOff:
    def __init__(self,button):
        self.button=button

    def on_mouse_down(self):
        self._set_clicked(not self.is_clicked)

    def on_mouse_up(self):
        pass

# Behaviour for linked buttons
class ButtonLinked:
    def __init__(self,button):
        self.button=button
        self.other_buttons=[]

    def add_other(self,buttons):
        for button in buttons:
            if button != self.button:
                self.other_buttons.append(button)

    def on_mouse_down(self):
        self.button._set_clicked(True)
        for b in self.other_buttons:
            b._set_clicked(False)


    def on_mouse_up(self):
        pass

class Button(Widget):
    def __init__(self,
            text,
            x,y,width,height,
            clicked_func,
            unclicked_func=None,
            style=ButtonTextStyle,
            behaviour=ButtonClick,
            font_size=Config.font_size,
            border_type=Config.border_type,
            border_color=Config.border_color,
            border_fill_color=Config.border_fill_color,
            border_radius=Config.border_radius,
            border_thickness=Config.border_thickness):
        
        Widget.__init__(self,x,y,width,height,
            border_type,border_color,border_fill_color,
            border_radius,border_thickness)
        
        self.behaviour=behaviour(self)
        self.style=style(self,text,font_size)
        self.text=text
        self.is_clicked=False
        self.clicked_func=clicked_func
        self.unclicked_func=unclicked_func

    def _set_clicked(self,clicked):
        if clicked!=self.is_clicked:
            self.is_clicked=clicked
            self.needs_update=True
            if clicked and self.clicked_func:
                self.clicked_func(self.text)
            elif self.unclicked_func:
                self.unclicked_func(self.text)

    
    def _draw_border(self,surface):
        if self.is_clicked:
            self.borders.draw(self.border_type,surface,self.rect,
                Config.clicked_border_color,self.border_fill_color,
                self.border_radius,self.border_thickness)
        elif self.has_focus:
            self.borders.draw(self.border_type,surface,self.rect,
                Config.sel_border_color,self.border_fill_color,
                self.border_radius,self.border_thickness)
        else:
            self.borders.draw(self.border_type,surface,self.rect,
                Config.border_color,self.border_fill_color,
                self.border_radius,self.border_thickness)
    
    # Draw thyself
    # Return updated rectangle if there was an update, None otherwise
    def update(self,surface):
        if self.needs_update:
            if self.is_clicked:
                self.style._draw_clicked(surface)
            else:
                self.style._draw_not_clicked(surface)
            return self.rect
        else:
            return None
    

    # Handle event, return True if handled
    # If some other widget handled it already 'handled' is True
    def handle(self, event, handled=False):
        if isinstance(event,MouseDown) or \
                (isinstance(event,KeyDown) and event.key==pygame.K_SPACE): 
            self.behaviour.on_mouse_down()
            return True
        elif isinstance(event,MouseUp) or \
                (isinstance(event,KeyUp) and event.key==pygame.K_SPACE):
            
            self.behaviour.on_mouse_up()
            return True
        else:
            return False

if __name__ == "__main__":
    def clicked_test(text): print text + u' clicked'
    def unclicked_test(text): print text + u' unclicked'

    b1=Button(u'Button One',10,10,150,32,clicked_test,unclicked_test,
        border_type=BorderType.NONE)
    b2=Button(u'button two',10,70,150,40,clicked_test,unclicked_test,
        border_type=BorderType.ROUNDED, border_radius=10)
    b3=Button(u'Button Three',10,130,150,35,clicked_test,unclicked_test,
        border_type=BorderType.SIMPLE,border_thickness=2)
    b4=Button(u'Button Four',10,190,150,50,clicked_test,unclicked_test,
        border_type=BorderType.OPEN,border_thickness=1)
            #text,
            #x,y,height,width,
            #clicked_func,
            #unclicked_func=None,
            #style=ButtonTextStyle,
            #behaviour=ButtonClick,
            #font_size=Config.font_size,
            #border_type=Config.border_type,
            #border_color=Config.border_color,
            #border_fill_color=Config.border_fill_color,
            #border_radius=Config.border_radius,
            #border_thickness=Config.border_thickness):
    from widgets import Widgets
    scr = pygame.display.set_mode((300,600))
    scr.fill(Config.bckg_color)
    widgets=Widgets(scr);
    widgets.add((b1,b2,b3,b4))
    widgets.run()      
    #b1.draw(scr)
    #b2.draw(scr)
    #b3.draw(scr)
    #b4.draw(scr)
    #pygame.display.update()
    #while pygame.event.wait().type != pg.QUIT: pass
