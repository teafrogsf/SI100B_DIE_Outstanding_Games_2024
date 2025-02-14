import pygame
from Statics import *


# BGM settings
class BGMPlayer:
    def __init__(self):
        pygame.mixer.init()
        # bgms
        self.current_BGM = None
        self.BGM_position = 0  # store the position of BGM (in milliseconds)
        self.main_theme_BGM = ImportedBGM.main_theme
        self.common_BGM = ImportedBGM.common_bgm
        self.load_BGM(self.common_BGM)

        # sound effects
        self.isaac_walk_sound = pygame.mixer.Sound(ImportedBGM.walk)
        self.isaac_shoot_sound = pygame.mixer.Sound(ImportedBGM.shoot)
        self.isaac_hurt_sound = pygame.mixer.Sound(ImportedBGM.hurt)
        self.bomb_explode_sound = pygame.mixer.Sound(ImportedBGM.explosion)
        self.tear_hit_sound = pygame.mixer.Sound(ImportedBGM.tear_impact)
        self.door_open_sound = pygame.mixer.Sound(ImportedBGM.door_open)
        self.channel = None

    def load_BGM(self, BGM_file):
        pygame.mixer_music.load(BGM_file)
        self.current_BGM = BGM_file  # Keep track of the current track

    def play_BGM(self):
        if self.current_BGM:
            pygame.mixer_music.play(
                -1, start=self.BGM_position / 1000
            )  # in seconds, why conflict??

    def get_BGM_current_pos(self):
        self.BGM_position += (
            pygame.mixer_music.get_pos()
        )  # Get the current position (in milliseconds)

    def switch_BGM(self, BGM_type: str):
        match BGM_type:
            case "MAIN_THEME":
                self.load_BGM(self.main_theme_BGM)
            case "COMMON":
                self.load_BGM(self.common_BGM)
        self.play_BGM()

    def stop_BGM(self):
        pygame.mixer_music.stop()

    def play_sound_effect(self, sound):
        if sound == "ISAAC_WALK":
            self.channel = self.isaac_walk_sound.play()  # default:0 play once
        if sound == "ISAAC_SHOOT":
            self.channel = self.isaac_shoot_sound.play()
        if sound == "ISAAC_HURT":
            self.channel = self.isaac_hurt_sound.play()
        if sound == "BOMB_EXPLODE":
            self.channel = self.bomb_explode_sound.play()
        if sound == "TEAR_HIT":
            self.channel = self.tear_hit_sound.play()
        if sound == "DOOR_OPEN":
            self.channel = self.door_open_sound.play()
