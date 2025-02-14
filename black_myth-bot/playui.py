import pygame
from animation import spirit_show_manager
import animation
from player_code import player

uibg=animation.Spirit_state(pygame.image.load("material/2.3/2.310/uibg.png"),0,700,95)
spirit_show_manager.add_spirit(uibg)

class Useable_ui:
    def __init__(self,base_name,name=None,x=2000,y=2000,scale=2):
        self.name=name
        self.icon=animation.Animation_Simple(base_name,scale=scale)
        self.icon_state=animation.Spirit_state(self.icon.ani_img,x,y,z=100)
        spirit_show_manager.add_spirit(self.icon_state)
    def use(self):
        self.icon.indice=1
        self.icon_state.image=self.icon.ani_img
    def unuse(self):
        self.icon.indice=0

class Status_ui(Useable_ui):
    def __init__(self,base_name,name=None,x=2000,y=2000,scale=5):
        super().__init__(base_name,name,x,y,scale)
        self.icon.indice=len(self.icon.imglist)-1
        self.icon_state=animation.Spirit_state(self.icon.ani_img,x,y,z=100)
        spirit_show_manager.add_spirit(self.icon_state)
    def refresh(self,gamer):
        self.icon.indice=gamer.status[self.name] if gamer.status[self.name]>=0 else 0
        self.icon_state.image=self.icon.ani_img
        self.icon_state.show_j()

class Play_ui_manager:
    def __init__(self):
        self.list=[]
    def add(self,ui,x,y):
        ui.icon_state.rect.x,ui.icon_state.rect.y=x,y
        self.list.append(ui)
    def refresh(self,gamer):
        for i in self.list:
            if isinstance(i,Status_ui):
                i.refresh(gamer)
    def show(self,gamer,x_c=0,y_c=0):
        self.refresh(gamer)
        uibg.show_j()
        for i in self.list:
            i.icon_state.show_j(x_c,y_c)

healthbar=Status_ui("2.3/2.31/healthbars/healthbar",name="health")
mpbar=Status_ui("2.3/2.31/mp/mp",name="mp")
time_energybar=Status_ui("2.3/2.31/time_energy/time_energy",name="time_energy")

uimanager=Play_ui_manager()
uimanager.add(healthbar,5,705)
uimanager.add(mpbar,215,705)
uimanager.add(time_energybar,425,705)


class Timebar():
    def __init__(self):
        self.my_font = pygame.font.Font("material/2.1/汇文明朝体GBK.ttf", 40)
        self.last_update = pygame.time.get_ticks()  # 用于跟踪上次更新的时间戳
        # 定义倒计时时长（以秒为单位）
        self.countdown_time = 600 # 例如：10秒倒计时
        self.start_ticks = pygame.time.get_ticks()  # 获取当前时间戳
        # 渲染倒计时文本
        self.text_surface = self.my_font.render(str(player.status["time"] ), True, (255, 0, 0))  # 文字颜色为红色
        self.timebar=animation.Spirit_state(self.text_surface,100,740,z=100.5)
        # 将倒计时文本绘制到屏幕底部中央
        spirit_show_manager.add_spirit(self.timebar)
    def update(self):
        current_ticks = pygame.time.get_ticks()
        if player.status["time"] <= 0:
            return True
        else:
            # 计算自上次更新以来经过的时间
            elapsed_time = (current_ticks - self.last_update) / 1000
            self.last_update = current_ticks
            # 减去经过的时间，但不超过剩余时间
            player.status["time"] = max(player.status["time"] - elapsed_time, 0)

            # 渲染新的倒计时文本
            self.text_surface = self.my_font.render(str(round(player.status["time"])), True, (255, 0, 0))
            
            # 更新Spirit_state对象的图像属性
            self.timebar.image = self.text_surface
            
            # 调用spirit_show_manager的适当方法来更新屏幕上的精灵状态
            self.timebar.show_j()
            
            return False