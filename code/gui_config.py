from singleton import Singleton
from borders import BorderType

class Config:
    __metaclass__=Singleton
    # global settings
    font_name="comicsansms"
    font_size=20
    font_color=(255,128,0)
    bckg_color=(32,0,32)

    # selection settings, e.g. clicked button
    sel_font="comicsans"
    sel_font_color=(255,128,128)
    sel_bckg_color=(16,0,16)
    sel_border_color=(255,128,0)

    # borders
    border_color=font_color
    border_fill_color=sel_bckg_color
    border_type=BorderType.SIMPLE
    border_radius=5
    border_thickness=1

