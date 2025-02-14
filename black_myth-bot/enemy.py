import animation
from animation import spirit_show_manager
import base
import pygame
from mapsetting import map_manager
import entity
import random
import hitbox
from player_code import player
import bullet

class Enemy(entity.EntityLike):
    def __init__(
            self,base_name,x=800,y=-1000,scale=3,
            hatred_range=500,c_direc_time=550,
            speed=4,health=30,attack_hitbox=[20,-5,55,70,2],
            bar_y=7
            ):
        

        self.attack_hitbox=hitbox.Hitbox(attack_hitbox[0],attack_hitbox[1],attack_hitbox[2],attack_hitbox[3],"attack",attack_hitbox[4])
        self.attack_time=pygame.time.get_ticks()

        self.direc="d"
        self.direc_time=pygame.time.get_ticks()
        self.c_direc_time=c_direc_time

        self.state="normal"
        self.act_state="idle"
        self.hurt_state=False
        self.death_state=False

        self.stepx,self.stepy=0,0
        self.speed=speed

        self.health=health
        self.max_health=health

        self.bar_y=bar_y

        self.hatred_range=hatred_range

        # 创建一个红色的 Surface 对象
        self.red_bar= pygame.Surface((100,7))
        self.red_bar.fill((255, 0, 0))  # RGB for red

        # 使用 Surface 对象创建 Spirit_state 的实例
        self.red_bar_spirit = animation.Spirit_state(self.red_bar,2000,2000,z=10)
        spirit_show_manager.add_spirit(self.red_bar_spirit)
    def f_idle(self):
        self.act_state="idle"
        self.stepy,self.stepx=0,0
        self.idle.start_animation()
        self.idle.update()
        self.imgstate.image=self.idle.ani_img
    def f_hurt(self):
        self.stepx,self.stepy=0,0
        self.hurt.direc=self.direc
        self.hurt.start_animation()
        if self.hurt.update_t(2):
            self.hurt_state=False
            self.hurt.stop_animation()
        else:
            self.imgstate.image=self.hurt.ani_img
    def f_death(self,manager):
        self.stepx,self.stepy=0,0
        self.death.direc=self.direc
        self.death.start_animation()
        if self.death.update_t(1):
            player.money+=1
            manager.delet_enemy(self)
            self.death.stop_animation()
        else:
            self.imgstate.image=self.death.ani_img
    def draw(self,map_name):
        self.ori_loc.x+=map_manager.dict[map_name]["camera"].len[0]
        self.ori_loc.y+=map_manager.dict[map_name]["camera"].len[1]
        self.imgstate.show_j(self.stepx+map_manager.dict[map_name]["camera"].len[0],self.stepy+map_manager.dict[map_name]["camera"].len[1])
    def face(self,rect):
        now=pygame.time.get_ticks()
        if now-self.direc_time>=self.c_direc_time:
            self.direc_time=pygame.time.get_ticks()
            (x,y)=base.relative_loc([self.imgstate.rect.center[0],self.imgstate.rect.center[1]],[rect.center[0],rect.center[1]])
            if x==0:
                self.direc="d" if y>0 else "u"
            elif y==0:
                self.direc="l" if x>0 else "r"
            else:
                if abs(x)>=abs(y) :
                        if random.randint(1,3)==1:
                            self.direc="d" if y>0 else "u"
                        else:
                            self.direc="l" if x>0 else "r"
                elif abs(x)<abs(y):
                        if random.randint(1,3)==1:
                            self.direc="l" if x>0 else "r"
                        else:
                            self.direc="d" if y>0 else "u"
    def collion_show(self,map_name):
          can=map_manager.dict[map_name]["entity_group"].listen(self)
          if can[0]==False:
               return False
          else:
               self.stepx,self.stepy=can[1],can[2]
               return True
    def direc_update(self):
        self.walk.direc=self.direc
        self.attack.direc=self.direc
        self.hurt.direc=self.direc
        self.idle.direc=self.direc
    def stop_movement(self):
        self.stepx,self.stepy=0,0
    def check_collision(self, rect):
        # 使用pygame的内置函数来检测两个矩形是否发生碰撞
        return self.imgstate.rect.colliderect(rect)
    
    def death_judge(self):
        if self.health<=0:
            self.death_state=True
        if self.health>0:
            self.death_state=False
    def draw_health_bar(self):
        # 计算当前血条宽度
        ratio = self.health / self.max_health
        current_health_width = int(self.imgstate.rect.width*ratio)
        self.red_bar_spirit.rect.x,self.red_bar_spirit.rect.y=self.imgstate.rect.x,self.imgstate.rect.y - self.bar_y
        if current_health_width<=0:
            current_health_width=0
        image = pygame.Surface((current_health_width ,7))
        image.fill((255, 0, 0))  # RGB for red
        self.red_bar_spirit.image=image
        self.red_bar_spirit.show_j()
    def hurt_judge(self,hitboxes):
        if hitboxes.list_listen(self.imgstate.rect)[0]==False:
            if self.hurt_state==False:
                self.health-=hitboxes.list_listen(self.imgstate.rect)[1]
                self.hurt_state=True
