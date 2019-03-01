import init
from gui_config import Config
from switch import Switch
from vframe import VFrame

class Radio(VFrame):

    class radio_func:
        def __init__(self):
            pass
        def init(self,switches):
            self.switches=switches
        def __call__(self,o,text):
            for s in self.switches: 
                if s.text!=text:
                    s.set(False)

    def __init__(self,options,default,x,y,width,height,
            config=Config.default_drawing_conf):
        radio=[]
        f=Radio.radio_func()    
        for o in options:
            s=Switch(o,o==default,x,y,width,height,f,config,True)
            radio.append(s)        
        f.init(radio)
        
        VFrame.__init__(self,radio,x,y,width,height,False,config)

if __name__ == "__main__":
    import pygame
    from widgets import Widgets
    r1=Radio([u'One',u'Two',u'Three',u'Four',u'Five'],u'Five',25,25,260,250)
    r2=Radio([u'One',u'Two',u'Three',u'Four'],u'Two',25,300,260,250)
    scr = pygame.display.set_mode((300,600))
    scr.fill(Config.default_drawing_conf.bckg_color)
    widgets=Widgets();
    widgets.add([r1,r2])
    widgets.run(scr)      
