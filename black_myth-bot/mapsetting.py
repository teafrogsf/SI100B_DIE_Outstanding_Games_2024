import pytmx
import pygame
import animation
from animation import spirit_show_manager
import random
import camera
from player_code import player
import entity
import door


pygame.display.set_mode((1200,800))
class Tilemap():
    def __init__(self,filename,x_c=0,y_c=0):
        self.tmx_data = pytmx.load_pygame(filename)        # 加载TMX文件
        self.tilesize=32
        self.width = self.tmx_data.width * self.tilesize
        self.height = self.tmx_data.height * self.tilesize
        self.objects = {}
        self.tile_list=[]
        self.animations=[]
        self.object_3d=[]
        self.object_name={}
        self.x_c=x_c
        self.y_c=y_c
        self.battle=self.find_object_in_tiled_map("战斗区域","战斗区域")
        self.battle_rect=pygame.Rect(self.battle.x-self.x_c*self.tilesize,self.battle.y-self.y_c*self.tilesize,self.battle.width,self.battle.height)
    def tile_spirit(self,layer_name,z=1):
        for x,y,surf in self.tmx_data.get_layer_by_name(f"{layer_name}").tiles():
            self.tile_list.append(animation.Spirit_state(surf,(x-self.x_c)*self.tilesize,(y-self.y_c)*self.tilesize,z))
    def object_name_get(self,layer_name):
        object_layer = self.tmx_data.get_layer_by_name(layer_name)
        for obj in object_layer:
            if hasattr(obj, 'width') and hasattr(obj, 'height'):
                self.object_name[obj.name]={"obj":obj,"w_h":True}
            else:
                self.object_name[obj.name]={"obj":obj,"w_h":False}
    def ani_tile_spirit(self,layer_name,z=1):
        for layer in self.tmx_data.visible_layers:
          if layer.name == layer_name:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    properties = self.tmx_data.get_tile_properties_by_gid(gid)
                    if properties and 'frames' in properties:
                        frames = properties['frames']
                        ani_spd = random.randint(int(sum(frame.duration for frame in frames)*1.25 / len(frames)),int(sum(frame.duration for frame in frames)*1.5 / len(frames)))  # 平均帧持续时间作为动画速度
                        imglist = [self.tmx_data.get_tile_image_by_gid(frame.gid) for frame in frames]
                        animation0 = animation.Animation_Simple(base_name=None, scale=1, ani_spd=ani_spd, imglist=imglist)
                        animation0.start_animation()
                        spirit0 = animation.Spirit_state(animation0.ani_img, (x-self.x_c)* self.tilesize, (y-self.y_c)* self.tilesize, z)
                        self.animations.append({"ani":animation0,"spi":spirit0})
                        self.tile_list.append(spirit0)
    def find_object_in_tiled_map(self,object_layer_name,object_name):
        # 获取特定名称的对象层
        object_layer = self.tmx_data.get_layer_by_name(object_layer_name)
        found_object = None
        # 遍历对象层中的所有对象
        for obj in object_layer:
            # 查找具有特定名称的对象
            if obj.name == object_name:
                found_object = obj
                break
        return found_object
    def update(self):
        """更新所有动画和关联的精灵状态"""
        for i in self.animations:
                i["ani"].update()
                i["spi"].image =i["ani"].ani_img  # 更新精灵的图像
    def tile_show(self,x_c,y_c):
        self.battle_rect.x+=x_c
        self.battle_rect.y+=y_c
        self.update()
        for i in self.tile_list:
            i.show_j(x_c,y_c)
    def add_list(self):
        for i in self.tile_list:
            spirit_show_manager.add_spirit(i)
    def delet_list(self):
        for i in self.tile_list:
            spirit_show_manager.delet_spirit(i)

tutoral=Tilemap("material/2.4/教程图.tmx",20.5,43)
tutoral.tile_spirit("地板",z=2)
tutoral.ani_tile_spirit("河流",z=1)
tutoral.tile_spirit("建筑",z=6)
tutoral.tile_spirit("建筑装饰",z=7)
tutoral.tile_spirit("地板装饰",z=4)
tutoral.tile_spirit("栏杆障碍",z=6)
tutoral.add_list()

colliongroup_tutoral=entity.collion_group()
doorgroup_tutoral=door.door_group()


boss=Tilemap("material/2.9/boss.tmx")
boss.tile_spirit("地板",z=2)
boss.tile_spirit("建筑",z=6)
boss.tile_spirit("建筑装饰",z=7)
boss.tile_spirit("装饰",z=4)
boss.tile_spirit("墙",z=6)
boss.add_list()

colliongroup_boss=entity.collion_group()
doorgroup_boss=door.door_group()


class Map_manager:
    def __init__(self):
        self.dict={}
    def add_map(self,name,tilemap,collion_group,doorgroup,collion_layer_name,door_layer_name,x=0,y=0,player=player):
        entity.get_collion(tilemap.tmx_data,collion_layer_name,collion_group,-x*tilemap.tilesize,-y*tilemap.tilesize)
        camera1=camera.SceneLike(player.imgstate.rect,tilemap.width,tilemap.height,x*tilemap.tilesize,y*tilemap.tilesize)
        door.get_door(tilemap.tmx_data,door_layer_name,'tutoral',doorgroup,-x*tilemap.tilesize,-y*tilemap.tilesize)
        self.dict[name]={"map":tilemap,"camera":camera1,"entity_group":collion_group,"door":doorgroup}

map_manager=Map_manager()
map_manager.add_map("tutoral",tutoral,colliongroup_tutoral,doorgroup_tutoral,"物体",'可交互',x=-20.5,y=-43)


map_manager.add_map("boss",boss,colliongroup_boss,doorgroup_boss,"物体",'可交互')






