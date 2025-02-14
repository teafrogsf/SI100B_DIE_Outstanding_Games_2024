from pygame import *
from Statics import *
import random
from TmpTools.Map import *


class SingleRoom(pygame.sprite.Sprite):
    def __init__(self, RoomID, roomImage=None, rect: pygame.Rect = None, Wall_Type=0):
        super().__init__()
        # randomly select a room image if not specified
        # if not roomImage:
        #     self.image = pygame.image.load(
        #         random.choice(list(ImportedImages.RoomImages)).value
        #     )
        # else:
        self.image = pygame.image.load(roomImage)
        self.image = pygame.transform.scale(
            self.image, (BasicSettings.screenWidth, BasicSettings.screenHeight)
        )
        if not rect:
            self.rect = self.image.get_rect()
        else:
            self.rect = rect

        self.RoomID = RoomID

        self._frame = pygame.sprite.Group()
        self._frame.empty()
        self.set_frame()
        self._walls = pygame.sprite.Group()
        self._walls.empty()
        self.gen_walls(Wall_Type)
        self._doors = pygame.sprite.Group()
        self._doors.empty()
        self.gen_doors()

    # property without setter
    def get_frame(self):
        return self._frame

    def get_walls(self):
        return self._walls

    def get_doors(self):
        return self._doors

    def set_frame(self):
        edge_thickness = 1
        self.top_edge = pygame.Rect(
            BasicSettings.marginWidth,
            BasicSettings.marginHeight - edge_thickness - 20,
            self.rect.width,
            edge_thickness,
        )
        self.bottom_edge = pygame.Rect(
            BasicSettings.marginWidth,
            BasicSettings.roomHeight - edge_thickness + 20,
            self.rect.width,
            edge_thickness,
        )
        self.left_edge = pygame.Rect(
            BasicSettings.marginWidth - edge_thickness - 20,
            BasicSettings.marginHeight,
            edge_thickness,
            self.rect.height,
        )
        self.right_edge = pygame.Rect(
            BasicSettings.roomWidth - edge_thickness + 20,
            BasicSettings.marginHeight,
            edge_thickness,
            self.rect.height,
        )
        edges = [self.top_edge, self.bottom_edge, self.left_edge, self.right_edge]
        for i in range(4):
            self._frame.add(Frame(edges[i]))

    def gen_doors(self):
        # generate four random doors
        door_locations = {
            "top": (self.rect.width / 2, BasicSettings.marginHeight + 10),
            "left": (BasicSettings.marginWidth - 25, self.rect.height / 2),
            "bottom": (self.rect.width / 2, BasicSettings.roomHeight - 10),
            "right": (BasicSettings.roomWidth + 10, self.rect.height / 2),
        }
        door_location_tags = ["top", "left", "bottom", "right"]
        if self.RoomID % 2 == 1 and self.RoomID > 1:  # 从左边进来
            door = Door(door_location_tags[1], self.RoomID)
            door.image = pygame.transform.rotate(door.image, 90 * 1)
            door.rect.center = door_locations[door_location_tags[1]]
            self._doors.add(door)
        if self.RoomID % 2 == 0:  # 从上边进来
            door = Door(door_location_tags[0], self.RoomID)
            door.image = pygame.transform.rotate(door.image, 90 * 0)
            door.rect.center = door_locations[door_location_tags[0]]
            self._doors.add(door)
        for i in range(2, 4):
            if RoomTree[self.RoomID].left:
                door = Door(door_location_tags[i], self.RoomID)
                door.image = pygame.transform.rotate(door.image, 90 * i)
                door.rect.center = door_locations[door_location_tags[i]]
                self._doors.add(door)
        self._doors.draw(self.image)  # draw on the Room's frame

    def gen_walls(self, mode):
        if mode == 1:
            # 模式一：在整个房间生成一整列一整列的墙体
            columns = random.randint(3, 4)  # 随机生成列数
            spacing = (
                BasicSettings.roomWidth - BasicSettings.marginWidth * 2
            ) // columns
            for i in range(columns):
                x = BasicSettings.marginWidth + i * spacing + spacing // 2
                for y in range(
                    BasicSettings.marginHeight,
                    BasicSettings.roomHeight,
                    Shit().image.get_height(),
                ):
                    wall = Shit()
                    if (
                        y > BasicSettings.marginHeight + Shit().image.get_height()
                        and y < BasicSettings.roomHeight - Shit().image.get_height()
                    ):
                        wall.rect.center = (x, y)
                        self._walls.add(wall)

        elif mode == 2:
            # 模式二：在房间的四角生成单独的墙体，不紧挨着边框
            corner_offsets = [
                (BasicSettings.marginWidth + 100, BasicSettings.marginHeight + 100),
                (BasicSettings.roomWidth - 100, BasicSettings.marginHeight + 100),
                (BasicSettings.marginWidth + 100, BasicSettings.roomHeight - 100),
                (BasicSettings.roomWidth - 100, BasicSettings.roomHeight - 100),
            ]
            for offset in corner_offsets:
                wall = Shit()
                wall.rect.center = offset
                self._walls.add(wall)

        elif mode == 3:
            # 模式三：在房间的中心生成 4x4 的墙体
            center_x = (BasicSettings.marginWidth + BasicSettings.roomWidth) // 2
            center_y = (
                BasicSettings.marginHeight + BasicSettings.roomHeight
            ) // 2 + 100
            wall_width = Shit().image.get_width()
            wall_height = Shit().image.get_height()

            start_x = center_x - (wall_width * 2.5)
            start_y = center_y - (wall_height * 2.5)

            for i in range(4):
                for j in range(4):
                    wall = Shit()
                    wall.rect.center = (
                        start_x + i * wall_width,
                        start_y + j * wall_height,
                    )
                    self._walls.add(wall)

        num_rocks = 0
        if mode != 0:
            num_rocks = random.randint(1, 5)
        for _ in range(num_rocks):
            while True:
                x = random.randint(
                    BasicSettings.marginWidth + 150,
                    BasicSettings.roomWidth - BasicSettings.marginWidth - 150,
                )
                y = random.randint(
                    BasicSettings.marginHeight + 150,
                    BasicSettings.roomHeight - BasicSettings.marginHeight - 150,
                )
                rock = Rock()
                rock.rect.center = (x, y)

                if not any(wall.rect.colliderect(rock.rect) for wall in self._walls):
                    self._walls.add(rock)
                    break

    def open_doors(self):
        for door in self._doors:
            door: Door
            door._is_open = True
            match door.type_tag:
                case "Wood":
                    door.image = pygame.image.load(
                        ImportedImages.OpenDoorImages.OPEN_WOOD_DOOR.value
                    )
                case "Shop":
                    door.image = pygame.image.load(
                        ImportedImages.OpenDoorImages.OPEN_SHOP_DOOR.value
                    )
                case "Treasure":
                    door.image = pygame.image.load(
                        ImportedImages.OpenDoorImages.OPEN_TREASURE_DOOR.value
                    )
                case "Secret":
                    door.image = pygame.image.load(
                        ImportedImages.OpenDoorImages.OPEN_SECRET_DOOR.value
                    )
                case "BlueWomb":
                    door.image = pygame.image.load(
                        ImportedImages.OpenDoorImages.OPEN_BLUEWOMB_DOOR.value
                    )
                case "Catacomb":
                    door.image = pygame.image.load(
                        ImportedImages.OpenDoorImages.OPEN_CATACOMB_DOOR.value
                    )
            door.image = pygame.transform.scale(
                door.image,
                (PlayerSettings.playerWidth * 1.5, PlayerSettings.playerHeight * 1.3),
            )
            match door.location_tag:
                case "left":
                    door.image = pygame.transform.rotate(door.image, 90)
                case "bottom":
                    door.image = pygame.transform.rotate(door.image, 90 * 2)
                case "right":
                    door.image = pygame.transform.rotate(door.image, 90 * 3)
        self._doors.draw(self.image)


