from singleton import Singleton
import copy

class DrawingConfig:
    def __init__(self):
        # global settings
        self.font_name="comicsansms"
        self.font_size=20
        self.font_color=(255,128,0)
        self.bckg_color=(32,0,32)

        # borders
        self.border_color=self.font_color
        self.border_fill_color=self.bckg_color
        self.border_radius=5
        self.border_thickness=1
        
        # padding
        self.padding=self.border_radius
        
        # selection settings
        self.sel_font=self.font_name
        self.sel_font_color=(255,160,0)#self.font_color
        self.sel_border_fill_color=self.border_fill_color
        self.sel_border_color=self.sel_font_color
        self.clicked_font_color=(255,100,0)
        self.clicked_border_fill_color=(128,0,128)
        self.clicked_border_color=self.clicked_font_color

        # label
        self.label_align='left' # left,center,right

        # progress
        self.progress_style='round' # thin,rect,round
        self.progress_tooltip='inside' # none,inside,floating
        self.progress_tooltip_font_sz=self.font_size
        self.progress_tooltip_alpha=128
        self.progress_tooltip_font_color=self.font_color

        # graphics
        self.trig_button_radius=10
        self.trig_button_ratio=2
        
        self.trig_button_border_color=(128,0,128)#self.border_color
        self.trig_button_empty_color=self.bckg_color
        self.trig_button_fill_color=self.clicked_border_fill_color

    def copy(self):
        return copy.deepcopy(self)

    def with_no_border(self):
        n=self.copy()
        n.border_thickness=0
        return n

    def with_rect_border(self):
        n=self.copy()
        n.border_radius=0
        return n

class Config:
    __metaclass__=Singleton

    # Drawing config
    default_drawing_conf=DrawingConfig()

    @classmethod
    def widgets(cls): return cls.default_drawing_conf.copy()

    # fps is maximum number of frames per second in pygame
    # basically determines how often the message loop is run per second
    fps=40

    # MouseDown with no MouseUp and when motion is less then mouse_long_distance
    #   is MouseLong
    # If mouse is moved more than mouse_long_distance before MouseUp
    #   Dragging starts
    # Then Dragging event is generated every drag_tick seconds unless that is 0
    # Once mouse is up, MouseLongEnd is generated 
    mouse_long_time=1000

    # MouseMotion with one of the buttons pressed is Dragging unless we are 
    #   in MouseLong already or distance covered is less than drag_min_distance
    #   NOTE: once we move more than drag_min_distance subsequent moves can be 
    #   smaller
    drag_min_distance=10
    
    # If a key is down for longer then key_repeat_start, start sending KeyUp 
    #   every key_repeat milliseconds
    # NOTE: this means that not every KeyUp is preceded by KeyDown
    key_repeat_start=1000
    key_repeat=500
