import pygame
from GameSettings import *


class Player:

    def __init__(self):
        # 图像设置
        self.facing = "right"
        self.frame = 0  # 人物运动到第几帧，一共4帧
        self.speed = MoveSettings.speed
        self.onJump = False
        self.isDashing = False
        self.dashSpeed = MoveSettings.dashSpeed  # 冲刺速度

        self.leftimg = [
            pygame.image.load(r".\assets\character\left1.png") for _ in range(4)
        ] + [pygame.image.load(r".\assets\character\left2.png") for _ in range(4)]
        self.rightimg = [
            pygame.image.load(r".\assets\character\right1.png") for _ in range(4)
        ] + [pygame.image.load(r".\assets\character\right2.png") for _ in range(4)]

        self.height = MoveSettings.playerHeight
        self.width = MoveSettings.playerWidth

        for i in range(8):
            self.leftimg[i] = pygame.transform.scale(
                self.leftimg[i], (self.width, self.height)
            )
            self.rightimg[i] = pygame.transform.scale(
                self.rightimg[i], (self.width, self.height)
            )
        self.img = self.rightimg[0]
        self.Rect = self.img.get_rect()
        self.dashLimg = pygame.image.load(r".\assets\character\left - dash.png")
        self.dashLimg = pygame.transform.scale(
            self.dashLimg, (self.width * 2.42, self.height * 0.83)
        )
        self.dashRimg = pygame.image.load(r".\assets\character\right - dash.png")
        self.dashRimg = pygame.transform.scale(
            self.dashRimg, (self.width * 2.42, self.height * 0.83)
        )

        # 属性设置
        self.money = 0

    def show(self, window):
        # 展示人物位置
        if self.isDashing:
            if self.facing == "left":
                window.blit(self.dashLimg, self.Rect.topleft)
            else:
                temprect = (
                    self.Rect.x - 1.42 * self.width,
                    self.Rect.y + 0.17 * self.height,
                )
                window.blit(self.dashRimg, temprect)
        else:
            window.blit(self.img, self.Rect)

        # 展示金币数量
        font = pygame.font.Font(FontSettings.FontPath, 30)
        text = font.render(
            str(self.money), True, WHITE
        )  # 抗锯齿: antialias = True, 文字更加平滑
        moneyimg = pygame.image.load(r".\assets\geo.png")
        moneyimg = pygame.transform.scale(moneyimg, (40, 40))
        window.blit(moneyimg, (20, 30))
        window.blit(text, (65, 35))
