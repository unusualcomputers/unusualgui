import pygame
import init
from gui_config import Config
from events import *
from widget import Widget

class Label(Widget):
    def __init__(self,
            text,
            x,y,width,height,
            config=Config.default_drawing_conf):
        
        Widget.__init__(self,x,y,width,height,config)
        self.__text=''
        self.__set_text(text)

    def __set_text(self,text):
        self.__text=text
        config=self.config
        font=self.fonts.get_font(config.font_name,config.font_size)
        (w,h)=font.size(text)
        inner=self.inner_rect
        if w > inner.width or h > inner.height:
            raise Exception(u'Box too small for label "'+text+'"'+\
                u'required: '+str((w,h))+u' available: '+\
                str((inner.width,inner.height)))
        self.pos=(inner.x+(inner.width-w)/2.0,inner.y+(inner.height-h)/2.0) 
        self.img=font.render(text,config.font_color,config.bckg_color)
        self.needs_update=True

    @property
    def text(self):
        return self.__text
    
    @text.setter
    def text(self,t):
        print 'setting ',t
        if t==self.__text: return
        else: self.__set_text(t)
        
    # Draw thyself
    # Return updated rectangle if there was an update, None otherwise
    def update(self,surface):
        surface.blit(self.img,self.pos)
        self.needs_update=False
        return self.rect
 
    # Label doesn't receive input. 
    def focus_queue(self):
        return []
 
    # Label doesn't receive input. 
    def focus(self):
        return
    
    def unfocus(self):
        return
    
    # Handle event, return True if handled
    # If some other widget handled it already 'handled' is True
    def handle(self, event, handled=False):
        return False

if __name__ == "__main__":

    l1=Label(u'Label One',10,10,150,32)
    l2=Label(u'label two',10,70,150,40)
    l3=Label(u'label Three',10,130,150,35)
    l4=Label(u'label Four',10,190,150,50)
    from widgets import Widgets
    scr = pygame.display.set_mode((300,600))
    scr.fill(Config.default_drawing_conf.bckg_color)
    widgets=Widgets();
    widgets.add((l1,l2,l3,l4))
    l4.text='LABEL FOUR'
    widgets.run(scr)      
