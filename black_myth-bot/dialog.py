import pygame
import time
import animation
from animation import spirit_show_manager
from player_code import player
from astart import object1
import copy
from astart import objectthing
w1=[]
ppt=[]
def makeWords(txt, size, color):  # 文字渲染,返回 渲染的对象和尺寸
    my_font = pygame.font.Font("material/2.1/汇文明朝体GBK.ttf", size)
    r = my_font.render(str(txt), True, color)
    return (r, r.get_size())


class WordsOutput():
    def __init__(self, text, x, y, name=None, portrait=None):
        self.startx = x  # 起始位置
        self.starty = y
        self.endx = 1200  # 边缘位置
        self.text = text
        self.name = name
        self.portrait = portrait  # 头像为surface对象
        if self.portrait != None:  # 如果有头像则改变起始位置
            self.startx = 192  # 将起始x位置设置为头像宽度
            self.portrait = pygame.transform.scale(
                self.portrait, (192, 192)
            )  # 压缩图片尺寸到192×192
        self.words = []  # 储存渲染出来的文字的列表
        self.analyzed = False  # 是否分析过
        self.interval = time.time()  # 计时器
        self.output_speed = 0.1  # 输出文字的间隔时间
        self.finished_writing = False  # 是否结束输出文字
        self.out_num = 0  # 输出的文字编号
        # 定义带有透明度的灰色 (R, G, B, A)
        gray_with_alpha = (128, 128, 128, 128)

        # 创建一个带有 alpha 通道的 Surface
        self.rect_surface = pygame.Surface((self.endx-self.startx, 300), pygame.SRCALPHA)
        self.rect_surface.fill(gray_with_alpha)
        self.kuang=animation.Spirit_state(self.rect_surface,self.startx,self.starty,90)
        spirit_show_manager.spirits.append(self.kuang)

    def analyze(self):
        txt = self.text  # 将txt赋值为内容
        height = makeWords(txt[0], 35, (255, 255, 255))[1][1]  # 单个文字高度,用第一个字的高度
        txt_list = []  # 渲染出来的文字列表
        w_last = 0  # 叠加文字后的整体长度
        start_y=self.starty
        # 检测是否有头像
        if self.portrait != None:
            #self.startx=self.startx+self.portrait.get_width()
            txt_list.append((self.portrait, (0, start_y)))
        # 若有名字则将名字渲染出来存储进列表,改变排版
        if self.name != None:
            a = makeWords(self.name, 35, (255, 255, 0))
            txt_list.append((a[0], (self.startx, self.starty)))
            start_y += a[1][1]
        # 开始遍历文字
        for i in range(len(txt)):
            a = makeWords(txt[i], 35, (255, 255, 255))  # 渲染文字
            if self.startx + w_last + a[1][0] <= self.endx:  # 检测是否超出设定边缘
                # 未超出则记录位置,渲染文字,存储进列表
                pos = (self.startx + w_last, start_y)
                txt_list.append((a[0], pos))
                w_last += a[1][0]
            else:
                # 超出:换行,将x坐标设置为初始值,y则增加一个字的高度
                start_y += a[1][1]
                w_last = 0
                a = makeWords(txt[i], 35, (255, 255, 255))
                pos = (self.startx + w_last, start_y)
                txt_list.append((a[0], pos))
                w_last += a[1][0]
        self.words = txt_list
        self.analyzed = True

    def paint(self,screen,event_que):
        for i in event_que.queue:
            if i.type==pygame.KEYDOWN and i.event.key==pygame.K_j :
                if len(self.words)!=self.out_num:
                    self.out_num= len(self.words)-1
                    event_que.queue.remove(i)
        
        self.kuang.show_j()
        if self.analyzed == False:
            self.analyze()
        if time.time() >= self.interval + self.output_speed and self.out_num < len(
            self.words
        ):  # 检测是否到输出下一个文字的时间并且还未输出完
            self.out_num += 1
            self.interval = time.time()  # 重置计时器
        for i in range(self.out_num):  # 绘制到达的文字
            img, pos = self.words[i]
            
            word=animation.Spirit_state(img,pos[0],pos[1],100)
            spirit_show_manager.spirits.append(word)
            word.show_j()
        if self.out_num == len(self.words):  # 如果绘制完了
            for i in event_que.queue:
                if i.type==pygame.KEYDOWN and i.event.key==pygame.K_j :
                    self.finished_writing = True
                    event_que.queue.remove(i)# 将变量设置为True
            


