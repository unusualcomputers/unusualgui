import pygame
import init
from gui_config import Config
from events import *
from widget import Widget
from borders import Borders

def _default_update_func(x):
    print 'progress control is at ',x

class Progress(Widget):
    def __init__(self,
            value,
            x,y,width,height,
            config=Config.default_drawing_conf,
            min_value=0.0,max_value=1.0,
            step_size=None,
            update_func=_default_update_func):
        Widget.__init__(self,x,y,width,height,config)
        self.__value=value
        self.__min=min_value
        self.__max=max_value
        
        self.takes_input=True
        if update_func:
            self.__update_func=update_func    
        else:
            self.__update_func=__default_update_func
        if step_size:
            self.__step_size=step_size
        else:
            self.__step_size=(max_value-min_value)/50.0
        self.__tooltip_style=config.progress_tooltip
        if self.__tooltip_style!=0:
            self.__tooltip_font=self.fonts.get_font(
                config.font_name,config.progress_tooltip_font_sz)
        
            if min_value==0.0 and max_value==1.0:
                self.__value_format=lambda x : ('%i%%' % int(x*100)).rjust(4)
            else:
                self.__value_format=lambda x : \
                    ('%i' % x).rjust(len(str(self.__max)))


    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self,v):
        if v==self.__value: return
        if v<self.__min: self.__value=self.__min
        elif v>self.__max: self.__value=self.__max
        else: self.__value=v
        self.needs_update=True

    # Draw thyself
    # Return updated rectangle if there was an update, None otherwise
    def update(self,surface):
        p=(self.__value-self.__min)/(self.__max-self.__min)
        conf=self.config
        if self.has_focus:
            border_color=conf.sel_border_color
        else:
            border_color=conf.border_color
        fill_color=conf.clicked_border_fill_color
        bckg_color=conf.bckg_color
        # 0-thin line,1-rectangular,else-rounded
        if conf.progress_style == 0:
            mid=int(self.rect.left+p*self.rect.width)
            y=self.rect.top
            pygame.draw.line(surface,border_color,(self.rect.left,y),(mid,y))
            pygame.draw.line(surface,fill_color,(mid,y),(self.rect.right,y))
        elif conf.progress_style==1:
            self.borders.draw_partial(surface,self.rect,border_color,
                fill_color,bckg_color,p,False)
        else: 
            self.borders.draw_partial(surface,self.rect,border_color,
                fill_color,bckg_color,p,True)
        #TODO: draw tooltip
        if self.__tooltip_style==1:
            text=self.__value_format(self.__value)
            font=self.__tooltip_font
            (w,h)=font.size(self.__value_format(self.__max))
            inner=self.inner_rect
            if w > inner.width or h > inner.height:
                raise Exception(u'Box too small for label "'+text+'"'+\
                    u'required: '+str((w,h))+u' available: '+\
                    str((inner.width,inner.height)))
            pos=(inner.x+(inner.width-w)/2.0,inner.y+(inner.height-h)/2.0) 
            img=font.render(text,conf.progress_tooltip_font_color,(0,0,0))
            img.set_colorkey((0,0,0))
            img.set_alpha(conf.progress_tooltip_alpha)
            surface.blit(img,pos)
        self.needs_update=False
        return self.rect
 
    def __mouse_pos_to_value(self,x):
        xx=float(x-self.x)/float(self.width)
        if xx <0: xx=0
        elif xx > 1.0: xx=1.0
        self.value = (self.__max-self.__min)*xx
        
    # Handle event, return True if handled
    # If some other widget handled it already 'handled' is True
    def handle(self, event, handled=False):
        if not self.takes_input: return False
        if isinstance(event,MouseUp) or isinstance(event,Dragging):
            self.__mouse_pos_to_value(event.pos[0])
            return True
        elif isinstance(event,Scroll):
            if event.direction==Direction.up or \
                event.direction==Direction.right:
                self.value+=self.__step_size
            else:
                self.value-=self.__step_size
            return True
        elif isinstance(event,KeyDown):
           if event.key==pygame.K_RIGHT or event.key==pygame.K_UP:
                self.value+=self.__step_size
                return True
           elif event.key==pygame.K_LEFT or event.key==pygame.K_DOWN:
                self.value-=self.__step_size
                return True
        return False 

if __name__ == "__main__":
    p1=Progress(32,10,10,150,32,min_value=13,max_value=2109)
    p2=Progress(0.3,10,70,150,40)
    config=Config.widgets()
    config.progress_style=0
    config.progress_tooltip=0
    p3=Progress(0.65,10,130,150,1,config=config)
    config=Config.widgets()
    config.progress_style=1
    p4=Progress(0.99,10,190,150,50,config=config)
    from widgets import Widgets
    scr = pygame.display.set_mode((300,600))
    scr.fill(Config.default_drawing_conf.bckg_color)
    widgets=Widgets();
    widgets.add((p1,p2,p3,p4))
    widgets.run(scr)      
