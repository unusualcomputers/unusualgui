import pygame
import gui_config as config
from borders import *
from events import *
from widget import Widget

# Style for a button that will change background color when clicked
class ButtonFilledStyle:
    def __init__(self,button,text,font_size):
        self.button=button
        font=button.fonts.get_font(config.font_name,font_size)
        (w,h)=font.size(text)
        inner=button.inner_rect
        if w > inner.width or h > inner.height:
            raise Exception(u'Box too small for button "'+text+'"'+\
                u'required: '+str((w,h))+u' available: '+\
                str((inner.width,inner.height)))
            raise Exception(u'Box too small for button "'+text+'"'+\
                u'required: '+(w,h)+u'available: '+(inner.width,inner.height))
        self.pos=(inner.x+(inner.width-w)/2.0,inner.y+(inner.height-h)/2.0) 
        self.img=font.render(text,config.font_color,config.bckg_color)
        
    def _draw_clicked(self,surface):
        b=self.button
        b.borders.draw(b.border_type,surface,b.rect,
            b.border_color,b.border_fill_color,
            b.border_radius,b.border_thickness)
        surface.blit(self.img,self.pos)
        
    def _draw_not_clicked(self,surface):
        b=self.button
        if b.has_focus:
            b.borders.draw(b.border_type,surface,b.rect,
                config.sel_color,None,
                b.border_radius,b.border_thickness)
        else: 
            b.borders.draw(b.border_type,surface,b.rect,
                b.border_color,None,
                b.border_radius,b.border_thickness)
        surface.blit(self.img,self.pos)

# Style for a button that will make text bold and underlined when clicked
class ButtonTextStyle:
    def __init__(self,button,text,font_size):
        self.button=button
        
        font=button.fonts.get_font(config.font_name,font_size)
        (w,h)=font.size(text)
        inner=button.inner_rect
        if w > inner.width or h > inner.height:
            raise Exception(u'Box too small for button "'+text+'"'+\
                u'required: '+str((w,h))+u' available: '+\
                str((inner.width,inner.height)))
        self.pos=(inner.x+(inner.width-w)/2.0,inner.y+(inner.height-h)/2.0) 
        self.img=font.render(text,config.font_color,config.bckg_color)
        
        font=button.fonts.get_font(config.font_name,font_size,bold=True)
        font.set_underline(True)
        (w,h)=font.size(text)
        if w > inner.width or h > inner.height:
            raise Exception(u'Box too small for button "'+text+'"'+\
                u'required: '+str((w,h))+u' available: '+\
                str((inner.width,inner.height)))
        self.clicked_pos=\
            (inner.x+(inner.width-w)/2.0,inner.y+(inner.height-h)/2.0) 
        self.clicked_img=font.render(text,config.font_color,config.bckg_color)
    
        font=button.fonts.get_font(config.font_name,font_size,italic=True)
        (w,h)=font.size(text)
        if w > inner.width or h > inner.height:
            raise Exception(u'Box too small for button "'+text+'"'+\
                u'required: '+str((w,h))+u' available: '+\
                str((inner.width,inner.height)))
        self.focus_pos=\
            (inner.x+(inner.width-w)/2.0,inner.y+(inner.height-h)/2.0) 
        self.focus_img=font.render(text,config.font_color,config.bckg_color)
    
    def _draw_clicked(self,surface):
        b=self.button
        b._draw_border(surface)
        surface.blit(self.clcked_img,self.clicked_pos)
        
    def _draw_not_clicked(self,surface):
        b=self.button
        b._draw_border(surface)
        if b.has_focus:
            surface.blit(self.focus_img,self.focus_pos)
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
        pass

    def on_mouse_up(self):
        self._set_clicked(not self.is_clicked)


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
        pass

    def on_mouse_up(self):
        self.button._set_clicked(True)
        for b in self.other_buttons:
            b._set_clicked(False)

class Button(Widget):
    def __init__(self,
            text,
            x,y,width,height,
            clicked_func,
            unclicked_func=None,
            style=ButtonTextStyle,
            behaviour=ButtonClick,
            font_size=config.font_size,
            border_type=config.border_type,
            border_color=config.border_color,
            border_fill_color=config.border_fill_color,
            border_radius=config.border_radius,
            border_thickness=config.border_thickness):
        
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
        t=type(event)
        if (t is MouseDown) or (t is KeyDown and t.unicode==u' '): 
            self.behaviour.on_mouse_down()
            return True
        elif (t is MouseClick) or (t is MouseLongEnd) or \
                (t is KeyUp and t.unicode==u' '):
            self.behaviour.on_mouse_up()
            return True
        else:
            return False

if __name__ == "__main__":
    pygame.init()
    scr = pygame.display.set_mode((300,600))
    scr.fill(config.bckg_color)
    def clicked_test(text): print text + u' clicked'
    def unclicked_test(text): print text + u' unclicked'

    b1=Button(u'Button One',10,10,150,32,clicked_test,unclicked_test,
        border_type=BorderType.NONE)
    b2=Button(u'Button Two',10,70,150,40,clicked_test,unclicked_test,
        style=ButtonFilledStyle,
        border_type=BorderType.ROUNDED, border_radius=10)
    b3=Button(u'Button Three',10,130,150,35,clicked_test,unclicked_test,
        style=ButtonFilledStyle,
        border_type=BorderType.SIMPLE,border_thickness=2)
    b4=Button(u'Button Four',10,190,150,50,clicked_test,unclicked_test,
        style=ButtonFilledStyle,
        border_type=BorderType.OPEN,border_thickness=1)
            #text,
            #x,y,height,width,
            #clicked_func,
            #unclicked_func=None,
            #style=ButtonTextStyle,
            #behaviour=ButtonClick,
            #font_size=config.font_size,
            #border_type=config.border_type,
            #border_color=config.border_color,
            #border_fill_color=config.border_fill_color,
            #border_radius=config.border_radius,
            #border_thickness=config.border_thickness):
    b1.draw(scr)
    b2.draw(scr)
    b3.draw(scr)
    b4.draw(scr)
    pygame.display.update()
    while pygame.event.wait().type != pg.QUIT: pass
