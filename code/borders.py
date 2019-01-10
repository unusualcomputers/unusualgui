import pygame as pg
from enum import Enum
from singleton import Singleton

class Borders:
    __metaclass__=Singleton
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
            # lines 1 to 4
            yy14=cy1234+y
            # lines 5 to 8
            yy58=cy5678-y
            l=min(cx1278+x, cx3456-x)
            rr=max(cx1278+x, cx3456-x)
            for j in range(l+1,rr):
                parr[j,yy14]=col_fill
                parr[j,yy58]=col_fill
            # lines 2 to 3
            yy23=cy1234+x
            # lines 6 to 7
            yy67=cy5678-x
            l=min(cx1278+y, cx3456-y)
            rr=max(cx1278+y, cx3456-y)
            for j in range(l+1,rr):
                parr[j,yy23]=col_fill
                parr[j,yy67]=col_fill
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
    
    def draw(self,surface,rect,
            radius=0,thickness=1,
            color_border=None,color_fill=None):
        if thickness==0 or color_border==None:
            return
        elif radius==0:
            pg.draw.rect(surface,color_border,rect,thickness)
            if color_fill is not None:
                rect=pg.Rect(rect).inflate(-2,-2)
                surface.fill(color_fill,rect)
        else:
            if color_fill is not None:
                self._bresenham_filled(surface,rect,
                    color_border,color_fill,radius)
            else:            
                self._bresenham_border(surface,rect,color_border,radius)

