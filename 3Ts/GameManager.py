import pygame, sys, Menu, ChatBox
from GameSettings import *
from SettingPage import SettingPage
from MapPage import MapPage
from Utility import BgmPlayer, Scene
from Player import Player
from HelpPage import HelpPage
from ShopPage import ShopPage
import battleController
import random
import upgradeCharacter
import difficultyController


class GameManager:

    def __init__(self, window):
        global events, listeners
        self.window = window
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.menu = Menu.Menu(window)
        self.bgmplayer = BgmPlayer()
        self.settingpage = SettingPage(self.bgmplayer)
        self.helppage = HelpPage()
        self.nowmap = 1
        self.map = [None for i in range(4)]
        for i in range(1, 4):
            self.map[i] = MapPage(self.player, i)
        self.chatboxes = {
            "Seer": ChatBox.ChatBox("Seer"),
            "Cornifer": ChatBox.ChatBox("Cornifer"),
        }
        self.shoppage = ShopPage(self.player)
        upgradeCharacter.reset()
        difficultyController.reset()
        listeners = [self.menu]
        events = []

    def AddEvent(self, event):
        events.append(event)

    def update(self):
        global events, listeners
        loadevents = pygame.event.get()
        for event in loadevents:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                self.AddEvent(event)

        for i in range(len(listeners)):
            listener = listeners[i]
            # show scenes
            if isinstance(listener, Scene):
                listener.show(self.window)

            # deal with scenes
            if (isinstance(listener, MapPage)) and (i == len(listeners) - 1):
                listener.move()

        # handle events
        while len(events) > 0:
            event = events.pop(0)
            listener = listeners[-1]
            value = listener.handle(event)
            if value != None:
                if value == "EnterMap":
                    print("EnterMap")
                    listeners = [self.map[self.nowmap]]
                    self.bgmplayer.switch("Map" + str(self.nowmap))
                elif value == "EnterSetting":
                    print("EnterSetting")
                    listeners = [self.settingpage]
                elif value == "EnterHelp":
                    print("EnterHelp")
                    listeners = [self.helppage]
                elif (value == "EnterMenufromSettings") or (
                    value == "EnterMenufromHelp"
                ):
                    listeners = [self.menu]
                elif value == "EnterMenufromMap":
                    self.bgmplayer.switch("Menu")
                    listeners = [self.menu]
                elif (isinstance(value, tuple)) and (value[0] == "EnterChat"):
                    listeners.append(
                        self.chatboxes[value[1]]
                    )  # ChatBox 的渲染应该在最后
                    print("EnterChat")
                elif (isinstance(value, tuple)) and (value[0] == "EndChat"):
                    listeners.remove(self.chatboxes[value[1]])
                    print("EndChat")
                elif (isinstance(value, tuple)) and (value[0] == "EnterTeleport"):
                    if (value[1] == 4) or (value[1] == 5):
                        self.nowmap += 1
                    else:
                        self.nowmap -= 1
                    if self.nowmap == 0:
                        self.map[0] = MapPage(self.player, 0)
                    listeners = [self.map[self.nowmap]]
                    self.map[self.nowmap].reborn(self.nowmap)
                    self.bgmplayer.switch("Map" + str(self.nowmap))
                    self.player.Rect.x = self.player.Rect.y = 0
                elif value == "EnterShop":
                    listeners.append(self.shoppage)
                elif value == "QuitShop":
                    listeners.remove(self.shoppage)
                elif (isinstance(value, tuple)) and (value[0] == "EnterBattle"):
                    print("EnterBattle")
                    if value[1] != "Boss":
                        self.bgmplayer.switch("Fight")
                    else:
                        self.bgmplayer.switch("BossFight")
                    if (value[1] == "Enemy1") or (value[1] == "Enemy6"):
                        status = battleController.main(Level=1)
                    elif value[1] == "Enemy2":
                        status = battleController.main(Level=2)
                    elif value[1] == "Enemy3":
                        status = battleController.main(Level=3)
                    elif value[1] == "Enemy0":
                        status = battleController.main(Level=0)
                    elif value[1] == "Boss":
                        status = battleController.main(Level=4)
                    elif value[1] == "Enemy5":
                        ran = random.randint(0, 1)
                        if ran == 0:
                            status = battleController.main(Level=1)
                        else:
                            status = battleController.main(Level=3)
                    if status == "Lose":
                        for listener in listeners:
                            if isinstance(listener, MapPage):
                                listener.reborn(self.nowmap)
                                listeners = [listener]
                    elif status == "Win":
                        if value[1] == "Enemy1":
                            for listener in listeners:
                                if isinstance(listener, MapPage):
                                    listener.isdead[0] = True
                            self.player.money += random.randint(30, 40)
                        elif value[1] == "Enemy6":
                            for listener in listeners:
                                if isinstance(listener, MapPage):
                                    listener.isdead[1] = True
                            self.player.money += random.randint(40, 50)
                        elif value[1] == "Enemy5":
                            for listener in listeners:
                                if isinstance(listener, MapPage):
                                    listener.isdead[0] = True
                            self.player.money += random.randint(35, 45)
                        elif value[1] == "Enemy2":
                            for listener in listeners:
                                if isinstance(listener, MapPage):
                                    listener.isdead[2] = True
                            self.player.money += random.randint(50, 60)
                        elif value[1] == "Enemy3":
                            for listener in listeners:
                                if isinstance(listener, MapPage):
                                    listener.isdead[0] = True
                            self.player.money += random.randint(80, 90)
                        elif value[1] == "Enemy0":
                            for listener in listeners:
                                if isinstance(listener, MapPage):
                                    listener.isdead[1] = True
                            self.player.money += random.randint(90, 100)
                        elif value[1] == "Boss":
                            for listener in listeners:
                                if isinstance(listener, MapPage):
                                    listener.isdead[0] = True
                            self.player.money += random.randint(120, 130)
                        self.map[self.nowmap].freshnpc(self.nowmap)
                    self.bgmplayer.switch("Map" + str(self.nowmap))

    def render(self):
        pygame.display.flip()
