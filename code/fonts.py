import pygame

class Fonts:
    class __FontWithCache:
        def __init__(self,font):
            self.font=font
            self.__text_cache={}
            self.__antialias=True

        def render(self,text,color,bckg_color):
            key=(text,color,bckg_color)
            if key in self.__text_cache:
                return self.__text_cache
            image=self.font.render(text,self.__antialias,color,bckg_color)
            self.__text_cache[key]=image
            return image

    class __SingletonFonts: 
        def __init__(self):
            self.__fonts_cache={}

        def get_font(font_name, size, bold=False, italic=False):
            key=(font_name,size,bold,italic)
            font=self.__fonts_cache.get(key, None)
            if font==None:
                font=Fonts.__FontWithCache(
                    pygame.font.SysFont(font_name,size,bold,italic))
                self.__fonts_cache[key]=font
            return font

    
    __instance=None
    def __init__(self):
        if not Fonts.__instance:
            Fonts.__instance=Fonts.__FontsBorders()
            
    def __getattr__(self,name):
        return getattr(self.__instance,name)
