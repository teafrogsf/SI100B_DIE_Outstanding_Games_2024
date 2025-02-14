import pygame
from animation import spirit_show_manager
import animation
import playui
class SKillUI(playui.Useable_ui):
    pass
    
class Skill():
   def __init__(self,ani_name,name,speed=0,rel_loc=-10,speedx=0,speedy=0,num=1,scale=1,z=20,mp=2):
       self.name=name
       self.ani=animation.Animation_Simple(ani_name,scale=scale)
       self.imgstate=animation.Spirit_state(self.ani.ani_img,2000,2000,z)
       spirit_show_manager.add_spirit(self.imgstate)
       self.direc='u'
       self.rel_loc=rel_loc

       self.speedx=speedx
       self.speedy=speedy
       self.speed=speed
       self.stepxy=(0,0)

       self.exist=False
       self.skill_release_num=num
       self.mp=mp
       # 预先创建所有方向的图像变体
       self.directions = {
            'u': 90,  # 向上是顺时针旋转90度
            'd': -90,  # 向下是逆时针旋转90度
            'l': 180,  # 向左是顺时针旋转180度
            'r': 0   # 向右不需要旋转
        }
       self.rotated_images = {}
       for d, angle in self.directions.items():
    # 对于每个方向，创建一个空列表来保存该方向的所有旋转图像
            rotated_image_list = []
            for image in self.ani.imglist:
                # 将图像根据对应的角度进行旋转，并添加到列表中
                rotated_image = pygame.transform.rotate(image, angle)
                rotated_image_list.append(rotated_image)
            # 将完成的旋转图像列表关联到对应的方向键
            self.rotated_images[d] = rotated_image_list
   def set_direction(self,gamer):
        """设置当前技能的方向和对应的图像"""
        self.direc=gamer.direc
        if self.direc in self.rotated_images:
            self.ani.imglist=self.rotated_images[self.direc] 

   def straight_release(self,gamer):
    self.set_direction(gamer)
    # 设置技能动画的初始位置基于角色的位置和方向
    if self.direc == "u":
        self.imgstate.rect.midbottom = gamer.imgstate.rect.midtop
        self.imgstate.rect.y -= self.rel_loc
        self.speedx=0
        self.speedy=-self.speed
    elif self.direc == "d":
        self.imgstate.rect.midtop = gamer.imgstate.rect.midbottom
        self.imgstate.rect.y += self.rel_loc
        self.speedx=0
        self.speedy=self.speed
    elif self.direc == "l":
        self.imgstate.rect.midright = gamer.imgstate.rect.midleft
        self.imgstate.rect.x -= self.rel_loc
        self.speedx=-self.speed
        self.speedy=0
    elif self.direc == "r":
        self.imgstate.rect.midleft= gamer.imgstate.rect.midright
        self.imgstate.rect.x += self.rel_loc
        self.speedx=self.speed
        self.speedy=0
    self.ani.start_animation()
    if self.ani.update_t(1):
        self.exist=False
    else:
        self.imgstate.image=self.ani.ani_img
   def sprint_release(self,gamer):
        self.set_direction(gamer)
        if self.direc=="l":
           (x_c,y_c)=(-self.speed,0)
        elif self.direc=="r":
           (x_c,y_c)=(self.speed,0)
        elif self.direc=="u":
           (x_c,y_c)=(0,-self.speed)
        elif self.direc=="d":
           (x_c,y_c)=(0,self.speed)
        self.stepxy=(x_c,y_c)
        self.ani.start_animation()
        if self.ani.update_t(1):
            self.exist=False
            self.stepxy=(0,0)
        else:
            pass
   def skill_release(self,gamer):
        self.imgstate.show_j()
        if self.skill_release_num==1:
           self.straight_release(gamer)
        elif self.skill_release_num==2:
            self.sprint_release(gamer)