class Long_range_enemy(Enemy):
    def __init__(self,base_name,map_name,bul_name="EyeFireRed",x=800,y=-1000,scale=2,
            hatred_range=1000,c_direc_time=550,
            speed=4,health=3,attack_hitbox=[20,-5,55,70,2],bar_y=-100):
        super().__init__(base_name,x,y,scale,hatred_range,c_direc_time,speed,health,attack_hitbox,bar_y)

        self.bullets=bullet.Bul_manager(map_name,bul_name)
        self.idle=animation.Animation_Simple(f"2.12/{base_name}/idle/idle",scale=scale,ani_spd=110)
        self.attack=animation.Animation_Simple(f"2.12/{base_name}/attack/attack",scale=scale,ani_spd=60)
        self.hurt=animation.Animation_Simple(f"2.12/{base_name}/hurt/hurt",scale=scale,ani_spd=200)
        self.death=animation.Animation_Simple(f"2.12/{base_name}/death/death",scale=scale,ani_spd=150)

        self.imgstate=animation.Spirit_state(self.idle.ani_img,x,y,z=9)
        spirit_show_manager.add_spirit(self.imgstate)

        self.ori_loc=pygame.Rect((x,y,self.imgstate.width,self.imgstate.height))
        self.hurt_hitbox=hitbox.Hitbox(0,0,43,43,"fire eye",1)
        self.direc="d"
        self.stepx,self.stepy=0,0
    def hurt_judge(self,hitboxes):
        if hitboxes.list_listen(self.hurt_hitbox)[0]==False:
            if self.hurt_state==False:
                self.health-=hitboxes.list_listen(self.hurt_hitbox.rect)[1]
                self.hurt_state=True
    def f_attack(self):
        self.attack.start_animation()
        if self.attack.update_t(1):
            self.attack.stop_animation()
            self.act_state=None
        else:
            self.imgstate.image=self.attack.ani_img
            if self.attack.indice==17:
                self.bullets.random_release(self)
    def attack_judge(self):
        if self.act_state !="attack":
          if self.bullets.ran_rel_judge():
             self.act_state="attack"
    def judge(self,rect,gamestate,hitboxes,manager):
        self.hurt_hitbox.creat(self)
        self.death_judge()
        self.hurt_judge(hitboxes)
        self.bullets.update(player)
        if self.death_state:
            self.f_death(manager)
        else:
            if self.hurt_state and self.act_state != "attack":
                    self.f_hurt()
            else:
                if gamestate=="battle":
                        if base.distance([self.imgstate.rect.x,self.imgstate.rect.y],[rect.x,rect.y])<self.hatred_range:
                            self.state="attack"
                        else:
                            self.state="normal"
                else:
                    self.state="normal"
                if self.state=="normal":
                    self.f_idle()
                elif self.state=="attack":
                    self.attack_judge()
                    if self.act_state=="attack":
                        self.f_attack()

