#音乐管理器
import pygame

import save.configs
from utils.util import utils


class music:  #所有的音频都放在两个列表里 music_list放世界的背景音乐 sound_list放特效音
    music_list = [r'.\assets\sound\startwindow.mp3',
                  r'.\assets\sound\background.ogg',
                  r'.\assets\sound\witchworld.mp3']
    
    sound_list = [r'.\assets\sound\sound_eatrice.mp3',
                  r'.\assets\sound\sound_pickstick.mp3',
                  r'.\assets\sound\sound_magic.mp3',
                  r'.\assets\sound\sound_click.mp3',
                  r'.\assets\sound\sound_layegg.mp3',
                  r'.\assets\sound\sound_building.mp3',
                  r'.\assets\sound\sound_nurturing.mp3']
    # 0-吃米 1-捡树枝 2-传送 3-鼠标点击 4-下蛋 5-筑鸡窝 6-进化

class music_player:
    def __init__(self):
        self.turnon_music = True  #背景音乐开关
        self.turnon_sound = True  #音效开关
        self.volume_music = 0.4  #背景音乐音量 初始为0.4
        self.volume_sound = 0.3  #音效音量 初始为0.3
        self.volume_music_before = 0.4  #背景音乐音量 初始为0.4
        self.volume_sound_before = 0.3  #音效音量 初始为0.3

        self.musicplaying = 0
        self.pausetime = [0]*len(music.music_list)
        self.sound = [0]*len(music.sound_list)


    def background_play(self, i, loop=-1):
        if self.turnon_music :
            #存储音频暂停时间
            status = pygame.mixer.music.get_busy()
            if status :
                pause = int(pygame.mixer.music.get_pos()/1000)
                self.pausetime[self.musicplaying] = pause

            #播放新音频
            pygame.mixer.music.load(music.music_list[i])
            pygame.mixer.music.play(loop)
            try:
                pygame.mixer.music.set_pos(self.pausetime[i])
            except Exception:
                print("回复暂停音频有误，从头播放")
            
            self.musicplaying = i 
            pygame.mixer.music.set_volume(self.volume_music)
    
    def background_weaken_volume(self) -> None: 
        if self.turnon_music:
            pygame.mixer.music.set_volume(0.1*int(Music_player.volume_music*5 + 1))

    def background_restore_volume(self) -> None: 
        if self.turnon_music:
            pygame.mixer.music.set_volume(Music_player.volume_music)
    
    def background_get_volume(self) : 
        if self.turnon :
            x = pygame.mixer.music.get_volume()
            return x
        else:
            return 0.0

    def sound_play(self,i):
        if self.turnon_sound :
            self.sound[i] = pygame.mixer.Sound(music.sound_list[i])
            self.sound[i].set_volume(self.volume_sound)
            self.sound[i].play()

    def sound_stop(self,i):
        if self.turnon_sound :
            self.sound[i].stop()

    def pause(self):  
        if self.turnon_music :
            #存储音频暂停时间
            status = pygame.mixer.music.get_busy()
            if status :
                pause = int(pygame.mixer.music.get_pos()/1000)
                self.pausetime[self.musicplaying] = pause
                pygame.mixer.music.stop()
    
    def background_volume_press(self, openorclose):
        if openorclose:
            if self.volume_music_before == 0.0:
                self.volume_music_before = 0.4
            pygame.mixer.music.set_volume(self.volume_music_before)
            self.volume_music = self.volume_music_before
        else:
            pygame.mixer.music.set_volume(0.0)
            self.volume_music = 0.0
        self.turnon_music = openorclose

        
    def sound_volume_press(self, openorclose):
        if openorclose:
            if self.volume_sound_before == 0.0:
                self.volume_sound_before =0.3
            self.volume_sound = self.volume_sound_before
        else:
            self.volume_sound = 0.0
        self.turnon_sound = openorclose

    def music_volume_drag(self, percentage):
        #将拖拽输入的结果立刻告诉按钮
        if percentage == 0.0:
            self.turnon_music = False
        else:
            self.turnon_music = True

        self.volume_music = percentage
        self.volume_music_before = percentage
        pygame.mixer.music.set_volume(self.volume_music)
        

    def sound_volume_drag(self, percentage):
        if percentage == 0.0:
            self.turnon_sound = False
        else:
            self.turnon_sound = True
        self.volume_sound = percentage
        self.volume_sound_before = percentage
        #音效暂时做不到实时变化 改完之后 下一次播放会有变化


    def stop(self):
        if self.turnon :
            pygame.mixer.music.stop()

    def writeConfig(self) -> dict:
        return {
            'BGM': self.turnon_music,
            'SE': self.turnon_sound,
            'BGM volume': self.volume_music if self.turnon_music else self.volume_music_before,
            'SE volume': self.volume_sound if self.turnon_sound else self.volume_sound_before,
        }
    
    def readConfig(self, data):
        self.music_volume_drag(save.configs.readElseDefault(
            data, 'BGM volume', 0.4,
            lambda x: utils.frange(x, 0, 1),
            'BGM volume must be in [0, 1]'
        ))
        self.sound_volume_drag(save.configs.readElseDefault(
            data, 'SE volume', 0.3,
            lambda x: utils.frange(x, 0, 1),
            'SE volume must be in [0, 1]'
        ))
        self.background_volume_press(save.configs.readElseDefault(
            data, 'BGM', True,
            {True: True, False: False},
            'BGM must be true or false'
        ))
        self.sound_volume_press(save.configs.readElseDefault(
            data, 'SE', True,
            {True: True, False: False},
            'SE must be true or false'
        ))

Music_player = music_player()
        

""" 
逻辑应该是：
点击关闭 音量拖拽条到0 
点击打开 音量拖拽条到上次设置的 如果没设置过 或者是0 那就是0.4

按钮为打开时 将拖拽条脱到0 按钮自动转为关闭
按钮为关闭时 将拖拽条拖到非0 按钮自动转为打开

目前实现了：
点击关闭后
self.volume_music = 0 但 self.volume_music_before 仍等于关闭前音量

点击打开后
当前音乐音量设置为self.volume_music_before 如果该值为0 则设置成0.4
音效的话 考虑到设置的时候应该没有音效 就是对下一次音效有作用（）

拖拽条：
可以通过变量 Music_player.volume_music 获得现在的音量 

函数 music_volume_drag(self, percentage) 可以percentage = 拖拽后的数
会让self.volume_music 和 self.volume_music_before一起变化
也就是当下背景音乐和“关闭前音量”一起变化

该函数会检查percentage是否为0 及时告诉bool类型的self.turnon_music 让按钮跟着变


音效同理
"""
