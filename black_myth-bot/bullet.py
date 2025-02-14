import animation
import pygame
import math
import hitbox
from mapsetting import map_manager
from player_code import player
import random
from animation import spirit_show_manager

class Bul:
    def __init__(self, base_name, shooter,scale=2, speedX=15, speedY=15,damage=1):
        self.direc="d"
        self.damage=damage
        self.ani = animation.Animation_Simple(f"2.17/EyeFireRed/bullet", scale=scale, ani_spd=100)
        self.ani.start_animation()
        self.imgstate = animation.Spirit_state(self.ani.ani_img,shooter.imgstate.rect.centerx,shooter.imgstate.rect.centery, z=9.4)
        spirit_show_manager.add_spirit(self.imgstate)
        self.stepx = speedX
        self.stepy = speedY
        self.last_update_time = pygame.time.get_ticks()
        self.update_rotation()
        self.hitbox=hitbox.Hitbox(0,0,min(self.imgstate.width,self.imgstate.height),min(self.imgstate.width,self.imgstate.height),"bullet",self.damage)
    def update_rotation(self):
        """ 根据速度矢量更新子弹的旋转角度 """
        angle = math.degrees(math.atan2(-self.stepy, self.stepx))  # 注意：y轴是反向的，所以需要取负
        self.imgstate.image = pygame.transform.rotozoom(self.ani.ani_img,angle, 1)
    def update(self,map_name):
        self.hitbox=hitbox.Hitbox(0,0,min(self.imgstate.width,self.imgstate.height),min(self.imgstate.width,self.imgstate.height),"bullet",self.damage)
        """ 更新子弹的位置和旋转 """
        self.hitbox.creat(self)
        self.ani.update() # 更新动画帧
        self.update_rotation()  # 更新旋转以匹配新的图像
        # 更新位置
        self.imgstate.rect.x+=self.stepx+map_manager.dict[map_name]["camera"].len[0]
        self.imgstate.rect.y+=self.stepy+map_manager.dict[map_name]["camera"].len[1]
    def collion_show(self,map_name):
          can=map_manager.dict[map_name]["entity_group"].listen(self)
          if can[0]==False:
               return False
          else:
               return True
class Bul_manager:
    def __init__(self,map_name,base_name,r=5,scale=2,rad_rel_t=10000,tar_rel_t=5000):
        self.buls=[]
        self.hitboxes=hitbox.Hitboxes()
        self.map=map_name
        self.base_name=base_name
        self.r=r
        self.scale=scale

        self.rad_rel_t=random.randint(rad_rel_t-5000,12000)
        self.rad_t=pygame.time.get_ticks()
        self.tar_rel_t=tar_rel_t
        self.tar_t=pygame.time.get_ticks()
    def update(self,player):
        for i in self.buls:
            if i.collion_show(self.map):
                self.delet(i)
            elif i.hitbox.rect!= None and player.hurthitbox.rect != None:
                if i.hitbox.rect.colliderect(player.hurthitbox.rect):
                    self.delet(i)
                else:
                  i.update(self.map)
            else:
                i.update(self.map)
    def ran_rel_judge(self):
        now=pygame.time.get_ticks()
        if now-self.rad_t>self.rad_rel_t:
            self.rad_t=now
            return True
        else:
            return False
    def draw(self):
        for i in self.buls:
            i.imgstate.show_j()
    def random_release(self,shooter):
        angle=random.randint(0,7)
        for i in range(1,random.randint(5,10)):
            angle+=random.randint(1,3)
            self.buls.append(Bul(self.base_name,shooter,scale=self.scale,speedX=self.r*math.cos(angle),speedY=self.r*math.sin(angle)))

    # def target_release(self):
    #     for i in range
    def delet(self,bul):
        bul.hitbox.vanish()
        self.buls.remove(bul)
