from Data.instance import *

import pygame
pygame.init()

def GatherEvent():
    return pygame.event.get()

def ClearEvent():
    pygame.event.get()