class Skill_manager():
   def __init__(self):
       self.dict_s={}
       self.trigger_num=0
       self.defaultUI1=SKillUI("2.3/2.36/default",x=990,y=718)
       self.defaultUI2=SKillUI("2.3/2.36/default",x=1059,y=718)
       self.defaultUI3=SKillUI("2.3/2.36/default",x=1128,y=718)
       self.sprintUI=SKillUI("2.3/2.36/sprint",x=921,y=718)
       self.sprint=Skill("2.10/2.102/sprint/sprint","sprint",num=2,speed=20)
       self.trigger={0:{"sprint":{"skill":self.sprint,"ui":self.sprintUI,"status":"off"}},1:{},2:{},3:{}}
   def add_s(self,skill,skillui):
       self.dict_s[skill.name] = {"skill": skill, "ui": skillui, "status": "off"}
   def skill_select(self,name,number):
       if name in self.dict_s:
            # 根据提供的数字，更新self.trigger相应位置的值
            try:
                self.trigger[number][name] = self.dict_s[name]
                if number==1:
                  self.dict_s[name]["ui"].icon_state.rect.x=990
                  self.dict_s[name]["ui"].icon_state.rect.y=718
                elif number==2:
                  self.dict_s[name]["ui"].icon_state.rect.x=1059
                  self.dict_s[name]["ui"].icon_state.rect.y=718
                elif number==3:
                  self.dict_s[name]["ui"].icon_state.rect.x=1128
                  self.dict_s[name]["ui"].icon_state.rect.y=718
            except:
                print("技能数字错误")
   def skill_default(self,number):
       if number==1:
            self.trigger[1]["default"]={"skill":"error","ui":self.defaultUI1,"status":"off"}
       elif number==2:
            self.trigger[2]["default"]={"skill":"error","ui":self.defaultUI2,"status":"off"}
       elif number==3:
            self.trigger[3]["default"]={"skill":"error","ui":self.defaultUI3,"status":"off"}
   def skill_choose(self,events):
       for event in events:
            if event.type==pygame.KEYDOWN:
                if event.event.key==pygame.K_d:
                    self.trigger_num = 0 if self.trigger_num == 3 else self.trigger_num + 1
                    for k,v in self.trigger.items():
                        if k == self.trigger_num:
                            for value in v.values():
                                value["ui"].icon.indice=1
                        else:
                            for value in v.values():
                                value["ui"].icon.indice=0
                if event.event.key==pygame.K_a:
                    self.trigger_num = 3 if self.trigger_num == 0 else self.trigger_num - 1
                    for k,v in self.trigger.items():
                        if k == self.trigger_num:
                            for value in v.values():
                                value["ui"].icon.indice=1
                        else:
                            for value in v.values():
                                value["ui"].icon.indice=0
   def skill_unchoose(self):
       for v in self.trigger.values():
           for value in v.values():
                  value["ui"].icon.indice=0
   def refresh(self,gamer):
    # 获取所有的触发器编号
        trigger_numbers = self.trigger.keys()
        if gamer.rul_state=="off":
            for v in self.trigger.values():
                for value in v.values():
                    value["ui"].icon.indice=0
        for v in self.trigger.values():
           for value in v.values():
              value["ui"].icon_state.image=value["ui"].icon.ani_img
              value["ui"].icon_state.show_j()
        for k, v in self.dict_s.items():
            # 检查技能是否在任何一个触发器子字典中
            if not any(k in self.trigger[number] for number in trigger_numbers):
                v["status"] = "off"
                v["ui"].icon_state.x=2000
                v["ui"].icon_state.y=2000   
        for k,v in self.trigger.items():
            if v=={}:
                self.skill_default(k)
        


windpunch=Skill("2.10/2.102/windpunch/windpunch","windpunch",scale=3,mp=4)
windpunchUI=SKillUI("2.3/2.36/windpunch")

player_skill=Skill_manager()
player_skill.add_s(windpunch,windpunchUI)
player_skill.skill_select("windpunch",1)

            
               
       
   
       

           

           