import pygame
import init
from gui_config import Config
from events import *
from widget import Widget
from widgets import Widgets
from borders import *

def _default_change_func(onOff,text):
    pass
    #print text + " is switched to " + str(onOff)

class Switch(Widget):
    def __init__(self,
            text,
            on,
            x,y,width,height,
            change_func=_default_change_func,
            config=Config.default_drawing_conf):
        
        Widget.__init__(self,x,y,width,height,config)
        self.__widgets=Widgets()
        self.__on=on
        self.text=text
        self.__change_func=change_func
        self.init()

    def init(self):
        config=self._config
        text=self.text
        font=self.fonts.get_font(config.font_name,config.font_size)
        font_sel=self.fonts.get_font(config.font_name,config.font_size,
            underline=True)
        (w,h)=font.size(text)
        inner=self.inner_rect
        
        # button height and width are golden ratio * font height
        bw=0.6180*font.get_height()
        self.__brect=pygame.Rect(
            inner.right-bw,
            (inner.height-bw)/2.0+inner.top,
            bw,
            bw)
        if w > (inner.width-self.__brect.width) or h > inner.height:
            raise Exception(u'Box too small for label "'+text+'"'+\
                u'required: '+str((w,h))+u' available: '+\
                str((inner.width-self.__brect.widtht,inner.height)))
        
        self.text_pos=(inner.x,inner.y+(inner.height-h)/2.0) 
        self.img=font.render(text,config.font_color,config.bckg_color)
        self.img_sel=font_sel.render(text,config.font_color,config.bckg_color)
        return self

    def set(self, onOff=True):
        self.__on=onOff
        self.needs_update=True

    def get(self):
        return self.__on

    # Draw thyself
    # Return updated rectangle if there was an update, None otherwise
    def update(self,surface):
        if self.has_focus:
            surface.blit(self.img_sel,self.text_pos)
        else:
            surface.blit(self.img,self.text_pos)
        
        config=self._config
        fill=None
        bord=None
        if self.__on:
            fill=config.clicked_border_fill_color
        else:
            fill=config.border_fill_color

        if self.has_focus:
            bord=config.sel_border_color
        else:    
            bord=config.clicked_border_color
        self.borders.draw(surface,self.__brect,
            config.border_radius,config.border_thickness,
            bord,fill)
        
        self.needs_update=False
        return self.rect
 
    # Handle event, return True if handled
    # If some other widget handled it already 'handled' is True
    def handle(self, event, handled=False):
        Widget.handle(self,event)
        if isinstance(event,MouseDown) or \
                (isinstance(event,KeyDown) and event.key==pygame.K_SPACE): 
            self.__widgets.request_focus(self)
            self.needs_update=True
            self.__on=not self.__on
            self.__change_func(self.__on,self.text)   
            return True
        else:
            return False


if __name__ == "__main__":

    l1=Switch(u'Label One',True,10,10,250,32)
    l2=Switch(u'button two',False,10,70,250,40)
    l3=Switch(u'Button Three',False,10,130,250,35)
    l4=Switch(u'Button Four',False,10,190,250,50)
    from widgets import Widgets
    scr = pygame.display.set_mode((300,600))
    scr.fill(Config.default_drawing_conf.bckg_color)
    widgets=Widgets();
    widgets.add((l1,l2,l3,l4))
    widgets.run(scr)      