class Door(pygame.sprite.Sprite):
    def __init__(self, location_tag: str, roomID: int):
        super().__init__()
        # randomly select a door image if not specified
        # if not image_path:
        #     self._image_path = random.choice(
        #         list(ImportedImages.ClosedDoorImages)
        #     ).value
        f = RoomTree[roomID].father
        r = RoomTree[roomID].right
        l = RoomTree[roomID].left
        match location_tag:
            case "left":
                DoorType = f.value
            case "top":
                DoorType = f.value
            case "right":
                DoorType = r.value
            case "bottom":
                DoorType = l.value
        # print(roomID, location_tag, DoorType)
        self._image_path = random.choice(list(ImportedImages.ClosedDoorImages)).value
        match DoorType:
            case "COMMON_ROOM":
                self._image_path = (
                    ImportedImages.ClosedDoorImages.CLOSED_WOOD_DOOR.value
                )
            case "SHOP":
                self._image_path = (
                    ImportedImages.ClosedDoorImages.CLOSED_SHOP_DOOR.value
                )
            case "TREASURE":
                self._image_path = (
                    ImportedImages.ClosedDoorImages.CLOSED_TREASURE_DOOR.value
                )
            case "BLUEWOMB":
                self._image_path = (
                    ImportedImages.ClosedDoorImages.CLOSED_BLUEWOMB_DOOR.value
                )
            case "CATACOMB":
                self._image_path = (
                    ImportedImages.ClosedDoorImages.CLOSED_CATACOMB_DOOR.value
                )
            case "SECRET":
                self._image_path = (
                    ImportedImages.ClosedDoorImages.CLOSED_SECRET_DOOR.value
                )
            case "START_ROOM":
                self._image_path = (
                    ImportedImages.ClosedDoorImages.CLOSED_WOOD_DOOR.value
                )

        self.image = pygame.image.load(self._image_path)
        self.image = pygame.transform.scale(
            self.image,
            (PlayerSettings.playerWidth * 1.5, PlayerSettings.playerHeight * 1.3),
        )
        self.rect = self.image.get_rect()
        self.location_tag = location_tag
        self._is_open = False
        self.type_tag = None
        match self._image_path:
            case ImportedImages.ClosedDoorImages.CLOSED_WOOD_DOOR.value:
                self.type_tag = "Wood"
            case ImportedImages.ClosedDoorImages.CLOSED_SHOP_DOOR.value:
                self.type_tag = "Shop"
            case ImportedImages.ClosedDoorImages.CLOSED_TREASURE_DOOR.value:
                self.type_tag = "Treasure"
            case ImportedImages.ClosedDoorImages.CLOSED_SECRET_DOOR.value:
                self.type_tag = "Secret"
            case ImportedImages.ClosedDoorImages.CLOSED_BLUEWOMB_DOOR.value:
                self.type_tag = "BlueWomb"
            case ImportedImages.ClosedDoorImages.CLOSED_CATACOMB_DOOR.value:
                self.type_tag = "Catacomb"

    @property
    def is_open(self):
        return self._is_open

    @is_open.setter
    def is_open(self, value: bool):
        self._is_open = value

    @property
    def image_path(self):
        return self._image_path

    @image_path.setter
    def image_path(self, value: str):
        self._image_path = value


