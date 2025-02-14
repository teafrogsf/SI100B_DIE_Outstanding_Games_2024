import pygame
import sys
from account_setter import account_admin
from load_picture import pictures
from bgmplayer import BgmPlayer
import transition_effect
import opening
import login
import gal
import menu

pygame.init()
acer = account_admin()
pic = pictures

screen_image = pygame.display.set_mode((900,560))
pygame.display.set_caption('Soul Knight')

bgm = BgmPlayer()
bgm.play('Soul_Soil.mp3', -1)

opening.opening(screen_image)
pygame.time.wait(1000)
transition_effect.fade_out(screen_image)

logined = False
while not logined:
    username = login.login(screen_image, bgm)
    logined = True
    user_resource = acer.get_resource(username)
    if user_resource['has_read0'] == 0:
        transition_effect.fade_out(screen_image)
        gal.gal(screen_image, username, 'Text\\Chapter0.txt', pic.Soul_knight_background, bgm, 'Soul_Soil.mp3')
        user_resource['has_read0'] = 1
        acer.update_resource(username, user_resource)

    transition_effect.fade_out(screen_image)
    result = menu.menu(screen_image, username, bgm)
    transition_effect.fade_out(screen_image)
    if result == -1:
        logined = False

pygame.quit()
sys.exit()

