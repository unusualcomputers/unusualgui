import pygame
from singleton import Singleton

class Init:
    __metaclass__=Singleton

    def __init__(self):
        pygame.init()
        print u'Unusual GUI initialized'

Init()
