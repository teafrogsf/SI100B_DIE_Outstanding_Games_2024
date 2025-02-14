import pygame
import sys
from GameSettings import *
from GameManager import GameManager


def main():
    global manager
    pygame.init()
    window = pygame.display.set_mode((WindowSettings.width, WindowSettings.height))
    pygame.display.set_caption(WindowSettings.title)
    manager = GameManager(window)
    while True:
        manager.update()
        manager.render()
        pygame.time.Clock().tick(WindowSettings.fps)


if __name__ == "__main__":
    main()
