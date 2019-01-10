import pygame
import init
from gui_config import Config
from borders import *
from events import *
from widget import Widget

# Default style for a button 
class ButtonDefaultStyle:
    def __init__(self,button,text):
        self.button=button
        self.borders=button.borders
        self.config=button.config
 
        font=button.fonts.get_font(self.config.font_name,self.config.font_size)
        (w,h)=font.size(text)
        inner=button.inner_rect
        if w > inner.width or h > inner.height:
            raise Exception(u'Box too small for button "'+text+'"'+\
                u'required: '+str((w,h))+u' available: '+\
                str((inner.width,inner.height)))
        self.pos=(inner.x+(inner.width-w)/2.0,inner.y+(inner.height-h)/2.0) 
        self.img=font.render(text,self.config.font_color,self.config.bckg_color)
        self.focus_img=font.render(text,
            self.config.sel_font_color,self.config.sel_border_fill_color)
        self.clicked_img=font.render(text,self.config.clicked_font_color,
            self.config.clicked_border_fill_color)
    
    def _draw_clicked(self,surface):
        self._draw_border(surface)
        surface.blit(self.clicked_img,self.pos)
        
    def _draw_not_clicked(self,surface):
        self._draw_border(surface)
        if self.button.has_focus:
            surface.blit(self.focus_img,self.pos)
        else:
            surface.blit(self.img,self.pos)
        
    def _draw_border(self,surface):
        rect=self.button.rect
        config=self.config
        if self.button.is_clicked:
            self.borders.draw(surface,rect,
                config.border_radius,config.border_thickness,
                config.clicked_border_color,
                config.clicked_border_fill_color)
        elif self.button.has_focus:
            self.borders.draw(surface,rect,
                config.border_radius,config.border_thickness,
                config.sel_border_color,
                config.sel_border_fill_color)
        else:
            self.borders.draw(surface,rect,
                config.border_radius,config.border_thickness,
                config.border_color,
                config.border_fill_color)

# Button style with no borders 
class ButtonTextStyle:
    def __init__(self,button,text):
        self.button=button
        self.borders=button.borders
        config=button.config
 
        font=button.fonts.get_font(config.font_name,config.font_size)
        (w,h)=font.size(text)
        inner=button.inner_rect
        if w > inner.width or h > inner.height:
            raise Exception(u'Box too small for button "'+text+'"'+\
                u'required: '+str((w,h))+u' available: '+\
                str((inner.width,inner.height)))
        self.pos=(inner.x+(inner.width-w)/2.0,inner.y+(inner.height-h)/2.0) 
        self.img=font.render(text,config.font_color,config.bckg_color)

        font_sel=button.fonts.get_font(config.font_name,config.font_size,
            underline=True)
        self.focus_img=font_sel.render(text,
            config.sel_font_color,config.bckg_color)
        self.clicked_img=font.render(text,config.clicked_font_color,
            config.bckg_color)
        self.clicked_sel_img=font_sel.render(text,config.clicked_font_color,
            config.bckg_color)
    
    def _draw_clicked(self,surface):
        if self.button.has_focus:
            surface.blit(self.clicked_sel_img,self.pos)
        else:
            surface.blit(self.clicked_img,self.pos)
    
    def _draw_not_clicked(self,surface):
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
        self.button._set_clicked(not self.button.is_clicked)

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
            style=ButtonDefaultStyle,
            behaviour=ButtonClick,
            config=Config.default_drawing_conf):
        
        Widget.__init__(self,x,y,width,height,config)
        
        self.behaviour=behaviour(self)
        self.style=style(self,text)
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

    b1=Button(u'Button One',10,10,150,32,clicked_test,unclicked_test)
    c2=Config.default_drawing_conf.with_rect_border()
    b2=Button(u'button two',10,70,150,40,clicked_test,unclicked_test,config=c2)
    b3=Button(u'Button Three',10,130,150,35,clicked_test,unclicked_test,
        behaviour=ButtonOnOff)
    b4=Button(u'Button Four',10,190,150,50,clicked_test,unclicked_test,
        style=ButtonTextStyle)
    from widgets import Widgets
    scr = pygame.display.set_mode((300,600))
    scr.fill(Config.default_drawing_conf.bckg_color)
    widgets=Widgets(scr);
    widgets.add((b1,b2,b3,b4))
    widgets.run()      
    #b1.draw(scr)
    #b2.draw(scr)
    #b3.draw(scr)
    #b4.draw(scr)
    #pygame.display.update()
    #while pygame.event.wait().type != pg.QUIT: pass