class Frame(pygame.sprite.Sprite):
    def __init__(self, rect: pygame.Rect):
        super().__init__()
        self.rect = rect


class Wall(pygame.sprite.Sprite):
    def __init__(self, wall_image, HP=3):
        super().__init__()
        self.image = wall_image
        self.HP = HP
        self.image = pygame.transform.scale(
            self.image,
            (PlayerSettings.playerWidth * 0.8, PlayerSettings.playerHeight * 0.8),
        )
        self.rect = self.image.get_rect()


class Shit(Wall):
    def __init__(self):
        shit_image = pygame.image.load(ImportedImages.ShitImages["TYPE_0"].value)
        HP = 5
        super().__init__(shit_image, HP)

    def destroyed(self):
        if self.HP <= 0:
            self.kill()
        else:
            new_image_key = f"TYPE_{int(5 - self.HP)}"
            self.image = pygame.image.load(
                ImportedImages.ShitImages[new_image_key].value
            )
            self.image = pygame.transform.scale(
                self.image,
                (
                    PlayerSettings.playerWidth * 0.8,
                    PlayerSettings.playerHeight * 0.8,
                ),
            )
            self.rect = self.image.get_rect(center=self.rect.center)


class Block(Wall):
    def __init__(self, block_image):
        super().__init__(block_image)

    def destroyed(self):
        if self.HP <= 0:
            self.kill()


