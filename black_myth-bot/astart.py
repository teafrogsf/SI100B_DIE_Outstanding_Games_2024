import pygame
import animation
from animation import spirit_show_manager
from player_code import player
import copy
objectlist = []
baglist = []

def prepare():
    fontname = pygame.font.Font("material/2.1/汇文明朝体GBK.ttf", 100)
    name_surface = fontname.render("瞬 刻 永 恒", True, (250, 250, 250))
    name_rect = name_surface.get_rect(center=(600, 300))
    name = animation.Spirit_state(name_surface, name_rect.x, name_rect.y, 2)
    spirit_show_manager.spirits.append(name)
    death_surface = fontname.render("你 死 了", True, (250, 250, 250))
    death_rect = death_surface.get_rect(center=(600, 300))
    death = animation.Spirit_state(death_surface, death_rect.x, death_rect.y, 2)
    spirit_show_manager.spirits.append(death)

    startbg = pygame.image.load("material/2.2/2.21/开始背景.png")
    startbg = pygame.transform.scale(startbg, (1200, 800))
    start = animation.Spirit_state(startbg, 0, 0, 1)
    spirit_show_manager.spirits.append(start)

    deathpic = pygame.image.load("material/2.151/死亡背景.png")
    deathpic = pygame.transform.scale(deathpic, (1200, 800))
    deathbg = animation.Spirit_state(deathpic, 0, 0, 1)
    spirit_show_manager.spirits.append(deathbg)

    font = pygame.font.Font("material/2.1/汇文明朝体GBK.ttf", 50)
    text_surface = font.render("按Enter键开始游戏", True, (250, 250, 250))
    text_rect = text_surface.get_rect(center=(600, 400 + 150))
    prompt = animation.Spirit_state(text_surface, text_rect.x, text_rect.y, 2)
    spirit_show_manager.spirits.append(prompt)

    fontlar = pygame.font.Font("material/2.1/汇文明朝体GBK.ttf", 80)

    continue_surface = font.render("按1继续游戏", True, (255, 255, 255))
    bag_surface = font.render("按2打开背包", True, (255, 255, 255))
    stoptit_surface = fontlar.render("暂停", True, (255, 255, 255))

    continue_rect = continue_surface.get_rect(center=(600, 400 - 150))
    bag_rect = bag_surface.get_rect(center=(600, 400 + 150))
    stoptit_rect = stoptit_surface.get_rect(center=(600, 100))

    continuegame = animation.Spirit_state(continue_surface, continue_rect.x, continue_rect.y, 2)
    bag = animation.Spirit_state(bag_surface, bag_rect.x, bag_rect.y, 2)
    stoptit = animation.Spirit_state(stoptit_surface, stoptit_rect.x, stoptit_rect.y, 2)

    spirit_show_manager.spirits.append(continuegame)
    spirit_show_manager.spirits.append(bag)
    spirit_show_manager.spirits.append(stoptit)

    shopbg1 = pygame.image.load("material/2.16/background_Town1.png")
    shopbg2 = pygame.image.load("material/2.16/background_Town2.png")
    shopbg3 = pygame.image.load("material/2.16/background_Town3.png")
    shoper = pygame.image.load("material/2.16/立绘.png")
    shopbg1 = pygame.transform.scale(shopbg1, (1200, 800))
    shopbg2 = pygame.transform.scale(shopbg2, (1200, 800))
    shopbg3 = pygame.transform.scale(shopbg3, (1200, 800))
    shoper = pygame.transform.scale(shoper, (300, 450))
    shop1 = animation.Spirit_state(shopbg1, 0, 0, 1)
    shop2 = animation.Spirit_state(shopbg2, 0, 0, 2)
    shop3 = animation.Spirit_state(shopbg3, 0, 0, 3)
    shoper = animation.Spirit_state(shoper, 0, 0, 4)
    spirit_show_manager.spirits.append(shop1)
    spirit_show_manager.spirits.append(shop2)
    spirit_show_manager.spirits.append(shop3)
    spirit_show_manager.spirits.append(shoper)

    # 定义带有透明度的灰色 (R, G, B, A)
    gray_with_alpha = (128, 128, 128, 128)
    # 创建一个带有 alpha 通道的 Surface
    rect_surface = pygame.Surface((1200 - 492, 500), pygame.SRCALPHA)
    rect_surface.fill(gray_with_alpha)
    shopkuang = animation.Spirit_state(rect_surface, 492, 300, 4)
    spirit_show_manager.spirits.append(shopkuang)

    bager = pygame.image.load("material/2.3/2.33/7.png")
    bager = pygame.transform.scale(bager, (300, 450))
    bagershow = animation.Spirit_state(bager, 0, 0, 4)
    spirit_show_manager.spirits.append(bagershow)

    return death ,deathbg,name ,start, prompt,continuegame,bag,stoptit,shop1,shop2,shop3,shoper,shopkuang,bagershow

