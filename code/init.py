import pygame
from singleton import Singleton
from gui_config import Config

screen_size=(300,600)

class Init:
    __metaclass__=Singleton

    def __init__(self):
        pygame.init()
        pygame.display.set_mode(screen_size)
        pygame.key.set_repeat(Config.key_repeat_start,Config.key_repeat)
        print u'Unusual GUI initialized'

Init()