def divide_image(img, index):
    image_width, image_height = img.get_size()
    part_width = image_width // index
    elements = []
    for i in range(index):
        rect = pygame.Rect(i * part_width, 0, part_width, image_height)
        part = img.subsurface(rect).copy()
        elements.append(part)
    return elements


class Rock(Block):
    def __init__(self):
        self.image = divide_image(
            pygame.image.load(ImportedImages.BlockImage.Rock.value), 3
        )[0]
        super().__init__(self.image)


class Black_Treasure_Box(Block):
    def __init__(self):
        self.image = divide_image(
            pygame.image.load(ImportedImages.BlockImage.Rock.value), 3
        )[1]
        super().__init__(self.image)


class Gold_Treasure_Box(Block):
    def __init__(self):
        self.image = divide_image(
            pygame.image.load(ImportedImages.BlockImage.Rock.value), 3
        )[2]
        super().__init__(self.image)


class Web(pygame.sprite.Sprite):
    def __init__(self):
        self.image = divide_image(
            pygame.image.load(ImportedImages.BlockImage.Rock.value), 4
        )[0]


class StartRoom(SingleRoom):
    def __init__(self, RoomID, rect: pygame.Rect = None):
        wall_type = 0
        super().__init__(
            RoomID, ImportedImages.RoomImages.START_ROOM.value, rect, wall_type
        )


class CommonRoom(SingleRoom):
    def __init__(self, RoomID, rect: pygame.Rect = None):
        wall_type = random.randint(1, 3)
        super().__init__(
            RoomID, ImportedImages.RoomImages.COMMON_ROOM.value, rect, wall_type
        )


class Shop(SingleRoom):
    def __init__(self, RoomID, rect: pygame.Rect = None):
        wall_type = 0
        super().__init__(RoomID, ImportedImages.RoomImages.SHOP.value, rect, wall_type)


class TreasureRoom(SingleRoom):
    def __init__(self, RoomID, rect: pygame.Rect = None):
        wall_type = 0
        super().__init__(
            RoomID, ImportedImages.RoomImages.TREASURE.value, rect, wall_type
        )


class SecretRoom(SingleRoom):
    def __init__(self, RoomID, rect: pygame.Rect = None):
        wall_type = random.randint(1, 3)
        super().__init__(
            RoomID, ImportedImages.RoomImages.SECRET.value, rect, wall_type
        )


class BlueWomb(SingleRoom):
    def __init__(self, RoomID, rect: pygame.Rect = None):
        wall_type = random.randint(1, 3)
        super().__init__(
            RoomID, ImportedImages.RoomImages.BLUEWOMB.value, rect, wall_type
        )


class BossRoom(SingleRoom):
    def __init__(self, RoomID, rect: pygame.Rect = None):
        wall_type = random.randint(1, 3)
        super().__init__(
            RoomID, ImportedImages.RoomImages.CATACOMB.value, rect, wall_type
        )