def makeWords(txt, size, color):  # 文字渲染,返回 渲染的对象和尺寸
    my_font = pygame.font.Font("material/2.1/汇文明朝体GBK.ttf", size)
    r = my_font.render(str(txt), True, color)
    return (r, r.get_size())
def victorydef(screen,event_que,list0):
    if len(list0)>=0:
        list0[0].show_j()
        for i in event_que.queue:
            if i.type == pygame.KEYDOWN and i.event.key == pygame.K_j and len(list0)>1:
                list0.pop(0)

def deathdef(screen,death,deathbg):
    death.show_j()
    deathbg.show_j()
def startdef(event_que, screen,name,start,prompt):
    name.show_j()

    start.show_j()

    prompt.show_j()

    for i in event_que.queue:
        if i.type == pygame.KEYDOWN and i.event.key == pygame.K_RETURN:
            event_que.queue.remove(i)
            return "normal"
    else:
        return "start"


def stopdef(event_que, screen, store,start,continuegame,bag,stoptit):
    
    start.show_j()   

    continuegame.show_j()
    bag.show_j()
    stoptit.show_j()

    for i in event_que.queue:
        if i.type == pygame.KEYDOWN:
            if i.event.key == pygame.K_1:
                event_que.queue.remove(i)
                return store
            elif i.event.key == pygame.K_2:
                event_que.queue.remove(i)
                return "bag"
    return "stop"


