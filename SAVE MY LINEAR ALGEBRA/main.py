import pygame
from GameManager import GameManager


def main():

    pygame.init()
    game_manager: GameManager = GameManager()

    while True:
        game_manager.update()


if __name__ == "__main__":
    main()
