import pygame

# This is a dictionary that contains all the settings for the game.
# It allows you to easily change settings without having to change the code repeatedly.

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class WindowSettings:
    width = 1000
    height = 650
    title = "Hollow Knight"
    fps = 120


class MoveSettings:
    playerHeight = 70  # 人物高度
    playerWidth = 35  # 人物宽度
    speed = 4  # 人物移动速度
    gravity = 1200  # 重力加速度
    initialSpeed = 600  # 起跳初速度
    blockSize = 50  # 地图方块大小
    edgeDist = (
        4 * blockSize
    )  # 人物实际活动范围距离左右边界的距离（超过这个距离，就变成地图移动，人物不动）
    dashSpeed = 13  # 冲刺速度
    dashDuration = 200  # 冲刺持续时间 (ms)


class BgmSettings:
    defaultvolume = 0.5


class ChatBoxSettings:
    chatbox_color = (0, 0, 0, 128)  # 半透明黑色聊天框
    input_box_color = (0, 0, 0, 64)  # 半透明黑色输入框
    text_color = (255, 255, 255)  # 白色文字

    # 聊天框位置和大小
    chatbox_x = 100
    chatbox_y = 50
    chatbox_width = 800
    chatbox_height = 400

    # 输入框位置和大小
    input_box_x = chatbox_x
    input_box_y = chatbox_y + chatbox_height + 10
    input_box_width = chatbox_width
    input_box_height = 50


class ShopSettings:
    shop_x = 100
    shop_y = 50
    width = 800
    height = 400
    shopbox_color = (0, 0, 0, 128)  # 半透明黑色购买框


class FontSettings:
    FontPath = "C:\\Windows\\Fonts\\simsun.ttc"  # 华文宋体字体路径
