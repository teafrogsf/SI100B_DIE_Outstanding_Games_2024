import pygame
import base
import sys
import animation
from animation import spirit_show_manager
from base import musicmanager

from npc import npc0,group0,npcimg

from mapsetting import map_manager

from enemy import Skeleton,Skeleton2,Dark,Dark2


from player_code import player
from player_gather import player_gather

import playui
from playui import uimanager

import dialog
from plot import piclist,piclist2
from chat import chatfunction1

from openai import OpenAI
from typing import List, Dict

from astart import startdef
from astart import shopdef
from astart import bagdef
from astart import stopdef
from astart import objectlist
from astart import baglist
from astart import prepare
from astart import deathdef
from astart import victorydef
from dialog import w1
from dialog import ppt
from mapsetting import doorgroup_tutoral

pygame.init()
def main():
   pygame.init()
   number=0
   screen = pygame.display.set_mode((1200,800))
    # 加载图标图像
   icon_image = npcimg
   pygame.display.set_icon(icon_image)

   death,deathbg,name ,start, prompt,continuegame,bag,stoptit,shop1,shop2,shop3,shoper,shopkuang,bagershow=prepare()
   wait=False
   gamestate='start'
   store=None

   

   touxiang = npcimg
   touxiang = pygame.transform.scale(touxiang,(110,110))
   map_name="tutoral"
   w1 = []
   text_input_box = dialog.TextInputBox(100, 100, 200, 50)
   user_input=''
   client = OpenAI(
      base_url='http://10.15.88.73:5003/v1',
      api_key='ollama',  # required but ignored
   )

   messages : List[Dict] = [
      {"role": "user", "content": "你不会好好说话，说话很高深莫测\
你是听说此地有第二使徒反叛的线索而前来调查的暗裔使徒，不知为何，突然陷入了时间的轮回中并且无法离开此区域，但由于身有神力，你还能在轮回中保持记忆。\
经过调查，你知道是作为武术家的主角因讨伐魔物，触发了第二使徒的恩宠，而让此区域陷入了时间的轮回。你在此处一边等待第二使徒来拯救他的魔物而现身，一边观察着触发轮回的主角能否成为打破轮回的天选者。\
若主角成为了天选者，则可将神器授予他，让他拥有天选之力而对抗第二使徒。你说话不能超过20字。"}
   ]
   for i in doorgroup_tutoral.list:
      if i.id ==185:
         i.map='boss'
   timebar=playui.Timebar()
   
   skeleton_number=4
   dark_number=5

   end_count1=False
   end_count2=False
   while True:
         screen.fill((0, 0, 0))
         event_que=base.Event_queue()
         event_que.fill()
         base.process(event_que.queue)
         if end_count1:
            if end_count2:
               gamestate="victory"
            else:
               gamestate="bad_end"
         
         if gamestate in ["victory","bad_end","start","death"]:
            musicmanager.play("menu")
         elif gamestate == "battle":
            musicmanager.play("battle")
         else:
            musicmanager.play("normal")
         if gamestate in ["stop","bag"]:
            musicmanager.pause()
         else:
            musicmanager.unpause()
         
         if gamestate=="death":
            deathdef(screen,death,deathbg)
            spirit_show_manager.sort_and_show(screen)
         elif gamestate=="victory":
            victorydef (screen,event_que,piclist2)
            spirit_show_manager.sort_and_show(screen)
         elif gamestate=="bad_end":
            victorydef (screen,event_que,piclist)
            spirit_show_manager.sort_and_show(screen)
            if len(piclist)==1:
               sys.exit()
         else:
            if gamestate != "stop" and gamestate != "bag":
               for i in event_que.queue:
                     if i.type == pygame.KEYDOWN:
                        if i.event.key == pygame.K_ESCAPE:
                           event_que.queue.remove(i)
                           store=gamestate
                           gamestate='stop'
            elif gamestate=='bag':
               gamestate=bagdef(event_que,screen,store,player.money,baglist,objectlist,gamestate,shop1,shop2,shop3,bagershow,shopkuang,player)
               spirit_show_manager.sort_and_show(screen)
            elif gamestate=='stop':
               gamestate=stopdef(event_que,screen,store,start,continuegame,bag,stoptit)
               spirit_show_manager.sort_and_show(screen)
            if gamestate=='shop':
               gamestate=shopdef(event_que,screen,"normal",player.money,objectlist,baglist,gamestate,shop1,shop2,shop3,shoper,shopkuang,player)
               spirit_show_manager.sort_and_show(screen)


            if gamestate=='start':
               gamestate=startdef(event_que,screen,name,start,prompt)
               spirit_show_manager.sort_and_show(screen)

            if gamestate=='fixdialog' or gamestate=='dialogchoice' or gamestate=='normal' or gamestate=='battle' or gamestate=='dialog':
                  if len(ppt)>0:
                     ppt[0].paint(screen,event_que)
                     if ppt[0].finished_writing:
                        ppt.pop(0)
                  (map_name,player.imgstate.rect.x,player.imgstate.rect.y)=map_manager.dict[map_name]["door"].listen(player,map_name,event_que)
                  map_manager.dict[map_name]["camera"].update(player)
                  map_manager.dict[map_name]["camera"].update_camera()
                  map_manager.dict[map_name]["map"].tile_show(map_manager.dict[map_name]["camera"].len[0],map_manager.dict[map_name]["camera"].len[1])

                  Skeleton.update_enemies(player,map_name,gamestate)
                  # Dark.update_enemies(player,map_name,gamestate)
                  # Dark.update_bullet()
                  Skeleton2.update_enemies_limit(player,map_name,gamestate,skeleton_number)
                  Dark2.update_enemies_limit(player,map_name,gamestate,dark_number)
                  Dark2.update_bullet()
                  if map_name=="boss":
                     if len(Skeleton2.enemies)==0 and len(Dark2.enemies)==0:
                       end_count1=True
                  battle_judge_state=player_gather.act_judge(event_que.queue,gamestate,map_name)
                  if gamestate !='fixdialog' and gamestate!='dialogchoice' and gamestate!='dialog':
                     if battle_judge_state:
                        gamestate="battle"
                     else:
                        gamestate="normal"
                  npc0.judge(player)

                  for i in event_que.queue:
                     if gamestate!= 'dialogchoice' and gamestate!= 'dialog' and gamestate!='shop' and i.type==pygame.KEYDOWN and i.event.key==pygame.K_e and npc0.dis==True:
                        gamestate='dialogchoice'
               
                  if gamestate=='dialogchoice' :
                     npc0.choice.paint(screen,event_que)
                     if npc0.choice.finished_writing and gamestate=='dialogchoice':

                        for i in event_que.queue:
                           if i.type==pygame.KEYDOWN and i.event.key==pygame.K_1 :
                              event_que.queue.remove(i)
                              npc0.choice.finished_writing=False
                              gamestate='dialog'
                           if i.type==pygame.KEYDOWN and i.event.key==pygame.K_2 :
                              event_que.queue.remove(i)
                              npc0.choice.finished_writing=False
                              gamestate='shop'
                           if i.type==pygame.KEYDOWN and i.event.key==pygame.K_3 :
                              event_que.queue.remove(i)
                              npc0.choice.finished_writing=False
                              gamestate='fixdialog'
                           if i.type==pygame.KEYDOWN and i.event.key==pygame.K_4 :
                              event_que.queue.remove(i)
                              npc0.choice.finished_writing=False
                              gamestate='normal'
                  
                  if gamestate=='fixdialog':
                     if player.status['time']>=300:
                        npc0.fixout[number].paint(screen,event_que)
                        if npc0.fixout[number].finished_writing:
                           gamestate='normal'
                           number=0
                     else:
                        npc0.fixout[number].paint(screen,event_que)
                        if npc0.fixout[number].finished_writing:
                           npc0.fixout[number].finished_writing=False
                           number=number+1    
                           if number==len(npc0.fixout):
                              gamestate='normal'
                              number=0
                              end_count2=True


                  if gamestate=='dialog' and len(w1)==0 and wait==False:
                     
                     chatfunction1(messages,client,screen,w1,'Sarvan',touxiang)
                  if gamestate=='dialog' and len(w1)>0:
                     w1[0].paint(screen,event_que)
                     if w1[0].finished_writing:
                        w1[0].finished_writing=False
                        w1.pop(0)
                  if len(w1)==0 and gamestate=='dialog': 
                     gamestate,wait=text_input_box.handle_event(w1,messages,user_input,event_que,'normal',touxiang,baglist)
                     text_input_box.draw(screen,event_que)
               
                  
                  uimanager.show(player)
                  if timebar.update():
                     gamestate="death"

                  map_manager.dict[map_name]["door"].draw(screen,map_manager.dict[map_name]["camera"].len)
                  map_manager.dict[map_name]["entity_group"].draw(screen,map_manager.dict[map_name]["camera"].len)
                  if map_name=="tutoral":
                        group0.draw(screen,map_manager.dict[map_name]["camera"].len)
                  spirit_show_manager.sort_and_show(screen)
         pygame.display.flip()
         pygame.time.Clock().tick(60)