class Short_range_enemy(Enemy):
    def __init__(self,base_name,map_name,x=800,y=-1000,scale=3,
            hatred_range=500,c_direc_time=550,
            speed=4,health=15,attack_hitbox=[20,-5,55,70,2],bar_y=7):
        super().__init__(base_name,x,y,scale,hatred_range,c_direc_time,speed,health,attack_hitbox,bar_y)
        self.walk=animation.Animation(f"2.12/{base_name}/walk/walk",scale=scale,ani_spd=100)
        self.attack=animation.Animation(f"2.12/{base_name}/attack/attack",scale=scale,ani_spd=110)
        self.hurt=animation.Animation(f"2.12/{base_name}/hurt/hurt",scale=scale,ani_spd=150)
        self.idle=animation.Animation(f"2.12/{base_name}/idle/idle",scale=scale,ani_spd=110)
        self.death=animation.Animation(f"2.12/{base_name}/death/death",scale=scale,ani_spd=130)
        self.imgstate=animation.Spirit_state(self.idle.ani_img,x,y,z=9)
        spirit_show_manager.add_spirit(self.imgstate)
        self.ori_loc=pygame.Rect((x,y,self.imgstate.width,self.imgstate.height))
    def collion_avoid(self,now_rect):
        m=now_rect.x-self.imgstate.rect.x
        n=now_rect.y-self.imgstate.rect.y
        if self.imgstate.rect.colliderect(now_rect) :
            return [True,(-m/5,-n/5),(m/5,n/5)]
        else :
            return [False,(0,0),(0,0)]
    def pursuing(self,rect):
        self.act_state="walk"
        speed=random.randint(self.speed-1,self.speed+1)
        self.face(rect)
        self.walk.direc=self.direc
        if self.direc=="l":
            self.stepx=-speed
            self.stepy=0
        elif self.direc=="r":
            self.stepx=speed
            self.stepy=0
        elif self.direc=="u":
            self.stepx=0
            self.stepy=-speed
        elif self.direc=="d":
            self.stepx=0
            self.stepy=speed
        self.walk.start_animation()
        self.walk.update()
        self.imgstate.image=self.walk.ani_img
    def f_attack(self):
       self.stepx,self.stepy=0,0
       self.attack.direc=self.direc
       self.attack.start_animation()
       if self.attack.update_t(1):
           self.attack.stop_animation()
           self.act_state=None
           self.attack_hitbox.vanish()
       else:
            self.act_state="attack"
            self.imgstate.image=self.attack.ani_img
            if self.attack.indices[self.direc]>=5 and self.attack.indices[self.direc]<=6:
                    self.attack_hitbox.creat(self)
    def attack_judge(self,gamer=player):
        now=pygame.time.get_ticks()
        if now-self.attack_time>=random.randint(2000,5000):
            if base.distance((self.imgstate.rect.x,self.imgstate.rect.y),(player.imgstate.rect.x,player.imgstate.rect.y))<100:
                self.attack_time=pygame.time.get_ticks()
                return True
        return False

    def turn_round(self):
        self.direc_time=pygame.time.get_ticks()
        if self.direc=="u":
            self.direc="r"
        elif self.direc=="d":
            self.direc="l"
        elif self.direc=="l":
            self.direc="u"
        elif self.direc=="r":
            self.direc="d"
    def turn_total(self):
        self.direc_time=pygame.time.get_ticks()
        if self.direc=="u":
            self.direc="d"
        elif self.direc=="d":
            self.direc="u"
        elif self.direc=="l":
            self.direc="r"
        elif self.direc=="r":
            self.direc="l"        
    def judge(self,rect,gamestate,hitboxes,manager):
        self.death_judge()
        self.hurt_judge(hitboxes)
        if self.death_state:
            self.f_death(manager)
            self.attack_hitbox.vanish()
        else:
            if self.hurt_state and self.act_state != "attack":
                    self.f_hurt()
            else:
                if gamestate=="battle":
                        if base.distance([self.imgstate.rect.x,self.imgstate.rect.y],[rect.x,rect.y])<self.hatred_range:
                            self.state="attack"
                        else:
                            self.state="normal"
                else:
                    self.state="normal"
                if self.state=="normal":
                    self.direc_update()
                    if self.check_collision(self.ori_loc):
                        self.f_idle()
                    else:
                        self.pursuing(self.ori_loc)
                elif self.state=="attack":
                    if self.attack_judge():
                        self.act_state="attack"
                    if self.act_state=="attack":
                        self.f_attack()
                    else:
                        self.pursuing(player.imgstate.rect)