class TextInputBox:
    def __init__(self, x, y, width, height,font_size=40):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (0, 0, 255)
        self.text = ""
        self.font = pygame.font.Font('material/2.1/汇文明朝体GBK.ttf', font_size)
        self.active = False
        self.width=width
        self.height=height
        self.dout=0
        self.startout=0
        self.ksurface=pygame.Surface((self.width,self.height))
        self.ksurface.fill((255,255,255))
        self.k=animation.Spirit_state(self.ksurface, self.rect.x,self.rect.y, 110)
        spirit_show_manager.spirits.append(self.k)

    def handle_event(self,w1,messages,user_input,event_que,store,touxiang,baglist):
        
        for i in event_que.queue:
            if i.type == pygame.MOUSEBUTTONDOWN :
                if self.rect.collidepoint(i.event.pos):
                    self.active = True
                    self.color=(255,0,0)
                else:
                    self.active = False
                    self.color=(0,0,255)
            if i.type == pygame.KEYDOWN:
                if self.active:
                    if i.event.key == pygame.K_RETURN:
                        event_que.queue.remove(i)
                        user_input=self.text
                        self.text = ""
                        self.active=False
                        self.color=(0,0,255)
                    elif i.event.key == pygame.K_BACKSPACE:
                        event_que.queue.remove(i)
                        self.text = self.text[:-1]
                    else:

                        self.text += i.event.unicode
        if user_input=='':
            return 'dialog',True
            
        elif user_input.lower() in ['exit','quit']:
            
            user_input=''
            print ('chat ends')
            return store,False
        elif user_input!='' :
            print(user_input)
            if 'not' in user_input and 'first' in user_input:
                print('1')
                newobject=objectthing(object1.text, object1.pic, object1.name, object1.num)
                newobject.num=str(len(baglist)+1)
                baglist.append(newobject)

                w1.append(WordsOutput('.. Interesting. Will there be some difference about this time.Let me get you some supplies'+' ',0,500,'名字',touxiang))
                return 'dialog',False
            elif 'kill me' in user_input:
                print('2')
                player.status['health']=0
                w1.append(WordsOutput('Interesting ,I will satisfy you' +' ',0,500,'名字',touxiang))
                return 'dialog',False
            else:
                messages.append({"role": "user", "content": user_input})
                return 'dialog',False
                
        

    def draw(self, surface,event_que):
        self.startout=max(len(self.text)-10,0)
        pygame.draw.rect(self.ksurface, self.color, self.ksurface.get_rect(), 2)
        self.k.show_j()
        for i in event_que.queue:
            if i.type==pygame.KEYDOWN and i.event.key==pygame.K_RIGHT :
                self.dout=self.dout+1
            if i.type==pygame.KEYDOWN and i.event.key==pygame.K_LEFT :
                self.dout=self.dout-1
        if self.startout+self.dout<0:
            self.dout=-self.startout
        if self.startout+self.dout>max(len(self.text)-10,0):
            self.dout=len(self.text)-10-self.startout
        self.startout=self.startout+self.dout

        text_surface = self.font.render(self.text[self.startout:self.startout+10], True, (0,0,0))
        textout=animation.Spirit_state(text_surface, self.rect.x + 5, self.rect.y + 5,120)
        spirit_show_manager.spirits.append(textout)
        textout.show_j()

ppt.append(WordsOutput('你好，受了委托的冒险者。',0,0))
ppt.append(WordsOutput('wasd 上下移动，j键出拳/确认，k键取消，e键交互。esc键进入暂停界面，用数字选择，打开背包。',0,0))
ppt.append(WordsOutput('触发战斗后，摁下lctrl进入时停状态',0,0))
ppt.append(WordsOutput('时停状态下，摁k退出，摁下tab后可用ad选择技能，jk键确认与取消。',0,0))
ppt.append(WordsOutput('时停的能量与放技能的法力值成互补关系，冲刺有无敌帧，请多多运用特性打败敌人。',0,0))
ppt.append(WordsOutput('被打僵直的时候既无法进入时停也无法行动哦，小心别被包围了。',0,0))
ppt.append(WordsOutput('生命清零会消耗60s左下角的时间复活，但左下角的时间清零了就会真的死亡。',0,0))
ppt.append(WordsOutput('你的任务目标就在左上角的隐藏洞穴内，冲！',0,0))
ppt.append(WordsOutput('（又是一次普通的任务，你心想，但对眼前的一切总有种即视感。）',0,0))