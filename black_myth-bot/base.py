import pygame
import sys
pygame.init()

class Event:  # 定义事件类，属性包括用于区分事件种类的编号，以及可选参数body传递一些信息
    def __init__(self, code: int, event, body={}):
        self.code = code
        self.body = body
        self.event = event
        self.type = event.type
# 定义不同种类事件的编号
DRAW = 1
STEP = 2
REQUEST_MOVE = 3
CAN_MOVE = 4
SYSTEM=0

class Event_queue():
    def __init__(self):
        self.queue=[]
    def add(self,event):
        self.queue.append(event)
    def pop(self):
        if len(self.queue)==0:
            return None
        else:
            return self.queue.pop(0)
    def get(self):
        if len(self.queue)==0:
            return None
        else:
            return self.queue[0]
    def clear(self):
        self.queue=[]
    def fill(self):
        for event in pygame.event.get():
            self.add(Event(SYSTEM,event))

def process(que_list):
    for event in que_list:
        if event.type == pygame.QUIT:
            sys.exit()
    
# 坐标相关
def distance(a,b):
    return ((a[0]-b[0])**2+(a[1]-b[1])**2)**0.5
def relative_loc(a,b):
    return (a[0]-b[0],b[1]-a[1])

def dis_in(a,x1,x2):
    if a>x1 and a<x2:
        return True
    else:
        return False
    
class MusicManager:
    def __init__(self):
        # 初始化混音器模块
        pygame.mixer.init()
        self.music_files = {}
        self.current_music = None

    def add_music(self, name, path, volume=0.5):
        """添加音乐到管理器中"""
        if name not in self.music_files:
            self.music_files[name] = {'path': path, 'volume': volume}
            if len(self.music_files) == 1:
                # 如果是第一次添加音乐，则自动加载并播放
                self.play(name)

    def play(self, name):
        """播放指定名称的音乐"""
        if name in self.music_files and name != self.current_music:
            music_info = self.music_files[name]
            pygame.mixer.music.load(music_info['path'])
            pygame.mixer.music.set_volume(music_info['volume'])
            pygame.mixer.music.play(-1)  # -1 表示无限循环播放
            self.current_music = name

    def pause(self):
        """暂停当前播放的音乐"""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()

    def unpause(self):
        """恢复暂停的音乐"""
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.unpause()

    def stop(self):
        """停止当前播放的音乐"""
        pygame.mixer.music.stop()
        self.current_music = None

musicmanager=MusicManager()
musicmanager.add_music("menu", "material/2.5/menu.mp3", volume=0.5)
musicmanager.add_music("normal", "material/2.5/country.mp3", volume=0.5)
musicmanager.add_music("battle", "material/2.5/battle.mp3", volume=0.5)