from player_code import player

import player_code
import pygame
# import collion
# from collion import group1
# from collion import group2


def tuple_sub(a, b):
    return (a[0] - b[0], a[1] - b[1])

def tuple_mul(a, b):
    return (a[0] * b, a[1] * b)

def tuple_min(a, b):
    return (min(a[0], b[0]), min(a[1], b[1]))

def tuple_max(a, b):
    return (max(a[0], b[0]), max(a[1], b[1]))

class SceneLike():  # 场景的类，管理障碍物、角色、地图背景的描绘、刷新等
    def __init__(self, p_rect,width,height,x=0,y=0):
         super().__init__()
         self.window_scale=(1200,700)
         self.map_range=(width,height)
         self.prect=p_rect
         self.rect=pygame.Rect((x,y,width,height))
         self.len=(0,0)
         self.judge=0
    def update(self, gamer):
        self.prect=pygame.Rect(gamer.imgstate.rect.x+gamer.stepx,gamer.imgstate.rect.y+gamer.stepy,gamer.imgstate.width,gamer.imgstate.height)
    def update_camera(self):
        if self.judge==0:
            xs=self.rect.x
            ys=self.rect.y
            self.camera = tuple_sub(self.prect.center,tuple_mul(self.window_scale,0.5))
            left_top = (0, 0)  
            right_down = tuple_sub(self.window_scale,self.map_range)
        
            (self.rect.x,self.rect.y)=(self.rect.x-self.camera[0],self.rect.y-self.camera[1])

            
            (self.rect.x,self.rect.y) = tuple_max(right_down, self.rect)
            (self.rect.x,self.rect.y) = tuple_min(left_top, self.rect)

            self.len=(self.rect.x-xs,self.rect.y-ys)
        else:
             self.camera=(0,0)
             self.len=(0,0)



