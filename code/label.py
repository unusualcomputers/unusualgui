import pygame
import gui_config as config
from borders import *
from widget import Widget
from fonts import *

class Label(Widget):
    def __init__(self,
            text,
            x,y,
            width=None,
            height=None,
            font_size=config.font_size):
        
        fonts=Fonts()
        font=fonts.get_font(config.font_name,font_size)
        (w,h)=font.size(text)
        if width is None:
            width=w+2*config.border_thickness
        if height is None:
            height=h+2*config.border_thickness
    
        Widget.__init__(self,x,y,width,height,
            BorderType.NONE,border_radius=0)
        inner=self.inner_rect
        if w > inner.width or h > inner.height:
            raise Exception(u'Box too small for button "'+text+'"'+\
                u'required: '+str((w,h))+u' available: '+\
                str((inner.width,inner.height)))
        self.pos=(inner.x,inner.bottom-h) 
        self.img=font.render(text,config.font_color,config.bckg_color)

    # Does this widget accept focus?
    def accepts_focus(self):
        return False

    # Draw thyself
    # Return updated rectangle if there was an update, None otherwise
    def update(self,surface):
        surface.blit(self.img,self.pos)
        return self.rect
    
    # Handle event, return True if handled
    # If some other widget handled it already 'handled' is True
    def handle(self, event, handled=False):
        return False

if __name__ == "__main__":
    pygame.init()
    scr = pygame.display.set_mode((300,600))
    scr.fill(config.bckg_color)
    l1=Label(u'Label One',10,10,150,50)
    l2=Label(u'Label Two',10,70)
    l1.draw(scr)
    l2.draw(scr)
    pygame.display.update()
    while pygame.event.wait().type != pg.QUIT: pass