class objectthing:
    def __init__(self, text, pic, name, num):
        self.name = name
        self.rect = pygame.Rect(300, 300, 800, 400)
        self.num = num
        self.text = text
        self.pic = pygame.transform.scale(pic, (192, 192))
        self.color = (255, 255, 255)
        self.active = False
        self.startx = 300 + 192
        self.starty = 300
        self.words = []
        self.analyzed = False
        self.endx = 1200

    def analyze(self):
        txt = self.text  # 将txt赋值为内容
        height = makeWords(txt[0], 35, (255, 255, 255))[1][
            1
        ]  # 单个文字高度,用第一个字的高度
        txt_list = []  # 渲染出来的文字列表
        w_last = 0  # 叠加文字后的整体长度
        start_y = self.starty
        txt_list.append((self.pic, (300, start_y)))
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

    def listen(self, screen, event_que, objectlist, baglist,gamestate,player):
        permitbuy = True
        for i in objectlist:
            if i.active == True:
                permitbuy = False

        for i in event_que.queue:
            if (
                permitbuy == True
                and self.active == False
                and i.type == pygame.KEYDOWN
                and i.event.unicode == self.num
            ):
                event_que.queue.remove(i)
                self.active = True
                self.color = (255, 0, 0)
            if (
                self.active == True
                and i.type == pygame.KEYDOWN
                and i.event.key == pygame.K_k
            ):
                event_que.queue.remove(i)
                self.active = False
                self.color = (255, 255, 255)
            if (
                self.active == True
                and i.type == pygame.KEYDOWN
                and i.event.key == pygame.K_j
            ):
                event_que.queue.remove(i)
                if gamestate == "bag":
                    if self.name=='苹果':
                        player.status['health']=player.status['health']+5
                        player.status['health']=min(player.status['health'],9)
                        print("do")
                        baglist.remove(self)
                    if self.name=='培根':
                        player.status['mp']=player.status['mp']+5
                        player.status['mp']=min(player.status['mp'],9)
                        print("do")
                        baglist.remove(self)
                    if self.name=='骨头':
                        player.status['time']=player.status['time']+50
                        player.status['time']=min(player.status['time'],600)
                        print("do")
                        baglist.remove(self)
                    if self.name=='蓝莓':
                        player.status['health']=player.status['health']+9
                        player.status['health']=min(player.status['health'],9)
                        print("do")
                        baglist.remove(self)        
                if gamestate == "shop":
                    if self.name=='苹果' and player.money>=2:
                        player.money=player.money-2
                        print('buy')
                        objectnew=objectthing(self.text, self.pic, self.name, self.num)
                        objectnew.num=str(len(baglist)+1)
                        baglist.append(objectnew)
                        self.active=False 
                        self.color=(255, 255, 255)
                    if self.name=='培根' and player.money>=3:
                        player.money=player.money-3
                        print('buy')
                        objectnew=objectthing(self.text, self.pic, self.name, self.num)
                        objectnew.num=str(len(baglist)+1)
                        baglist.append(objectnew)
                        self.active=False 
                        self.color=(255, 255, 255)
                    if self.name=='骨头' and player.money>=20:
                        player.money=player.money-20
                        print('buy')
                        objectnew=objectthing(self.text, self.pic, self.name, self.num)
                        objectnew.num=str(len(baglist)+1)
                        baglist.append(objectnew)
                        self.active=False 
                        self.color=(255, 255, 255)
                    if self.name=='蓝莓' and player.money>=5:
                        player.money=player.money-5
                        print('buy')
                        objectnew=objectthing(self.text, self.pic, self.name, self.num)
                        objectnew.num=str(len(baglist)+1)
                        baglist.append(objectnew)
                        self.active=False 
                        self.color=(255, 255, 255)


    def draw(self, screen, event_que):
        if self.active == True:
            if self.analyzed == False:
                self.analyze()
            for i in range(len(self.words)):  # 绘制到达的文字
                img, pos = self.words[i]
                shopword = animation.Spirit_state(img, pos[0], pos[1], 5)
                spirit_show_manager.spirits.append(shopword)
                shopword.show_j()

    def paintup(self, screen, num):
        if num + 1 <= 3:
            y = 0
        elif num + 1 <= 6:
            y = 50
        elif num + 1 <= 9:
            y = 100
        elif num + 1 <= 12:
            y = 150
        else:
            y = 200
        font = pygame.font.Font("material/2.1/汇文明朝体GBK.ttf", 50)
        list_surface = font.render(f"{self.num}.{self.name}", True, self.color)
        list_rect = list_surface.get_rect(topleft=(300 + ((num) % 3) * 250, y))
        listshow = animation.Spirit_state(list_surface, list_rect.x, list_rect.y, 5)
        spirit_show_manager.spirits.append(listshow)
        listshow.show_j()


def shopdef(event_que, screen, store, money, objectlist,baglist, gamestate,shop1,shop2,shop3,shoper,shopkuang,player):
    
    shop1.show_j()
    shop2.show_j()
    shop3.show_j()
    shoper.show_j()
    font = pygame.font.Font("material/2.1/汇文明朝体GBK.ttf", 50)
    money_surface = font.render(f"money  :  {money}", True, (255, 255, 255))
    money_rect = money_surface.get_rect(center=(150, 500))
    moneyshow = animation.Spirit_state(money_surface, money_rect.x, money_rect.y, 4)
    spirit_show_manager.spirits.append(moneyshow)
    moneyshow.show_j()
    
    shopkuang.show_j()
    for i in range(len(objectlist)):
        objectlist[i].paintup(screen, i)
        objectlist[i].listen(screen, event_que, objectlist,baglist, gamestate,player)
        objectlist[i].draw(screen, event_que)
    for i in objectlist:
        if i.active == True:
            return "shop"
    for i in event_que.queue:
        if i.type == pygame.KEYDOWN and i.event.key == pygame.K_k:
            event_que.queue.remove(i)
            return store
    return "shop"


