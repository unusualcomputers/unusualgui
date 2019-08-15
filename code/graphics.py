import pygame
import init
from singleton import Singleton
import math
try:
    import pygame.gfxdraw
    use_gfx=True
except ImportError:
    import pygame.draw
    use_gfx=False

class Graphics:
    __metaclass__=Singleton
    def __init__(self):
        self.__down={}
        self.__up={}
        self.__left={}
        self.__right={}
  
    def __left_points(self,r,q):
        d=2*r
        x1=int(round(0.067*d+0.5))
        x2=d-x1
        x3=x2
        y1=r
        y2=0
        y3=d
        points=[(x1,y1),(x2,y2),(x3,y3)]
        d1=int(r/float(q)+0.5)
        d2=int(d1/1.732+0.5)
        inner_points=[(x1+d1,y1),(x2-d2,y2+d1),(x3-d2,y3-d1)]
        return (points,inner_points)

    def __right_points(self,r,q):
        d=2*r
        x2=int(round(0.067*d+0.5))
        x1=d-x2
        x3=x2
        y1=r
        y2=0
        y3=d
        points=[(x1,y1),(x2,y2),(x3,y3)]
        d1=int(r/float(q)+0.5)
        d2=int(d1/1.732+0.5)
        inner_points=[(x1-d1,y1),(x2+d2,y2+d1),(x3+d2,y3-d1)]
        return (points,inner_points)

    def __down_points(self,r,q):
        d=2*r
        y1=int(round(0.067*d+0.5))
        y2=y1
        y3=d-y1
        x1=0
        x2=d
        x3=r#=d/2
        points=[(x1,y1),(x2,y2),(x3,y3)]
        d1=int(r/float(q)+0.5)
        d2=int(d1/1.732+0.5)
        inner_points=[(x1+d1,y1+d2),(x2-d1,y2+d2),(x3,y3-d1)]
        return (points,inner_points)
    
    def __up_points(self,r,q):
        d=2*r
        #height=1.732/2.0*d
        #y1=(d-height)/2.0=(1.0-1.732/2.0)*d/2.0=(0.5-1.732/4.0)*d
        y1=int(round(0.067*d+0.5))
        y2=d-y1
        y3=y2
        x3=0
        x2=d
        x1=int(float(d)/2.0+0.5)
        points=[(x1,y1),(x2,y2),(x3,y3)]
        d1=int(r/float(q)+0.5)
        d2=int(d1/1.732+0.5)
        inner_points=[(x1,y1+d1),(x2-d1,y2-d2),(x3+d1,y3-d2)]
        return (points,inner_points)
    
    def __trig(self,config,screen,filled,points_f, cache):
        (r,q,colb)=(config.trig_button_radius, 
            config.trig_button_ratio,
            config.trig_button_border_color)
      
        if filled:
            inside_col=config.trig_button_fill_color
        else:
            inside_col=config.trig_button_empty_color 
        if (r,colb,inside_col) in cache:
            return cache[(r,colb,inside_col)]
        d=2*r
        surface=pygame.Surface((d,d),
            screen.get_flags() | pygame.SRCALPHA,
            screen.get_bitsize(),screen.get_masks())
        (points,inner_points)=points_f(r,q)        
        if use_gfx:
            pygame.gfxdraw.filled_polygon(surface,inner_points,inside_col)
            pygame.gfxdraw.aapolygon(surface,inner_points,inside_col)
            pygame.gfxdraw.aapolygon(surface,points,colb)
            for p in points+inner_points:
                pygame.gfxdraw.pixel(surface,p[0],p[1],config.bckg_color)
        else:
            pygame.draw.lines(surface,colb,True,points,1)
        cache[(r,colb,inside_col)]=surface
        return surface
    
    def right(self,config,screen,filled=False):
        return self.__trig(config,screen,filled,
            self.__right_points,self.__right)

    def left(self,config,screen,filled=False):
        return self.__trig(config,screen,filled,
            self.__left_points,self.__left)

    def up(self,config,screen,filled=False):
        return self.__trig(config,screen,filled,
            self.__up_points,self.__up)
    
    def down(self,config,screen,filled=False):
        return self.__trig(config,screen,filled,
            self.__down_points,self.__down)
    
        
if __name__ == "__main__":
    from gui_config import Config
    from widgets import Widgets
    scr = pygame.display.set_mode((300,600))
    g=Graphics()
    conf=Config.default_drawing_conf
    b1=g.up(conf,scr)
    b2=g.up(conf,scr,True)
    b3=g.down(conf,scr)
    b4=g.down(conf,scr,True)

    b5=g.left(conf,scr)
    b6=g.left(conf,scr,True)
    b7=g.right(conf,scr)
    b8=g.right(conf,scr,True)
   
    a=conf.trig_button_radius
    scr.blit(b1,(a,a))
    scr.blit(b2,(a,4*a))
    scr.blit(b3,(a,8*a)) 
    scr.blit(b4,(a,12*a)) 
    scr.blit(b5,(4*a,a))
    scr.blit(b6,(4*a,4*a))
    scr.blit(b7,(4*a,8*a))
    scr.blit(b8,(4*a,12*a))
    
    conf=conf.copy()
    conf.trig_button_radius=20
    print 20
    b11=g.up(conf,scr)
    print b11.get_height()
    b12=g.up(conf,scr,True)
    b13=g.down(conf,scr)
    print b12.get_height()
    b14=g.down(conf,scr,True)

    b15=g.left(conf,scr)
    print b15.get_height()
    b16=g.left(conf,scr,True)
    b17=g.right(conf,scr)
    print b17.get_height()
    b18=g.right(conf,scr,True)
   
    o=100
    a=conf.trig_button_radius
    scr.blit(b11,(o+a,a))
    scr.blit(b12,(o+a,4*a))
    scr.blit(b13,(o+a,8*a)) 
    scr.blit(b14,(o+a,12*a)) 
    scr.blit(b15,(o+4*a,a))
    scr.blit(b16,(o+4*a,4*a))
    scr.blit(b17,(o+4*a,8*a))
    scr.blit(b18,(o+4*a,12*a))
    

    conf=conf.copy()
    conf.trig_button_radius=5
    b11=g.up(conf,scr)
    b12=g.up(conf,scr,True)
    b13=g.down(conf,scr)
    b14=g.down(conf,scr,True)

    b15=g.left(conf,scr)
    b16=g.left(conf,scr,True)
    b17=g.right(conf,scr)
    b18=g.right(conf,scr,True)
   
    o=250
    a=conf.trig_button_radius
    scr.blit(b11,(o+a,a))
    scr.blit(b12,(o+a,4*a))
    scr.blit(b13,(o+a,8*a)) 
    scr.blit(b14,(o+a,12*a)) 
    scr.blit(b15,(o+4*a,a))
    scr.blit(b16,(o+4*a,4*a))
    scr.blit(b17,(o+4*a,8*a))
    scr.blit(b18,(o+4*a,12*a))
    pygame.display.update()
    widgets=Widgets();
    widgets.run(scr)      
                    
