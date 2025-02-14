import os
import random
import sys
import time

import pygame

import AIHelper
import Client
import Config
import I18n
from Config import SCREEN_WIDTH, SCREEN_HEIGHT, MAP_WIDTH, MAP_HEIGHT, BLOCK_SIZE
from entity.Entity import Monster
from entity.Player import Player
from render import Renderer, Particle, Action
from render.Renderer import ImageRenderer
from ui.StarterUI import StarterUI


def main():
    Config.RUNNING = True

    os.environ["SDL_IME_SHOW_UI"] = "1"

    print('=================================================================')
    print('Thanks for playing Redemption！')
    print('=================================================================')

    pygame.init()
    pygame.display.set_caption("Redemption")
    pygame.display.set_icon(pygame.image.load("./assets/ui/icon.png"))
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    pygame.mixer.init()
    pygame.scrap.init()
    pygame.key.stop_text_input()

    player = Player(I18n.text('player_name'), (1024, 1024), (1024, 1024), Renderer.PLAYER, size=(50, 50))

    Config.CLIENT = Client.Client(screen, clock, player, 'the_world')
    Config.CLIENT.open_ui(StarterUI())

    for _ in range(12):
        Config.CLIENT.spawn_entity(
            Monster(I18n.text('zombie'), (1200 + random.randint(0, MAP_WIDTH * BLOCK_SIZE - 1250),
                                          random.randint(0, MAP_HEIGHT * BLOCK_SIZE - 50)),
                    ImageRenderer(pygame.transform.scale(pygame.image.load("./assets/entities/zombie.png"), (50, 50))),
                    coins=8)
        )
    for _ in range(12):
        Config.CLIENT.spawn_entity(
            Monster(I18n.text('skeleton'), (1200 + random.randint(0, MAP_WIDTH * BLOCK_SIZE - 1250),
                                            random.randint(0, MAP_HEIGHT * BLOCK_SIZE - 50)),
                    ImageRenderer(pygame.transform.scale(pygame.image.load("./assets/entities/skeleton.png"),
                                                         (50, 50))),
                    coins=12, actions=[Action.ARROW_LEFT])
        )

    while True:
        st = time.time()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                Config.RUNNING = False
                AIHelper.thread.join()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                Particle.UI_PARTICLES.add(Particle.ClickParticle((pos[0] - 16, pos[1] - 16), 30))

        Config.CLIENT.tick(events)

        # 执行渲染
        pygame.display.flip()
        if time.time() - st > 1 / 90:
            print(time.time() - st)

        clock.tick(90)


if __name__ == "__main__":
    main()
