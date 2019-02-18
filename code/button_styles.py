import pygame
import init
from gui_config import Config
from borders import *

class ButtonStyle:
    # Default style for a button 
    class Default:
        def __init__(self,button,text):
            self.button=button
            self.init(text)

        def init(self,text):
            button=self.button
            self.borders=button.borders
            self.config=button._config
     
            font=button.fonts.get_font(self.config.font_name,
                self.config.font_size)
            (w,h)=font.size(text)
            inner=button.inner_rect
            if w > inner.width or h > inner.height:
                raise Exception(u'Box too small for button "'+text+'"'+\
                    u'required: '+str((w,h))+u' available: '+\
                    str((inner.width,inner.height)))
            self.pos=(inner.x+(inner.width-w)/2.0,inner.y+(inner.height-h)/2.0) 
            self.img=font.render(text,self.config.font_color,
                self.config.border_fill_color)
            self.focus_img=font.render(text,
                self.config.sel_font_color,self.config.sel_border_fill_color)
            self.clicked_img=font.render(text,self.config.clicked_font_color,
                self.config.clicked_border_fill_color)
            return self       
 
        def _draw_clicked(self,surface):
            self._draw_border(surface)
            surface.blit(self.clicked_img,self.pos)
            
        def _draw_not_clicked(self,surface):
            self._draw_border(surface)
            if self.button.has_focus:
                surface.blit(self.focus_img,self.pos)
            else:
                surface.blit(self.img,self.pos)
            
        def _draw_border(self,surface):
            rect=self.button.rect
            config=self.config
            if self.button.is_clicked:
                self.borders.draw(surface,rect,
                    config.border_radius,config.border_thickness,
                    config.clicked_border_color,
                    config.clicked_border_fill_color)
            elif self.button.has_focus:
                self.borders.draw(surface,rect,
                    config.border_radius,config.border_thickness,
                    config.sel_border_color,
                    config.sel_border_fill_color)
            else:
                self.borders.draw(surface,rect,
                    config.border_radius,config.border_thickness,
                    config.border_color,
                    config.border_fill_color)

    # Button style with text only 
    class Text:
        def __init__(self,button,text):
            self.button=button
            self.init(text)

        def init(self,text):
            button=self.button
            self.borders=button.borders
            config=button._config
     
            font=button.fonts.get_font(config.font_name,config.font_size)
            (w,h)=font.size(text)
            inner=button.inner_rect
            if w > inner.width or h > inner.height:
                raise Exception(u'Box too small for button "'+text+'"'+\
                    u'required: '+str((w,h))+u' available: '+\
                    str((inner.width,inner.height)))
            self.pos=(inner.x+(inner.width-w)/2.0,inner.y+(inner.height-h)/2.0) 
            self.img=font.render(text,config.font_color,config.bckg_color)

            font_sel=button.fonts.get_font(config.font_name,config.font_size,
                underline=True)
            self.focus_img=font_sel.render(text,
                config.sel_font_color,config.bckg_color)
            self.clicked_img=font.render(text,config.clicked_font_color,
                config.bckg_color)
            self.clicked_sel_img=font_sel.render(text,config.clicked_font_color,
                config.bckg_color)
        
        def _draw_clicked(self,surface):
            if self.button.has_focus:
                surface.blit(self.clicked_sel_img,self.pos)
            else:
                surface.blit(self.clicked_img,self.pos)
        
        def _draw_not_clicked(self,surface):
            if self.button.has_focus:
                surface.blit(self.focus_img,self.pos)
            else:
                surface.blit(self.img,self.pos)

    # Button style with no borders 
    class Borderless:
        def __init__(self,button,text):
            self.button=button
            self.init(text)

        def init(self,text):
            button=self.button
            config=button._config
     
            font=button.fonts.get_font(config.font_name,config.font_size)
            (w,h)=font.size(text)
            inner=button.inner_rect
            if w > inner.width or h > inner.height:
                raise Exception(u'Box too small for button "'+text+'"'+\
                    u'required: '+str((w,h))+u' available: '+\
                    str((inner.width,inner.height)))
            wdth=button.width
            hght=button.height
            pos=((wdth-w)/2.0,(hght-h)/2.0)
            self.pos=(button.x,button.y) 
           
            surface=pygame.Surface((button.rect.width, button.rect.height))
            surface.fill(config.border_fill_color)
            surface.blit(font.render(text,config.font_color,
                config.border_fill_color),pos) 
            self.img=surface.copy()
            surface.fill(config.sel_border_fill_color)
            surface.blit(font.render(text,
                config.sel_font_color,config.sel_border_fill_color),pos) 
            self.focus_img=surface.copy()
            surface.fill(config.clicked_border_fill_color)
            surface.blit(font.render(text,config.clicked_font_color,
                config.clicked_border_fill_color),pos) 
            self.clicked_img=surface.copy()
        
        def _draw_clicked(self,surface):
            surface.blit(self.clicked_img,self.pos)
        
        def _draw_not_clicked(self,surface):
            if self.button.has_focus:
                surface.blit(self.focus_img,self.pos)
            else:
                surface.blit(self.img,self.pos)
