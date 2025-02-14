import pygame, sys
from GameSettings import *
from Utility import Scene
import upgradeCharacter


class ShopPage(Scene):

    def __init__(self, player):
        self.player = player
        self.font = pygame.font.Font(FontSettings.FontPath, 36)

        self.tip_text = self.font.render("", True, WHITE)
        self.tip_rect = self.tip_text.get_rect()
        self.tip_rect.center = (ShopSettings.width // 2, ShopSettings.shop_y + 400)
        self.width = ShopSettings.width
        self.height = ShopSettings.height
        self.shop_x = ShopSettings.shop_x
        self.shop_y = ShopSettings.shop_y
        self.shop_rect = pygame.Rect(self.shop_x, self.shop_y, self.width, self.height)
        self.shop_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.shop_surface.fill(ShopSettings.shopbox_color)
        self.buytime = -1000

        self.card_cost = 40
        self.health_cost = 25
        self.sp_cost = 30
        self.spheal_cost = 50

    def show(self, window):
        self.window = window

        # 加载商品图标
        self.card_icon = pygame.image.load(r".\assets\card.png")
        self.card_icon = pygame.transform.scale(self.card_icon, (60, 50))
        self.health_icon = pygame.image.load(r".\assets\hp.png")
        self.health_icon = pygame.transform.scale(self.health_icon, (50, 70))
        self.sp_icon = pygame.image.load(r".\assets\sp.png")
        self.sp_icon = pygame.transform.scale(self.sp_icon, (60, 60))
        self.spheal_icon = pygame.image.load(r".\assets\spheal.png")
        self.spheal_icon = pygame.transform.scale(self.spheal_icon, (180, 60))

        # 定义商店界面文本
        self.store_text = self.font.render("商店", True, WHITE)
        self.store_rect = self.store_text.get_rect()
        self.store_rect.center = (self.width // 2 + 30, self.shop_y + 50)

        # 定义商品价格文本
        self.card_price_text = self.font.render(f"{self.card_cost} 吉欧", True, WHITE)
        self.card_price_rect = self.card_price_text.get_rect()
        self.card_price_rect.center = (self.width // 2 + 100, self.shop_y + 120)

        self.health_price_text = self.font.render(
            f"{self.health_cost} 吉欧", True, WHITE
        )
        self.health_price_rect = self.health_price_text.get_rect()
        self.health_price_rect.center = (self.width // 2 + 100, self.shop_y + 200)

        self.sp_price_text = self.font.render(f"{self.sp_cost} 吉欧", True, WHITE)
        self.sp_price_rect = self.sp_price_text.get_rect()
        self.sp_price_rect.center = (self.width // 2 + 100, self.shop_y + 280)

        self.spheal_price_text = self.font.render(
            f"{self.spheal_cost} 吉欧", True, WHITE
        )
        self.spheal_price_rect = self.spheal_price_text.get_rect()
        self.spheal_price_rect.center = (self.width // 2 + 100, self.shop_y + 360)

        window.blit(self.shop_surface, (self.shop_x, self.shop_y))
        window.blit(self.store_text, self.store_rect)
        window.blit(self.card_icon, (self.width // 2 - 100, self.shop_y + 90))
        window.blit(self.card_price_text, self.card_price_rect)
        window.blit(self.health_icon, (self.width // 2 - 100, self.shop_y + 170))
        window.blit(self.health_price_text, self.health_price_rect)
        window.blit(self.sp_icon, (self.width // 2 - 100, self.shop_y + 250))
        window.blit(self.sp_price_text, self.sp_price_rect)
        window.blit(self.spheal_icon, (self.width // 2 - 150, self.shop_y + 330))
        window.blit(self.spheal_price_text, self.spheal_price_rect)
        tim = pygame.time.get_ticks()
        if tim - self.buytime < 500:
            window.blit(self.tip_text, self.tip_rect)

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 鼠标左键点击
            self.card_icon_rect = self.card_icon.get_rect()
            self.card_icon_rect.topleft = (self.width // 2 - 100, self.shop_y + 150)

            self.health_icon_rect = self.health_icon.get_rect()
            self.health_icon_rect.topleft = (self.width // 2 - 100, self.shop_y + 250)

            mouse_pos = event.pos
            if self.card_icon_rect.collidepoint(
                mouse_pos
            ) or self.card_price_rect.collidepoint(mouse_pos):
                self.buytime = pygame.time.get_ticks()
                # 点击升级卡牌
                if self.player.money >= self.card_cost:
                    self.player.money -= self.card_cost
                    self.card_cost = int(self.card_cost * 1.2)
                    upgradeCharacter.addAllCardLevel(1)
                    self.tip_text = self.font.render("购买成功", True, WHITE)
                else:
                    self.tip_text = self.font.render("吉欧不足", True, WHITE)
            elif self.health_icon_rect.collidepoint(
                mouse_pos
            ) or self.health_price_rect.collidepoint(mouse_pos):
                self.buytime = pygame.time.get_ticks()
                # 点击提升血量上限
                if self.player.money >= self.health_cost:
                    self.player.money -= self.health_cost
                    self.health_cost = int(self.health_cost * 1.2)
                    upgradeCharacter.addMaxHP(10)
                    self.tip_text = self.font.render("购买成功", True, WHITE)
                else:
                    self.tip_text = self.font.render("吉欧不足", True, WHITE)
            elif self.sp_icon.get_rect().collidepoint(
                mouse_pos
            ) or self.sp_price_rect.collidepoint(mouse_pos):
                self.buytime = pygame.time.get_ticks()
                # 点击提升精力上限
                if self.player.money >= self.sp_cost:
                    self.player.money -= self.sp_cost
                    self.sp_cost = int(self.sp_cost * 1.2)
                    upgradeCharacter.addMaxSP(2)
                    self.tip_text = self.font.render("购买成功", True, WHITE)
                else:
                    self.tip_text = self.font.render("吉欧不足", True, WHITE)
            elif self.spheal_icon.get_rect().collidepoint(
                mouse_pos
            ) or self.spheal_price_rect.collidepoint(mouse_pos):
                self.buytime = pygame.time.get_ticks()
                # 点击增加精力恢复速度
                if self.player.money >= self.spheal_cost:
                    self.player.money -= self.spheal_cost
                    self.spheal_cost = int(self.spheal_cost * 1.2)
                    upgradeCharacter.addSPHeal(1)
                    self.tip_text = self.font.render("购买成功", True, WHITE)
                else:
                    self.tip_text = self.font.render("吉欧不足", True, WHITE)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "QuitShop"
