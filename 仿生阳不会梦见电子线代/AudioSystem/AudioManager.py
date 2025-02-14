from Data.instance import *

import pygame,os,json,copy,random
from enum import Enum

pathcwd = os.getcwd()
def LoadAudio(typ,file):
    path = os.path.join(pathcwd,"Assets","Audio",typ.value,file)
    if os.path.exists(path):
        return path
    else:
        return None

class AudioType(Enum):
    Sound = "Effects"
    Music = "BGMs"

class Audio:
    def __init__(self,id,typ,audioSource,channel=0,volume=1,delay=0):
        self.id = id
        self.audioType = typ
        self.audioSource = audioSource
        self.channel = channel
        self.volume = volume
        self.delay = delay
        self.isPlaying = False
    def play(self):
        self.isPlaying = True
        _audio = LoadAudio(self.audioType,self.audioSource)
        if _audio == None:
            return
        if self.audioType == AudioType.Music:
            pygame.mixer.music.load(_audio)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(0,0,1000)
        else:
            pygame.mixer.Channel(self.channel).set_volume(self.volume)
            pygame.mixer.Channel(self.channel).play(pygame.mixer.Sound(_audio))
    def tick(self):
        if self.delay >= 0:
            self.delay -= 1
            if self.delay < 0:
                self.play()
        if self.isPlaying:
            if self.audioType == AudioType.Music:
                if not pygame.mixer.music.get_busy():
                    self.onEnd()
            elif self.audioType == AudioType.Sound:
                if not pygame.mixer.Channel(self.channel).get_busy():
                    self.onEnd()
    def onEnd(self):
        if self.audioType == AudioType.Music:
            audioManager.OnMusicEnd()
        else:
            audioManager.OnSoundEnd(self.id,self.channel)
    def forceEnd(self):
        if self.audioType == AudioType.Music:
            pygame.mixer.music.fadeout(1000)
        else:
            pygame.mixer.Channel(self.channel).stop()
        self.onEnd()


@instance
class AudioManager:
    def __init__(self):
        self.maxChannel = 16

        pygame.mixer.init()
        pygame.mixer.set_num_channels(self.maxChannel)

        self.AudioList = None

        self.audios = {}

        self.safeDeleteAudio = []
        self.safeAddAudio = []

        self.emptyChannel = set()
        self.emptyChannel.update([i for i in range(self.maxChannel)])

        self.musicList = None
        self.musicRule = None
        self.musicID = "BGM"

        self.LoadAudio()
    def TickingAudioFrame(self):
        for audio in self.audios.values():
            audio.tick()
        for id in self.safeDeleteAudio:
            if id in self.audios.keys():
                self.audios.pop(id)
        for audio in self.safeAddAudio:
            self.audios[audio.id] = audio
        self.safeAddAudio.clear()
        self.safeDeleteAudio.clear()
        if not self.musicID in self.audios.keys():
            self.StartRandomBGM()
    def OnMusicEnd(self):
        self.safeDeleteAudio.append(self.musicID)
    def OnSoundEnd(self,id,channel):
        if not channel in self.emptyChannel:
            self.emptyChannel.add(channel)
        #print(len(self.emptyChannel))
        self.safeDeleteAudio.append(id)
    def LoadAudio(self):
        path = os.path.join(os.getcwd(),"Assets","Audio","AudioLis.json")
        if os.path.exists(path):
            with open(path,"r",encoding="utf-8") as f:
                self.AudioList = json.load(f)
    def getEmptyChannel(self):
        if len(self.emptyChannel) == 0:
            return None
        else:
            return self.emptyChannel.pop()
    def getVolumeModify(self,nam):
        #print(self.AudioList["VolumeModify"])
        if nam in self.AudioList["VolumeModify"].keys():
            return self.AudioList["VolumeModify"][nam]
        else:
            return 1
    def getMutiModify(self,nam):
        if nam in self.AudioList["MutiModify"].keys():
            return self.AudioList["MutiModify"][nam]
        else:
            return True
    def AddEffect(self,nam,delay=0):
        if nam in self.AudioList["SoundEffect"]:
            _effect = self.AudioList["SoundEffect"][nam]
            _audioNam = None
            if self.getMutiModify(_effect):
                _channel = self.getEmptyChannel()
                _audioNam = nam+str(_channel)
            else:
                if nam in self.audios.keys():
                    return
                _channel = self.getEmptyChannel()
                _audioNam = nam
            if _channel != None and _audioNam != None:
                self.safeAddAudio.append(Audio(_audioNam,AudioType.Sound,_effect,_channel,self.getVolumeModify(_effect),delay))
    def SwitchBGMList(self,lv1,lv2,lv3=None,lv4=None):
        #UGLYYYYYYYYYYYYYYYYYY CODING
        #But I don't care )))
        if lv1 in self.AudioList:
            if lv2 in self.AudioList[lv1]:
                if isinstance(self.AudioList[lv1][lv2],list):
                    self.musicList = copy.deepcopy(self.AudioList[lv1][lv2])
                    self.musicRule = None
                elif isinstance(self.AudioList[lv1][lv2],dict):
                    self.musicList = None
                    self.musicRule = None
                    if "List" in self.AudioList[lv1][lv2].keys():
                        self.musicList = copy.deepcopy(self.AudioList[lv1][lv2]["List"])
                    if "Rule" in self.AudioList[lv1][lv2].keys():
                        self.musicRule = copy.deepcopy(self.AudioList[lv1][lv2]["Rule"])  
        if self.musicID in self.audios:
            self.audios[self.musicID].forceEnd()
    def StartRandomBGM(self):
        if self.musicList == None or len(self.musicList) == 0:
            return
        _nxtBGM = None
        if self.musicRule != None:
            if "FirstLock" in self.musicRule.keys() and self.musicRule["FirstLock"] != None:
                _nxtBGM = self.musicRule["FirstLock"]
                self.musicRule["FirstLock"] = None
        if _nxtBGM == None:
            _nxtBGM = random.sample(self.musicList,1)[0]
        print(_nxtBGM)
        self.safeAddAudio.append(Audio(self.musicID,AudioType.Music,_nxtBGM,None,self.getVolumeModify(_nxtBGM),10))

audioManager = AudioManager()