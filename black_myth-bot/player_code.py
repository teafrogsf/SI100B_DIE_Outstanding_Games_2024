import pygame
import animation
from animation import spirit_show_manager
import hitbox

class Player():
    def __init__(self,x=600,y=400,scale=1.5):
        self.run=animation.Animation("2.10/2.101/run副本/run",scale=scale)#跑步动画实例
        self.idle=animation.Animation("2.10/2.101/idle/idle",scale=scale)#站立动画实例
        self.jab=animation.Animation("2.10/2.101/jab/jab",scale=scale,ani_spd=40)# 轻拳动画实例
        self.stagger=animation.Animation("2.10/2.101/stagger/stagger",scale=scale,ani_spd=50)
        self.state_dict={
            "idle":{"status":0,"project":self.idle},
            "normal_move":{"status":0,"project":self.run},             
            "jab":{"status":0,"project":self.jab},
            "stagger":{"status":0,"project":self.stagger}
        }
        self.imgstate=animation.Spirit_state(self.idle.ani_img,x,y,z=9)#角色图形性质实例
        self.imgstate.width,self.imgstate.height=45,60
        spirit_show_manager.add_spirit(self.imgstate)

        self.state='idle'#角色行动状态
        self.rul_state='off'#时停状态
        self.state_occ='free'#事件占用状态
        self.status={"health":9,"mp":9,"time_energy":9,"time":600}#角色状态
        #时间相关
        self.rul_time=0#时间能量的恢复检查
        #
        self.stepx=0
        self.stepy=0
        

        self.direc='u'

        self.skill_state=None#确定现在是在释放什么技能

        self.jabhitbox=hitbox.Hitbox(30,0,40,60,"jab",2)
        self.windpunch_hitbox=hitbox.Hitbox(80,0,120,50,"windpunch",2)
        self.defaulthitbox=hitbox.Hitbox(0,0,0,0,"default",0)
        self.hurthitbox=hitbox.Hitbox(0,0,35,35,"hurt",0)
        self.hurt_admit=True 
        self.hurt_state=False

        self.hitboxes=hitbox.Hitboxes()
        self.hitboxes.add(self.jabhitbox)
        self.hitboxes.add(self.windpunch_hitbox)
        self.hitboxes.add(self.defaulthitbox)
        self.money=10
        self.skill_hitbox_dict={"windpunch":{0:self.windpunch_hitbox, 1:self.jabhitbox,"Ani":self.jab},"sprint":{0:self.defaulthitbox, 1:self.defaulthitbox,"Ani":None}}
    #更新角色状态词典函数
    def state_update(self):
       for k,v in self.state_dict.items():
           if self.state==k:
               v["status"]=1
           else:
               v["status"]=0
    #非战斗移动函数
    def normal_move(self,events):
        keys_pressed = pygame.key.get_pressed()  
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.event.key == pygame.K_a:
                    self.stepx=-8
                    self.stepy=0
                    self.run.direc="l"
                elif event.event.key == pygame.K_d:
                    self.stepx=8
                    self.stepy=0
                    self.run.direc="r"
                elif event.event.key == pygame.K_w:
                    self.stepy=-8
                    self.stepx=0
                    self.run.direc="u"
                elif event.event.key== pygame.K_s:
                    self.stepy=8
                    self.stepx=0
                    self.run.direc="d"         
        if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_d] or keys_pressed[pygame.K_s] or keys_pressed[pygame.K_w]:
            self.run.start_animation()
        else:
            self.stepx=0
            self.stepy=0
            self.run.stop_animation()
        self.run.update()
        self.direc=self.run.direc
        self.imgstate.image=self.run.ani_img
   #站立函数
    def f_idle(self):
       self.stepx,self.stepy=0,0
       self.idle.start_animation()
       self.idle.update()
       self.idle.direc=self.direc
       self.imgstate.image=self.idle.ani_img
   #轻拳函数
    def f_jab(self):
       self.stepx,self.stepy=0,0
       self.jab.direc=self.direc
       self.jab.start_animation()
       if self.jab.update_t(1):
           self.jabhitbox.rect=None
           self.state_occ="free"
       else:
           self.state_occ='busy'
           self.imgstate.image=self.jab.ani_img
           if self.skill_state == None:
                if self.jab.indices[self.direc]>=3 and self.jab.indices[self.direc]<=8:
                    self.jabhitbox.creat(self)
    def f_stagger(self,events):
        keys_pressed = pygame.key.get_pressed()  
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.event.key == pygame.K_a:
                    self.stepx=-2
                    self.stepy=0
                    self.run.direc="l"
                elif event.event.key == pygame.K_d:
                    self.stepx=2
                    self.stepy=0
                    self.run.direc="r"
                elif event.event.key == pygame.K_w:
                    self.stepy=-2
                    self.stepx=0
                    self.run.direc="u"
                elif event.event.key== pygame.K_s:
                    self.stepy=2
                    self.stepx=0
                    self.run.direc="d"         
        if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_d] or keys_pressed[pygame.K_s] or keys_pressed[pygame.K_w]:
            self.run.start_animation()
        else:
            self.stepx=0
            self.stepy=0
        self.stagger.direc=self.direc
        self.stagger.start_animation()
        if self.stagger.update_t(1):
            self.state_occ="free"
            self.hurt_state=False
        else:
            self.state_occ='busy'
            self.imgstate.image=self.stagger.ani_img
    def skill_check(self):
       if self.skill_state=="windpunch":
           self.jab.ani_spd=100
           self.f_jab()
           self.jab.ani_spd=40
       if self.skill_state=="sprint":
            self.state_occ='busy'
            self.run.direc=self.direc
            self.run.start_animation()
            self.imgstate.image=self.run.ani_img
            self.run.update()

    def rul_check(self):#时间能量的减少和恢复
        if self.status["time_energy"]==0:
            self.rul_state="off"
        if self.rul_state=="off":
          if self.status["time_energy"]<4:
              if pygame.time.get_ticks()-self.rul_time>=600:
                  self.rul_time=pygame.time.get_ticks()
                  self.status["time_energy"]+=1
          elif self.status["time_energy"]<6:
              if pygame.time.get_ticks()-self.rul_time>=1000:
                  self.rul_time=pygame.time.get_ticks()
                  self.status["time_energy"]+=1
          elif self.status["time_energy"]<9:
              if pygame.time.get_ticks()-self.rul_time>=2000:
                  self.rul_time=pygame.time.get_ticks()
                  self.status["time_energy"]+=1
        if self.rul_state=="on":
          if self.status["time_energy"]>=0:
              if pygame.time.get_ticks()-self.rul_time>=1000:
                  self.rul_time=pygame.time.get_ticks()
                  self.status["time_energy"]-=1
    def refresh(self):
        if self.hurt_admit:
            self.hurthitbox.creat(player)
        else:
            self.hurthitbox.vanish()
        self.rul_check()
        for v in self.status.values():
            if v<0:
                v=0
        self.status["mp"]=9-self.status["time_energy"]
        if self.status["health"]<=0:
            self.status["time"]-=60
            self.status["health"]=9

    def hurt_check(self,hitboxes,events):
        if self.hurt_admit:
            a=hitboxes.list_listen(self.hurthitbox.rect)
            if self.hurt_state==False:
                if a[0]:
                    pass
                else:
                    self.hurt_state=True
                    self.status["health"]-=a[1]
        if self.hurt_state:
            self.f_stagger(events)
player=Player()


                