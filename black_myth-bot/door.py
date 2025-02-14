import pygame
import camera
import pytmx
class DoorLike():
    def __init__(self,id,rect,tarmap,x,y,group):
        self.rect=rect
        self.x=x
        self.y=y
        self.map=tarmap
        self.id=id
        group.list.append(self)
    def listen(self,playerrect,nowmap,event_que):
        for i in event_que.queue:
            if i.type==pygame.KEYDOWN and i.event.key==pygame.K_e and self.rect.colliderect(playerrect):
                event_que.queue.remove(i)
                return False
        return True

    def draw(self, screen,camera: tuple[int, int]):  # 定义显示实体的方法，该方法在场景需要描绘图像的时候调用
        self.rect.x=self.rect.x+camera[0]
        self.rect.y=self.rect.y+camera[1]
        # 根据摄像头的位置计算实际要描绘的位置，例如摄像头往上了，实际描绘的位置就要往下
        # 实际上就是将该实体的横纵坐标分别减去摄像头左上角的坐标
        #pygame.draw.rect(screen, (0, 255, 0), self.rect)


class door_group():
    def __init__(self):
        self.list=[]
    def listen(self,gamer,nowmap,event_que):
        touchrect=pygame.Rect(gamer.imgstate.rect.x,gamer.imgstate.rect.y,gamer.imgstate.width,gamer.imgstate.height)
        permit=True
        for i in self.list:
            permit=i.listen(touchrect,nowmap,event_que)
            if permit==False:
                return (i.map,i.x,i.y)
    
        if permit==True:     
            return (nowmap,gamer.imgstate.rect.x,gamer.imgstate.rect.y)
    def draw(self,screen,camera):
        for i in self.list:
            i.draw(screen,camera)





def get_door(tmx_data, layer_name,tarmap,group,dx,dy):
    # 查找指定的对象层
    object_layer = next((layer for layer in tmx_data.objectgroups if layer.name == layer_name), None)
    if not object_layer:
        print(f"Object layer '{layer_name}' not found.")
        return

    # 遍历对象层中的每个对象并打印其属性
    for obj in object_layer:

        rect=pygame.Rect(obj.x-dx,obj.y-dy,obj.width,obj.height)
        if obj.id==142:
            DoorLike(obj.id,rect,tarmap,rect.x-200,60,group)
        if obj.id==143:
            DoorLike(obj.id,rect,tarmap,rect.x+100,60,group)
        if obj.id==185:
            DoorLike(obj.id,rect,tarmap,200,200,group)
 