class Enemy_manager():
    def __init__(self,map_name,class_mode,name,num=5):
        self.enemies = []
        self.hitboxes=hitbox.Hitboxes()
        self.buls=[]
        self.bulhit=[]
        self.map=map_name
        self.num=num
        self.name=name
        self.mode=class_mode
        self.count=True
        self.count2=True
    def add_enemy(self, enemy):
        self.enemies.append(enemy)
        self.hitboxes.add_list(enemy.attack_hitbox)
    def update_bullet(self):
        for x in self.bulhit:
           if x in self.hitboxes.list:
              self.hitboxes.list.remove(x)
        buls=[]
        for i in self.enemies:
            buls+=i.bullets.buls
            for j in i.bullets.buls:
                if j not in self.buls:
                    self.buls.append(j)
        for i in self.bulhit:
            if i not in buls:
                self.bulhit.remove(i)
        for i in self.buls:
            if i.hitbox not in self.bulhit:
                self.bulhit.append(i.hitbox)
        for x in self.bulhit:
           if x not in self.hitboxes.list:
              self.hitboxes.list.append(x)

    def delet_enemy(self,enemy):
        self.enemies.remove(enemy)
    def update_enemies(self, player,map_name,gamestate):
        if map_name==self.map:
            if len(self.enemies)<self.num:
                if random.randint(1,10)==1:
                    self.add_enemies(map_manager.dict[map_name]["map"].battle_rect)
            if player.rul_state=="off":
                for enemy in self.enemies:
                    enemy.judge(player.imgstate.rect,gamestate,player.hitboxes,self)
                    if player.hurthitbox.rect!=None:
                      if enemy.check_collision(player.hurthitbox.rect):
                            enemy.stop_movement()
                    else:
                        if enemy.check_collision(player.imgstate.rect):
                            enemy.stop_movement()
                # 检测敌人之间的碰撞
                for i, enemy_i in enumerate(self.enemies):
                    if isinstance(enemy_i,Short_range_enemy):
                        if enemy_i.collion_show(map_name):
                            enemy_i.turn_round()
                        for enemy_j in self.enemies[i + 1:]:
                            can=enemy_j.collion_avoid(enemy_i.imgstate.rect)
                            if can[0]:
                            # 这里处理敌人之间碰撞的逻辑，例如反弹或停止
                                (enemy_i.stepx,enemy_i.stepy)=can[2]
                                (enemy_j.stepx,enemy_j.stepy)=can[1]
                                enemy_i.turn_round()
                                enemy_j.turn_round()
                                break
            else:
                for enemy in self.enemies:
                    enemy.stop_movement()
            self.draw_enemies(map_name)
    def update_enemies_limit(self, player,map_name,gamestate,limit):
        if map_name==self.map:
            if self.count:
               for i in range(0,limit):
                    self.add_enemies(map_manager.dict[map_name]["map"].battle_rect)
                    self.count=False
            if player.rul_state=="off":
                for enemy in self.enemies:
                    enemy.judge(player.imgstate.rect,gamestate,player.hitboxes,self)
                    if player.hurthitbox.rect!=None:
                      if enemy.check_collision(player.hurthitbox.rect):
                            enemy.stop_movement()
                    else:
                        if enemy.check_collision(player.imgstate.rect):
                            enemy.stop_movement()
                # 检测敌人之间的碰撞
                for i, enemy_i in enumerate(self.enemies):
                    if isinstance(enemy_i,Short_range_enemy):
                        if enemy_i.collion_show(map_name):
                            enemy_i.turn_round()
                        for enemy_j in self.enemies[i + 1:]:
                            can=enemy_j.collion_avoid(enemy_i.imgstate.rect)
                            if can[0]:
                            # 这里处理敌人之间碰撞的逻辑，例如反弹或停止
                                (enemy_i.stepx,enemy_i.stepy)=can[2]
                                (enemy_j.stepx,enemy_j.stepy)=can[1]
                                enemy_i.turn_round()
                                enemy_j.turn_round()
                                break
            else:
                for enemy in self.enemies:
                    enemy.stop_movement()
            self.draw_enemies(map_name)
    def draw_enemies(self, map_name):
        for enemy in self.enemies:
            if isinstance(enemy,Short_range_enemy):
                enemy.draw_health_bar()
            if isinstance(enemy,Long_range_enemy):
                enemy.bullets.draw()
            enemy.draw(map_name)
    def draw_hitboxes(self,screen):
        for i in self.enemies:
            try:
                  pygame.draw.rect(screen, (128,0, 255), i.attack_hitbox.rect,2)
            except:
                pass
    def add_enemies(self,rect):
        x1=random.randint(rect.x+100,rect.x+rect.width-300)
        y1=random.randint(rect.y+100,rect.y+rect.height-500)
        self.add_enemy(self.mode(self.name,self.map,x=x1,y=y1))
    


Skeleton=Enemy_manager("tutoral",Short_range_enemy,"skeleton")
map_manager.dict["tutoral"]["hitboxes"]=[Skeleton.hitboxes]

Dark=Enemy_manager("tutoral",Long_range_enemy,"dark",num=2)
map_manager.dict["tutoral"]["hitboxes"].append(Dark.hitboxes)

Skeleton2=Enemy_manager("boss",Short_range_enemy,"skeleton")
Dark2=Enemy_manager("boss",Long_range_enemy,"dark",num=2)
map_manager.dict["boss"]["hitboxes"]=[Skeleton2.hitboxes,Dark2.hitboxes]


# class Boss(Enemy):
#     def 