object1pic = pygame.image.load("material/2.16/物品/apple.png")
object2pic=pygame.image.load('material/2.16/物品/bacon fried.png')
object3pic=pygame.image.load('material/2.16/物品/beef on bone raw.png')
object4pic=pygame.image.load('material/2.16/物品/blue jam.png')
object5pic=pygame.image.load('material/2.16/物品/bacon fried.png')
object1 = objectthing(
    "加5hp,价格2元",
    object1pic,
    "苹果",
    '1',
)
object2 = objectthing(
    "加5mp,价格2元",
    object2pic,
    "培根",
    '2',
)
object3 = objectthing(
    "加50time,价格20元",
    object3pic,
    "骨头",
    '3',
)
object4 = objectthing(
    "加9hp,价格5元",
    object4pic,
    "蓝莓",
    '4',
)


objectlist.append(object1)
objectlist.append(object2)
objectlist.append(object3)
objectlist.append(object4)





def bagdef(event_que, screen, store, money, baglist,objectlist, gamestate,shop1,shop2,shop3,bagershow,shopkuang,player):

    
    shop1.show_j()
    shop2.show_j()
    shop3.show_j()
    bagershow.show_j()
    font = pygame.font.Font("material/2.1/汇文明朝体GBK.ttf", 50)

    money_surface = font.render(f"money  :  {money}", True, (255, 255, 255))
    health_surface = font.render(f"health  :  {player.status['health']}", True, (255, 255, 255))
    mp_surface = font.render(f"mp  :  {player.status['mp']}", True, (255, 255, 255))
    time_energy_surface = font.render(f"time_energy  :  {player.status['time_energy']}", True, (255, 255, 255))
    time_surface = font.render(f"time  :  {int(player.status['time'])}", True, (255, 255, 255))
    # health_surface = font.render(f"health  :  {player.status["health"]}", True, (255, 255, 255))
    # mp_surface = font.render(f"mp  :  {player.status["mp"]}", True, (255, 255, 255))
    # time_energy_surface = font.render(f"time_energy  :  {player.status["time_energy"]}", True, (255, 255, 255))
    # time_surface = font.render(f"time  :  {int(player.status["time"])}", True, (255, 255, 255))

    money_rect = money_surface.get_rect(center=(200, 500))
    health_rect = health_surface.get_rect(center=(200, 550))
    mp_rect = mp_surface.get_rect(center=(200, 600))
    time_energy_rect = time_energy_surface.get_rect(center=(200, 650))
    time_rect = time_surface.get_rect(center=(200, 700))

    moneyshow = animation.Spirit_state(money_surface, money_rect.x, money_rect.y, 4)
    healthshow = animation.Spirit_state(health_surface, health_rect.x, health_rect.y, 4)
    mpshow = animation.Spirit_state(mp_surface, mp_rect.x, mp_rect.y, 4)
    time_energyshow = animation.Spirit_state(time_energy_surface, time_energy_rect.x, time_energy_rect.y, 4)
    timeshow = animation.Spirit_state(time_surface, time_rect.x, time_rect.y, 4)

    spirit_show_manager.spirits.append(moneyshow)
    spirit_show_manager.spirits.append(healthshow)
    spirit_show_manager.spirits.append(mpshow)
    spirit_show_manager.spirits.append(time_energyshow)
    spirit_show_manager.spirits.append(timeshow)

    moneyshow.show_j()
    healthshow.show_j()
    mpshow.show_j()
    time_energyshow.show_j()
    timeshow.show_j()

    spirit_show_manager.spirits.append(shopkuang)
    shopkuang.show_j()
    for i in range(len(baglist) - 1, -1, -1):
        baglist[i].paintup(screen, i)
        baglist[i].draw(screen, event_que)
        baglist[i].listen(screen, event_que, objectlist,baglist, gamestate,player)
    for i in range (1,len(baglist)+1):
        baglist[i-1].num=str(i)
    for i in baglist:
        if i.active == True:
            return "bag"
    for i in event_que.queue:
        if i.type == pygame.KEYDOWN and i.event.key == pygame.K_k:
            event_que.queue.remove(i)
            return store
    return "bag"
