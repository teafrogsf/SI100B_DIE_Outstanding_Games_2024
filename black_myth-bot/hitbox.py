import pygame


class Hitbox():  
    def __init__(self,rel_x,rel_y,width,height,name,damage):
        self.name=name
        self.width=width
        self.height=height
        self.dx=rel_x
        self.dy=rel_y       
        self.rect=None
        self.damage=damage
    def creat(self, player):  
        if player.direc=='u':
            self.x=player.imgstate.rect.center[0]+self.dy
            self.y=player.imgstate.rect.center[1]-self.dx
            twidth,theight=self.height,self.width
        if player.direc=='r':
            self.x=player.imgstate.rect.center[0]+self.dx
            self.y=player.imgstate.rect.center[1]+self.dy
            twidth,theight=self.width,self.height
        if player.direc=='l':
            self.x=player.imgstate.rect.center[0]-self.dx
            self.y=player.imgstate.rect.center[1]-self.dy
            twidth,theight=self.width,self.height
        if player.direc=='d':
            self.x=player.imgstate.rect.center[0]-self.dy
            self.y=player.imgstate.rect.center[1]+self.dx
            twidth,theight=self.height,self.width
        self.rect=pygame.Rect(self.x-twidth*0.5,self.y-theight*0.5,twidth,theight)
    def vanish(self):
        self.rect=None
    def listen(self, target_rect):
        if self.rect.colliderect(target_rect) :
            return False
        else :
            return True

class Hitboxes():
    def __init__(self):
        self.dict={}
        self.list=[]
    def add(self,hitbox):
        self.dict[hitbox.name]={"hitbox":hitbox,"damage":hitbox.damage}
        self.list.append(hitbox)
    def add_list(self,hitbox):
        self.list.append(hitbox)
    def listen(self,target_rect):
        for values in self.dict.valules():
            if values["hitbox"].rect !=None:
                if values["hitbox"].listen(target_rect)==False:
                    return(False,values["damage"])
        return(True,0)        
    def list_listen(self,target_rect):
        for i in self.list:
            if i.rect !=None:
                if i.listen(target_rect)==False:
                    return(False,i.damage)
        return(True,0)        
    def vanish(self):
        for values in self.dict.values():
            values["hitbox"].vanish()