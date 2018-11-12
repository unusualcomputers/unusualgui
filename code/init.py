import pygame
from singleton import Singleton

screen_size=(300,600)

class Init:
    __metaclass__=Singleton

    def __init__(self):
        pygame.init()
        pygame.display.set_mode(screen_size)
        print u'Unusual GUI initialized'

Init()
