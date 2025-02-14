import pygame
import os
def img_load(name,scale=1):
    images=[]
    i = 0
    while True:
        i += 1
        filename = name.format(i)
        if os.path.exists(filename):
            images.append(pygame.transform.scale(pygame.image.load(filename),(pygame.image.load(filename).get_width()*scale,pygame.image.load(filename).get_height()*scale)))
        else:
            break
    return images
class Base_Animation():
    def __init__(self,ani_spd=100):
        self.ani_spd=ani_spd
        self.last_update_time = pygame.time.get_ticks()
        self.animation_active = False
        self.loop_count=0
    def start_animation(self):
        self.animation_active = True
    def stop_animation(self):
        self.animation_active = False  

class Animation_Simple(Base_Animation):
    def __init__(self,base_name,scale=1,ani_spd=100,imglist=None):
        super().__init__(ani_spd)
        if base_name==None:
           self.imglist=imglist
        else:
           self.imglist=img_load(f"material/{base_name}{{}}.png",scale)
        self._indice = 0   # 内部使用的属性  
        self.ani_img=self.imglist[self._indice]
    @property
    def indice(self):
        """Property getter for the current index in the animation."""
        return self._indice

    @indice.setter
    def indice(self, value):
        """Property setter for the current index in the animation. Updates ani_img when indice changes."""
        self._indice = value % len(self.imglist)  # 确保索引在有效范围内
        self.ani_img = self.imglist[self._indice]  # 更新ani_img以反映新的indice

    def update(self):
        if self.animation_active == True:
            now=pygame.time.get_ticks()
            if now - self.last_update_time > self.ani_spd:
                self.last_update_time = now
                self.indice = (self.indice+ 1) % len(self.imglist)##
                self.ani_img=self.imglist[self.indice]
    def update_t(self,time):
        # 新增属性: 动画循环计数器和目标循环次数
        self.target_loops = time
        def update_with_count():
            self.update()
            # 如果动画帧达到最后一个，则增加循环计数
            if self.indice == len(self.imglist)-1 and self.animation_active:
                self.loop_count += 1
        if self.animation_active:
            if self.loop_count >= self.target_loops:
                self.stop_animation()
                self.loop_count = 0
                return True
            else:
                update_with_count()
                # 检查是否达到了目标循环次数
                return False
        else:
            return False  # 如果动画未激活，则返回False

class Animation(Base_Animation):
    def __init__(self,base_name,scale=1,ani_spd=70):
        super().__init__(ani_spd)
        self.imgdict={"l":None,"r":None,"u":None,"d":None}
        self.indices={"l":0,"r":0,"u":0,"d":0}
        for direction in ["l", "r", "u", "d"]:
            image_path = f"material/{base_name}_{direction}{{}}.png"
            self.imgdict[direction] = img_load(image_path,scale)
        self.direc= "u"
        self.last_direc="u"
        self.ani_img=self.imgdict[self.direc][self.indices[self.direc]]
        self.loop_count=0
    
    def update(self):
        if self.animation_active == True:
            for i in self.indices.keys():
                if i != self.direc:
                    self.indices[i]=0
            now=pygame.time.get_ticks()
            if self.direc== self.last_direc:
                if now - self.last_update_time > self.ani_spd:
                    self.last_update_time = now
                    self.indices[self.direc] = (self.indices[self.direc] + 1) % len(self.imgdict[self.direc])
                    self.ani_img=self.imgdict[self.direc][self.indices[self.direc]]
            else:
                self.last_direc=self.direc
                self.last_update_time = now
                self.indices[self.direc] = (self.indices[self.direc] + 1) % len(self.imgdict[self.direc])
                self.ani_img=self.imgdict[self.direc][self.indices[self.direc]]
    def update_t(self, time):
        # 新增属性: 动画循环计数器和目标循环次数
        self.target_loops = time
        def update_with_count():
            self.update()
            # 如果动画帧达到最后一个，则增加循环计数
            if self.indices[self.direc] == 0 and self.animation_active:
                self.loop_count += 1
        if self.animation_active:
            while self.loop_count < self.target_loops:
                update_with_count()
                # 检查是否达到了目标循环次数
                if self.loop_count >= self.target_loops:
                    self.stop_animation()
                    self.loop_count = 0
                    return True
                else:
                    return False
        else:
            return False  # 如果动画未激活，则返回False      
    def refresh(self):
        self.indices={"l":0,"r":0,"u":0,"d":0}


class Spirit_state():
    def __init__(self,image,x,y,z=1):
        self._width=image.get_width()
        self._height=image.get_height()
        self.image = image 
        self.direc="u"
        self.rect = pygame.Rect((x,y,self.width,self.height))
        self.z=z
        self.isshow=False
        self.always_show=False

    @property
    def width(self):
        """Image getter method."""
        return self._width

    @width.setter
    def width(self, new_width):
        self.rect.width = new_width
    
    @property
    def height(self):
        """Image getter method."""
        return self._height

    @height.setter
    def height(self, new_height):
        self.rect.height= new_height

    def show_j(self,x_c=0,y_c=0):
        self.rect.x+=x_c
        self.rect.y+=y_c
        self.isshow=True

    def show(self,screen,):
        if self.isshow:
            screen.blit(self.image,self.rect)
        if self.always_show:
            pass
        else:
          self.isshow=False

class SpiritManager:
    def __init__(self):
        self.spirits = []

    def add_spirit(self, spirit):
        # 添加精灵到列表中
        self.spirits.append(spirit)
    def delet_spirit(self,spirit):
        self.spirits.remove(spirit)

    def sort_and_show(self, screen):
        # 根据 z 排序
        self.spirits.sort(key=lambda s: (s.z,s.rect.bottom))
        # 依次调用 show 方法
        for spirit in self.spirits:
            if spirit.z==0:
                pass
            else:
               spirit.show(screen)
spirit_show_manager=SpiritManager()