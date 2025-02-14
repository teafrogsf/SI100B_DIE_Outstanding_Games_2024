from player_code import player
from skill import player_skill
import pygame
from mapsetting import map_manager
import entity

class Player_gather():
     def __init__(self):
        self.skill_con=0 #0则不在选技能，1则在选技能，2则在放技能
        self.playstate={"state":None,"rul_state":None,"state_occ":None,"skill_state":None}#存储玩家状态
     def collion_show(self,map_name):
          group=entity.collion_group()
          for k,v in map_manager.dict[map_name].items():
               if 'group' in k:
                    for i in v.list:
                        group.list.append(i)
          can=group.listen(player)
          if can[0]==False:
               player.imgstate.show_j(player.stepx+map_manager.dict[map_name]["camera"].len[0],player.stepy+map_manager.dict[map_name]["camera"].len[1])
               return False
          else:
               player.imgstate.show_j(can[1]+map_manager.dict[map_name]["camera"].len[0],can[2]+map_manager.dict[map_name]["camera"].len[1])
               return True
     def battle_state(self,map_name,player=player):
        if player.imgstate.rect.colliderect(map_manager.dict[map_name]["map"].battle_rect):
            return True
        else:
            return False
     def hurt_judge(self,map_name,events,player=player):
        for i in map_manager.dict[map_name]["hitboxes"]:
              player.hurt_check(i,events)
     def normal_act(self,events):
          global player
          if player.state_occ=="free":
               if player.stepx==0 and player.stepy==0:
                    player.state="idle"
               for event in events:
                    if event.type == pygame.KEYDOWN:
                         if event.event.key == pygame.K_a or event.event.key == pygame.K_d or event.event.key == pygame.K_w or event.event.key == pygame.K_s:
                              player.state="normal_move"
                         if event.event.key == pygame.K_j:
                              player.state="jab"
          if player.state=="jab":
                    player.f_jab()
          elif player.state=="normal_move":
                    player.normal_move(events)
          else:
                    player.f_idle()
     def battle_act(self,events):
          global player,player_skill
          if self.skill_con==2:
               for v in player_skill.trigger.values():
                    for k,value in v.items():
                         if k!="default":
                              if value["status"]=="on":
                                   if value["skill"].exist:
                                        player.rul_state="off"
                                        player.skill_state=k
                                        player.skill_hitbox_dict[value["skill"].name][0].creat(player)
                                        value["skill"].skill_release(player)
                                        (player.stepx,player.stepy)=value["skill"].stepxy
                                        player.skill_check()
                                   else:
                                        player.hurt_admit=True
                                        player.state="idle"
                                        self.skill_con=0
                                        player.skill_state=None
                                        player.state_occ="free"
                                        player.hitboxes.vanish()
                                        try:
                                             player.skill_hitbox_dict[value["skill"].name]["Ani"].refresh()
                                        except:
                                             pass
                                        value["status"]="off"
          if player.rul_state == 'off':
               if player.state!="skill":
                    if player.hurt_state==False:
                         self.normal_act(events)
                         for event in events:
                              if event.type == pygame.KEYDOWN:
                                   if player.status["time_energy"]>= 1:
                                        if event.event.key == pygame.K_LCTRL or event.event.key == pygame.K_RCTRL:
                                             player.rul_state = "on"
                                             player.stepx = 0
                                             player.stepy = 0
          elif player.rul_state == 'on':
               # Allow changing direction during time pause but do not move
               if self.skill_con==0:
                    for event in events:
                              if event.type == pygame.KEYDOWN:
                                   if event.event.key==pygame.K_TAB:
                                        self.skill_con=1
                                        for v in player_skill.trigger[0].values():
                                             v["ui"].icon.indice=1
                                   if event.event.key==pygame.K_k:
                                        self.skill_con=0
                                        player.rul_state='off'
                                   if event.event.key==pygame.K_a:
                                        player.direc="l"
                                   if event.event.key==pygame.K_d:
                                        player.direc="r"
                                   if event.event.key==pygame.K_w:
                                        player.direc="u"
                                   if event.event.key==pygame.K_s:
                                        player.direc="d"
                    for k,v in player.state_dict.items():
                         if v["status"]==1:
                              v["project"].indices[player.direc]=v["project"].indices[v["project"].direc]
                              v["project"].direc=player.direc
                              v["project"].ani_img=v["project"].imgdict[v["project"].direc][v["project"].indices[v["project"].direc]]
                              player.imgstate.image= v["project"].ani_img
               if self.skill_con==1:
                         player_skill.skill_choose(events)
                         for event in events:
                              if event.type==pygame.KEYDOWN:
                                   if event.event.key==pygame.K_k:
                                        self.skill_con=0
                                        player_skill.skill_unchoose()
                                   if event.event.key==pygame.K_j:
                                       for v in player_skill.trigger.values():
                                          for k,value in v.items():
                                                if k!="default":
                                                  if value["ui"].icon.indice==1:
                                                     if player.status["mp"]>=value["skill"].mp:
                                                            player.status["mp"]-=value["skill"].mp
                                                            value["skill"].exist=True
                                                            if value["skill"].name=="sprint":
                                                               player.hurt_admit=False
                                                            value["status"]= "on"
                                                            self.skill_con=2
                                                            player_skill.trigger_num=0
                                                            value["ui"].icon.indice=0
                                                            player.state="skill"

     def act_judge(self,events,gamestate,map_name):
          global player,player_skill,skill_choosing
          player.state_update()
          a=False
          if self.battle_state(map_name,player=player):
               a=True
          if gamestate =='normal':
               self.normal_act(events)
          if gamestate=='battle':
               self.hurt_judge(map_name,events)
               self.battle_act(events)
          player_skill.refresh(player)
          player.refresh()
          if player_gather.collion_show(map_name):
            map_manager.dict[map_name]["camera"].judge=1
          else:
            map_manager.dict[map_name]["camera"].judge=0
          return a
player_gather=Player_gather()
           
