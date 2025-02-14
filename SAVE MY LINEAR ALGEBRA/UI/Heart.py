from pygame import *
from Statics import *
from TmpTools.tools import *
from BGMPlayer import BGMPlayer


class Heart(pygame.sprite.Sprite):
    bgm_player = BGMPlayer()

    def __init__(self):
        super().__init__()
        self.frame = []
        self.frame_index = 0
        self.frame_rects = HeartSettings.heart_frame_rects
        self.sheet = pygame.image.load(ImportedImages.heartImage)
        for i in range(len(self.frame_rects)):
            tmp_image = get_images(self.sheet, *self.frame_rects[i], (0, 0, 0), 3.0)
            self.frame.append(
                pygame.transform.scale(
                    tmp_image, (HeartSettings.heartWidth, HeartSettings.heartHeight)
                )
            )
        self.image = self.frame[0]
        self.rect = self.image.get_rect()
        self.rect.x = UISettings.heart.x
        self.rect.y = UISettings.heart.y
        self.HP = PlayerSettings.PlayerHP
        self.state = "normal"
        self.timer = 0

    def update(self):
        current_time = pygame.time.get_ticks()
        if self.state == "reduce" and current_time - self.timer > 1000:
            self.HP -= 1 + BasicSettings.Hardship_coefficient // 2
            self.timer = current_time
            Heart.bgm_player.play_sound_effect("ISAAC_HURT")

        else:
            self.state = "normal"

        if self.HP <= 0:
            event.post(event.Event(Events.GAME_OVER))
            self.HP = 0
            # 触发事件游戏结束
        self.image = self.frame[6 - self.HP]
