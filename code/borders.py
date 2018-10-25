import pygame as pg
from enum import Enum
class BorderType(Enum):
    NONE=0
    SIMPLE=1
    OPEN=2
    ROUNDED=3
    ROUNDED_FILLED=4

class Borders:
    class __SingletonBorders: 
        def __init__(self):
            # cache for bresenham circle points
            # one entry per radius, centered at (radius,radius)
            self.rr_cache={}


        # rounded rectangle border, an adaptation of algorithm described here:
        # https://web.engr.oregonstate.edu/~sllu/bcircle.pdf
        def _calc_bresenham(self,r):
            if r in self.rr_cache: return self.rr_cache[r]
            self.rr_cache[r]=[]
            points=self.rr_cache[r]

            x=r
            y=0
            xch=1-2*r
            ych=1
            rerr=0
            while x >= y:
                #octant 1
                points.append((x,y))
                
                y+=1
                rerr+=ych
                ych+=2
                if (2*rerr+xch)>0:
                    x-=1
                    rerr+=xch
                    xch+=2
            return points

        # rounded rectangle border, an adaptation of algorithm described here:
        # https://web.engr.oregonstate.edu/~sllu/bcircle.pdf
        def _bresenham_border(self,surface,rect,color,r):
            rect=pg.Rect(rect)
            col=surface.map_rgb(pg.Color(*color))
            top=rect.top
            bottom=rect.bottom
            left=rect.left
            right=rect.right   
            points=self._calc_bresenham(r)
            parr=pg.PixelArray(surface)
            
            cx1278=right-r
            cy1234=bottom-r
            cx3456=left+r
            cy5678=top+r
            for i in range(0,len(points)):
                (x,y)=points[i]
                #octant 1
                parr[cx1278+x,cy1234+y]=col
                #octant 2
                parr[cx1278+y,cy1234+x]=col
                #octant 3
                parr[cx3456-y,cy1234+x]=col
                #octant 4
                parr[cx3456-x,cy1234+y]=col
                #octant 5
                parr[cx3456-x,cy5678-y]=col
                #octant 6
                parr[cx3456-y,cy5678-x]=col
                #octant 7
                parr[cx1278+y,cy5678-x]=col
                #octant 8
                parr[cx1278+x,cy5678-y]=col
            
            for i in range(left+r,right-r+1):
                parr[i,top]=col
                parr[i,bottom]=col
            
            for i in range(top+r,bottom-r+1):
                parr[left,i]=col
                parr[right,i]=col
                
            del parr
        
        def _bresenham_filled(self,surface,rect,color_border,color_fill,r):
            rect=pg.Rect(rect)
            col=surface.map_rgb(pg.Color(*color_border))
            if color_fill is None:
                color_fill=color_border
                col_fill=col
            else:
                col_fill=surface.map_rgb(pg.Color(*color_fill))
            
            top=rect.top
            bottom=rect.bottom
            left=rect.left
            right=rect.right   
            points=self._calc_bresenham(r)
            surface.fill(color_fill,rect.inflate(0,-2*r))
            parr=pg.PixelArray(surface)
            
            cx1278=right-r
            cy1234=bottom-r
            cx3456=left+r
            cy5678=top+r
            for i in range(0,len(points)):
                (x,y)=points[i]
                #octant 1
                parr[cx1278+x,cy1234+y]=col
                #octant 2
                parr[cx1278+y,cy1234+x]=col
                #octant 3
                parr[cx3456-y,cy1234+x]=col
                #octant 4
                parr[cx3456-x,cy1234+y]=col
                #octant 5
                parr[cx3456-x,cy5678-y]=col
                #octant 6
                parr[cx3456-y,cy5678-x]=col
                #octant 7
                parr[cx1278+y,cy5678-x]=col
                #octant 8
                parr[cx1278+x,cy5678-y]=col
                for j in range(cx3456-y+1,cx1278+y):
                    parr[j,cy1234+x]=col_fill
                    parr[j,cy5678-x]=col_fill
                for j in range(cx3456-x+1,cx1278+x):
                    parr[j,cy1234+y]=col_fill
                    parr[j,cy5678-y]=col_fill
            
            for i in range(left+r,right-r+1):
                parr[i,top]=col
                parr[i,bottom]=col
           
            for i in range(top+r,bottom-r+1):
                parr[left,i]=col
                parr[right,i]=col
                
            del parr
        
        def draw(self,border_type,surface,rect,
                color_border,color_fill=None,
                radius=0,thickness=1):
            if border_type == BorderType.NONE:
                return
            elif border_type == BorderType.SIMPLE:
                pg.draw.rect(surface,color_border,rect,thickness)
                if color_fill:
                    rect=pg.Rect(rect).inflate(-2,-2)
                    surface.fill(color_fill,rect)
            elif border_type == BorderType.OPEN:
                rect=pg.Rect(rect)
                top=rect.top
                bottom=rect.bottom
                left=rect.left
                right=rect.right   
                pg.draw.line(surface,color_border,
                    (left+radius,top),(right-radius,top),thickness)
                pg.draw.line(surface,color_border,
                    (left+radius,bottom),(right-radius,bottom),thickness)
                pg.draw.line(surface,color_border,
                    (left,top+radius),(left,bottom-radius),thickness)
                pg.draw.line(surface,color_border,
                    (right,top+radius),(right,bottom-radius),thickness)
            elif border_type == BorderType.ROUNDED:
                self._bresenham_border(surface,rect,color_border,radius)
            elif border_type == BorderType.ROUNDED_FILLED:
                self._bresenham_filled(surface,rect,
                    color_border,color_fill,radius)

    __instance=None
    def __init__(self):
        if not Borders.__instance:
            Borders.__instance=Borders.__SingletonBorders()
            
    def __getattr__(self,name):
        return getattr(self.__instance,name)

if __name__ == "__main__":
    scr = pg.display.set_mode((300,600))
    scr.fill(-1)
    f=32
    w=150
    h=50
    d=10
    t=1
    c=(250,0,0)
    c2=(120,0,0)
    b=Borders()
    b.draw(BorderType.NONE,scr,(10,10,w,h),c,radius=d)
    b.draw(BorderType.SIMPLE,scr,(10,100,w,h),c,radius=d)
    b.draw(BorderType.OPEN,scr,(10,160,w,h),c,radius=d)
    b.draw(BorderType.ROUNDED,scr,(10,220,w,h),c,radius=d)
    b.draw(BorderType.ROUNDED_FILLED,scr,(10,280,w,h),c,radius=d)
    b.draw(BorderType.ROUNDED_FILLED,scr,(10,350,w,h),c,c2,radius=d)
    b.draw(BorderType.SIMPLE,scr,(10,420,w,h),c,c2,radius=d)
    pg.display.update()
    while pg.event.wait().type != pg.QUIT: pass
