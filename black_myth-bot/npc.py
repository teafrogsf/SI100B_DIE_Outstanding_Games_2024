import entity
import mapsetting
from mapsetting import map_manager
import pygame
import dialog
import animation
from animation import spirit_show_manager


class npcs(entity.EntityLike):
    def __init__(self,name,portrait,rect,group,fixtextlist):
        super().__init__(rect,group)
        self.name=name
        self.portrait=portrait
        self.dis=False
        self.rect_surface = pygame.Surface((300, 300), pygame.SRCALPHA)
        self.rect_surface.fill((128, 128, 128, 128))
        self.choice=dialog.WordsOutput('1.LLM对话''2.交易''3.固定对话''4.返回',0,500,name,portrait)
        self.fixout=fixtextlist

        self.ani=animation.Animation_Simple("2.11/2.113/Agis",scale=1)
        self.ani.start_animation()
        self.npcshow=animation.Spirit_state(self.ani.ani_img,self.rect.x,self.rect.y,9)
        spirit_show_manager.add_spirit(self.npcshow)
        
    def judge(self,player):
        if ((player.imgstate.rect.center[0]-self.rect.x)**2+(player.imgstate.rect.center[1]-self.rect.y)**2)**0.5<=600:
            self.dis= True
        else:
            self.dis= False
        
    def draw(self,screen,camera: tuple[int, int]):  # 定义显示实体的方法，该方法在场景需要描绘图像的时候调用
        self.npcshow.rect.x=self.npcshow.rect.x+camera[0]
        self.npcshow.rect.y=self.npcshow.rect.y+camera[1]
        self.rect.x=self.rect.x+camera[0]
        self.rect.y=self.rect.y+camera[1]
        self.ani.update()
        self.npcshow.image=self.ani.ani_img
        # pygame.draw.rect(screen, (0, 128, 255), self.npcshow.rect,2)
        self.npcshow.show_j()




npcimg=pygame.image.load('material/2.11/2.113/Agis1.png')
npcimg=pygame.transform.scale(npcimg,(208,225))
npcrect=pygame.Rect(-450,-1400,208,225)


m1=dialog.WordsOutput('......',0,500,'名字',npcimg)
m2=dialog.WordsOutput('怎么可能？',0,500,'名字',npcimg)
m3=dialog.WordsOutput('为什么你会在这一次浪费了这么多时间？',0,500,'名字',npcimg)
m4=dialog.WordsOutput('...',0,500,'名字',npcimg)
m5=dialog.WordsOutput('有来客进入你的意识了，对吗',0,500,'名字',npcimg)
m6=dialog.WordsOutput('想不到这样一次任务都能见证天选者的诞生',0,500,'名字',npcimg)
m7=dialog.WordsOutput('我授予你时间的神器，消耗你的时间之后，能获得什么能力全看你的天资了',0,500,'名字',npcimg)
m8=dialog.WordsOutput('（收下神器）',0,500,'名字',npcimg)
m9=dialog.WordsOutput('左上角有通往魔物的道路，去结束轮回吧',0,500,'名字',npcimg)

npcmessage=[m1,m2,m3,m4,m5,m6,m7,m8]
group0=entity.collion_group()
npc0=npcs('名字',npcimg,npcrect,group0,npcmessage)