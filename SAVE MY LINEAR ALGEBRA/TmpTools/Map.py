import pygame
import random

class MapTree:
    def __init__(self, id, value):
        self.value = value
        self.id  = id
        self.left = None
        self.right = None
        self.father = None

RoomTree = []  #记录房间关系

scene_choices = ["COMMON_ROOM","SHOP","TREASURE","SECRET","BLUEWOMB"]
root = "START_ROOM"
    
max_depth = 4 
RoomType = []
RoomType.append(" ")
catacombPlace = random.choice([9,11,13,15])
for i in range(1,2**max_depth):
    x = random.choice(scene_choices)
    if i == catacombPlace:
        x = "CATACOMB"
    if i == 1:  
        x = root
    RoomType.append(x)


def add_children(node, depth, shop_added, treasure_added, catacomb_added):
    if depth == max_depth:
        RoomTree.append(node)
        return

    choices = scene_choices.copy()

    if choices:
        leftson = RoomType[node.id * 2]
        rightson = RoomType[node.id * 2 + 1]

        node.left = MapTree(node.id * 2, leftson)
        node.left.father = node
        node.right = MapTree(node.id * 2 + 1, rightson)
        node.right.father = node
        RoomTree.append(node)


    if node.left:
        add_children(
            node.left, 
            depth + 1, 
            node.left in ["SHOP"] or shop_added,
            node.left in ["TREASURE"] or treasure_added,
            node.left in ["CATACOMB"] or catacomb_added
            )
    if node.right:
        add_children(
            node.right, 
            depth + 1, 
            node.right in ["SHOP"] or shop_added,
            node.right in ["TREASURE"] or treasure_added,
            node.right in ["CATACOMB"] or catacomb_added
        )

root_node = MapTree(1, root)
add_children(root_node, 1, False, False, False)
RoomTree.append(MapTree(
    value = "None",
    id = 0
))
RoomTree.sort(key=lambda room: room.id)
BossRoom_location = 1
for room in RoomTree:
    if room.value == "CATACOMB":
        BossRoom_location = room.id