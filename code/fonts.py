import pygame
import init
from singleton import Singleton

class _FontWithCache:
    def __init__(self,font):
        self.font=font
        self.__text_cache={}
        self.__antialias=True

    def render(self,text,color,bckg_color):
        key=(text,color,bckg_color)
        if key in self.__text_cache:
            return self.__text_cache[key]
        image=self.font.render(text,self.__antialias,color,bckg_color)
        self.__text_cache[key]=image
        return image

    def __getattr__(self,name):
        if name=='render':
            return self.render
        return getattr(self.font,name)

class Fonts:
    __metaclass__=Singleton
    def __init__(self):
        self.__fonts_cache={}

    def get_font(self,font_name,size,bold=False,italic=False,underline=False):
        key=(font_name,size,bold,italic,underline)
        font=self.__fonts_cache.get(key, None)
        if font==None:
            font=_FontWithCache(
                pygame.font.SysFont(font_name,size,bold,italic))
            font.font.set_underline(underline)
            self.__fonts_cache[key]=font
        return font

