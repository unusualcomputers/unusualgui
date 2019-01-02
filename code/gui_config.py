from singleton import Singleton
from borders import BorderType

class Config:
    __metaclass__=Singleton
    # global settings
    font_name="comicsansms"
    font_size=20
    font_color=(255,128,0)
    bckg_color=(32,0,32)

    # selection settings
    sel_font="comicsans"
    sel_font_color=(255,140,0)
    clicked_font_color=(255,110,0)
    sel_bckg_color=(16,0,16)
    sel_border_color=sel_font_color
    clicked_border_color=clicked_font_color
    

    # borders
    border_color=font_color
    border_fill_color=bckg_color
    border_type=BorderType.SIMPLE
    border_radius=5
    border_thickness=1

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
