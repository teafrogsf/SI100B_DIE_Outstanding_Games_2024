import pygame

from Player import Player
from GameManager import Gamemanager
from Settings import *

def run():
    #init
    pygame.init()
    window = pygame.display.set_mode((WindowSettings.width, WindowSettings.height))
    pygame.display.set_caption("Genshin Impact")
    pygame.display.set_icon( pygame.image.load(r".\assets_library\PlayerBasic\PlayerIdle.png") )

    player = Player()
    manager = Gamemanager(window, player)

    while True:
        manager.tick(30)
        #shop和victory两个场景需要调用pygame事件队列来渲染
        if manager.state != GameState.VICTORY and manager.state != GameState.GAME_PLAY_SHOP:
            manager.event_queue(player)
        if manager.state == GameState.GAME_PLAY_SHOP and manager.scene.quit:
            manager.event_queue(player)
        keys = pygame.key.get_pressed()
        if manager.state == GameState.MAIN_MENU or manager.state == GameState.GAME_PLAY_PAUSE or manager.state == GameState.GAME_PLAY_DEAD or manager.state == GameState.VICTORY or manager.state == GameState.GAME_PLAY_SHOP:
            manager.render()
        else:
            manager.update(player)
            manager.render()
            player.update(keys, manager.scene)
            player.draw(window, manager.scene.cameraX, manager.scene.cameraY) 

        pygame.display.flip()

if __name__ == "__main__":
    run()