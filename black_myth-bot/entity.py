
import pygame
import dialog
import animation
from animation import spirit_show_manager

class EntityLike():  # 实体类
    def __init__(self,rect,group):
        self.rect=rect
        group.list.append(self)
    def listen(self, target_rect, now_rect):
        if self.rect.colliderect(target_rect) :
            a=0
            b=0
            c=True
            if self.rect.colliderect(now_rect) :
                for i in [-1,1,-2,2,-3,3]:
                    now_rect.y+=i
                    if self.rect.colliderect(now_rect):
                            pass
                    else:
                            b=i
                            c=False
                            break
                if c:
                    for j in [-1,1,-2,2,-3,3]:
                        now_rect.x+=j
                        if self.rect.colliderect(now_rect):
                                pass
                        else:
                                a=i
                                c=False
                                break
                if c:
                    for i in [-1,1,-2,2,-3,3]:
                        for j in [-1,1,-2,2,-3,3]:
                            now_rect.x+=j
                            now_rect.y+=i
                            if self.rect.colliderect(now_rect):
                                pass
                            else:
                                a,b=j,i
                                c=False
                                break
                if c:
                    for i in [-4.4,-5,5,-6,6]:
                        now_rect.y+=i
                        if self.rect.colliderect(now_rect):
                                pass
                        else:
                                b=i
                                c=False
                                break
            return [True,a,b]
        else :
            return [False,0,0]
   
    def draw(self,screen,camera: tuple[int, int]):  # 定义显示实体的方法，该方法在场景需要描绘图像的时候调用
        self.rect.x=self.rect.x+camera[0]
        self.rect.y=self.rect.y+camera[1]
        pygame.draw.rect(screen, (0, 128, 255), self.rect,2)


class collion_group():
    def __init__(self):
        self.list=[]
    def listen(self,gamer):
        touchrect=pygame.Rect(gamer.imgstate.rect.x+gamer.stepx,gamer.imgstate.rect.y+gamer.stepy,gamer.imgstate.rect.width,gamer.imgstate.rect.height)
        nowrect=pygame.Rect(gamer.imgstate.rect.x,gamer.imgstate.rect.y,gamer.imgstate.rect.width,gamer.imgstate.rect.height)
        permit=[False,0,0]
        for i in self.list:
            permit=i.listen(touchrect,nowrect)
            if permit[0]:
                return permit
        else:
            return permit
    def draw(self,screen,camera):
        for i in self.list:
            i.draw(screen,camera)

def get_collion(tmx_data, layer_name,group,dx,dy):
    # 查找指定的对象层
    object_layer = next((layer for layer in tmx_data.objectgroups if layer.name == layer_name), None)
    if not object_layer:
        print(f"Object layer '{layer_name}' not found.")
        return

    # 遍历对象层中的每个对象并打印其属性
    for obj in object_layer:
        rect=pygame.Rect(obj.x-dx,obj.y-dy,obj.width,obj.height)
        EntityLike(rect,group)
 





