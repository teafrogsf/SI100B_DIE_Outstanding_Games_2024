import os.path
import random
from typing import Union

import pygame
from pygame import Surface

from LLA import chat_with_ai as ai
from entity.manager import entityManager
from interact.interacts import interact
from render import font, egg_generate
from render.renderer import renderer
from save.save import Archive
from utils.game import game
from utils.text import RenderableString, Description
from utils.util import utils
from utils.vector import Vector, BlockVector
from render.renderable import Renderable
from render.resource import Texture, resourceManager
from window.widget import Widget, Button, Location, ColorSet, PullObject, Slider
from world.world import World, WitchWorld
from music.music import Music_player


class Window(Renderable):
	"""
	窗口。窗口始终占据整个屏幕，且默认同时只会显示game.window这一个窗口。
	请注意，渲染期间不可以改变Windows._widgets的元素个数，否则会导致循环迭代器失效。更改元素没有关系。
	self._catches是捕捉控件。如果它不是None，那么所有的消息都会最先传给它，然后再根据返回值传给其他控件。
	"""
	
	def __init__(self, title: str, texture: Texture | None = None):
		"""
		:param title: 窗口标题
		:param texture: 窗口背景纹理，默认None
		"""
		super().__init__(texture)
		self._title: str = title
		self._widgets: list[Widget] = []
		self.backgroundColor: int = 0x88000000
		self.lastOpen: Union['Window', None] = None
		self._backgroundPosition = Vector()
		self._backgroundLocation = Location.LEFT_TOP
	
	def setLastOpen(self, last: 'Window') -> 'Window':
		"""
		:param last: 上一次打开的窗口
		:return: 自身
		"""
		self.lastOpen = last
		return self
	
	def renderBackground(self, delta: float, at: BlockVector = BlockVector()) -> None:
		"""
		渲染背景。可以重写
		"""
		if self._texture is not None:
			w, h = renderer.getCanvas().get_size()
			pos = BlockVector()
			match self._backgroundLocation:
				case Location.LEFT_TOP:
					pos = BlockVector(int(w * self._backgroundPosition.x), int(h * self._backgroundPosition.y))
				case Location.LEFT:
					pos = BlockVector(int(w * self._backgroundPosition.x), int(h * self._backgroundPosition.y + (h - self._texture.getUiScaledSurface().get_size()[1] >> 1)))
				case Location.LEFT_BOTTOM:
					pos = BlockVector(int(w * self._backgroundPosition.x), int(h * self._backgroundPosition.y - self._texture.getUiScaledSurface().get_size()[1]))
				case Location.TOP:
					pos = BlockVector(int(w * self._backgroundPosition.x + (w - self._texture.getUiScaledSurface().get_size()[0] >> 1)), int(h * self._backgroundPosition.y))
				case Location.CENTER:
					pos = BlockVector(int(w * self._backgroundPosition.x + (w - self._texture.getUiScaledSurface().get_size()[0] >> 1)), int(h * self._backgroundPosition.y + (h - self._texture.getUiScaledSurface().get_size()[1] >> 1)))
				case Location.BOTTOM:
					pos = BlockVector(int(w * self._backgroundPosition.x + (w - self._texture.getUiScaledSurface().get_size()[0] >> 1)), int(h * self._backgroundPosition.y - self._texture.getUiScaledSurface().get_size()[1]))
				case Location.RIGHT:
					pos = BlockVector(int(w * self._backgroundPosition.x - self._texture.getUiScaledSurface().get_size()[0]), int(h * self._backgroundPosition.y))
				case Location.RIGHT_TOP:
					pos = BlockVector(int(w * self._backgroundPosition.x - self._texture.getUiScaledSurface().get_size()[0]), int(h * self._backgroundPosition.y + (h - self._texture.getUiScaledSurface().get_size()[1] >> 1)))
				case Location.RIGHT_BOTTOM:
					pos = BlockVector(int(w * self._backgroundPosition.x - self._texture.getUiScaledSurface().get_size()[0]), int(h * self._backgroundPosition.y - self._texture.getUiScaledSurface().get_size()[1]))
			self._texture.renderAtInterface(pos)
		else:
			head = self.backgroundColor & 0xff000000
			if head == 0:
				renderer.getCanvas().fill(0)
			else:
				color = self.backgroundColor & 0xffffff
				s = Surface(renderer.getCanvas().get_size())
				s.fill(color)
				s.set_alpha(head >> 24)
				renderer.getCanvas().blit(s, (0, 0))
	
	def render(self, delta: float) -> None:
		pass
	
	def passRender(self, delta: float, at: Vector | None = None) -> None:
		self.renderBackground(delta)
		self.render(delta)
		for widget in reversed(self._widgets):
			widget.passRender(delta)
	
	def passMouseMove(self, x: int, y: int, buttons: tuple[int, int, int]) -> None:
		for widget in self._widgets:
			if widget.isMouseIn(x, y):
				widget.passHover(x, y, buttons)
	
	def passMouseDown(self, x: int, y: int, buttons: tuple[int, int, int]) -> None:
		for widget in self._widgets:
			if widget.isMouseIn(x, y):
				widget.passMouseDown(x, y, buttons)
	
	def passMouseUp(self, x: int, y: int, buttons: tuple[int, int, int]) -> None:
		for widget in self._widgets:
			if widget.isMouseIn(x, y):
				widget.passMouseUp(x, y, buttons)
	
	def passTick(self) -> None:
		for widget in self._widgets:
			widget.tick()
		self.tick()
	
	def tick(self) -> None:
		"""
		窗口的tick函数。可以重写。默认情况下，ESC会关闭当前窗口
		"""
		if interact.keys[pygame.K_ESCAPE].deals():
			game.setWindow(self.lastOpen)
	
	def onResize(self) -> None:
		"""
		窗口大小改变时的回调。可以重写，但是不要忘了令所有widgets也onResize一下
		"""
		for widget in self._widgets:
			widget.onResize()
	
	def pauseGame(self) -> bool:
		"""
		可重写。有些窗口不需要暂停游戏，重写改False就行
		"""
		return True


class FloatWindow(Renderable):
	"""
	浮动窗口。窗口会根据鼠标位置自动移动。不用继承，想显示什么直接game.floatWindow.submit()就行了，目前只支持Text
	"""
	
	def __init__(self):
		super().__init__(None)
		self._rendering: list[Description | None] = []
		self.changed = False
	
	def submit(self, contents: list[Description] | Description | None) -> None:
		"""
		把要显示的东西提交给FloatWindow
		:param contents: 要显示的RenderableString，每一行一个元素，每个RenderableString不要包含换行符
		"""
		if isinstance(contents, list):
			self._rendering = self._rendering + contents
		else:
			self._rendering.append(contents)
		self.changed = True
	
	def change(self, contents: list[Description] | Description | None) -> None:
		if contents is None:
			self._rendering = []
		elif isinstance(contents, list):
			self._rendering = contents
		else:
			self._rendering = [contents]
		self.changed = True
	
	def clear(self) -> None:
		self._rendering = []
	
	def empty(self) -> bool:
		return len(self._rendering) == 0
	
	def render(self, delta: float) -> None:
		if self._rendering is None:
			return
		info = []
		maximum = 0
		for r in self._rendering:
			for i in r.generate():
				present = i.lengthSmall()
				info.append((i, present))
				if present > maximum:
					maximum = present
		s = Surface((maximum, len(info) * font.realHalfHeight))
		s.fill((0x33, 0x33, 0x33))
		for i in range(len(info)):
			info[i][0].renderSmall(s, 0, i * font.realHalfHeight, 0xffffffff, 0xff333333)
		x, y = interact.mouse.clone().subtract(0, len(info) * font.realHalfHeight).getTuple()
		if x < 0:
			x = 0
		elif x + maximum > renderer.getCanvas().get_width():
			x = renderer.getCanvas().get_width() - maximum
		if y < 0:
			y = 0
		renderer.getCanvas().blit(s, (x, y))


class PresetColors:
	color = ColorSet()
	textColor = ColorSet()
	textColor.active = 0xff000000
	textColor.hovering = 0xffFCE8AD
	textColor.inactive = 0xff666666
	textColor.click = 0xff000000
	color.active = 0
	color.hovering = 0xff000000
	color.inactive = 0
	color.click = 0
	exitColor = ColorSet()
	exitText = ColorSet()
	exitColor.active = 0xffee0000
	exitColor.hovering = 0xffee6666
	exitColor.inactive = 0xff660000
	exitColor.click = 0xffeeaaaa
	exitText.active = 0xff000000
	exitText.hovering = 0xff000000
	exitText.inactive = 0xff000000
	exitText.click = 0xff000000
	plotColor = ColorSet()
	plotText = ColorSet()
	plotText.active = 0xffFFCA18
	plotText.hovering = 0xffFCE8AD
	plotText.inactive = 0xffFFCA18
	plotText.click = 0xffFFCA18
	plotColor.active = 0xff545454
	plotColor.hovering = 0xff7C7D7A
	plotColor.inactive = 0xffFFCA18
	plotColor.click = 0xffFFCA18


class StartWindow(Window):
	def __init__(self):
		super().__init__("Start")
		self._texture = resourceManager.getOrNew('window/start')
		self._texture.adaptsMap(False)
		self._texture.adaptsUI(False)
		self._texture.adaptsSystem(True)
		
		def _1(x, y, b) -> bool:
			if b[0] == 1:
				game.setWindow(None)
				game.setWorld(WitchWorld())
			return True
		
		self._widgets.append(Button(Location.CENTER, 0, 0.05, 0.4, 0.08, RenderableString("\\.00FCE8AD\\01LINK START"), Description([RenderableString("开始游戏")]), textLocation=Location.CENTER))
		from window.ingame import PlotWindow
		self._widgets[0].onMouseDown = lambda x, y, b: b[0] == 1 and game.setWindow(PlotWindow().setLastOpen(self)) or True
		self._widgets.append(Button(Location.CENTER, 0, 0.15, 0.4, 0.08, RenderableString("\\.00FCE8AD\\01LOAD"), Description([RenderableString("加载存档")]), textLocation=Location.CENTER))
		self._widgets[1].onMouseDown = lambda x, y, b: b[0] == 1 and game.setWindow(LoadWindow().setLastOpen(self)) or True
		self._widgets.append(Button(Location.CENTER, 0, 0.25, 0.4, 0.08, RenderableString("\\.00FCE8AD\\01OPTIONS"), Description([RenderableString("设置")]), textLocation=Location.CENTER))
		self._widgets[2].onMouseDown = lambda x, y, b: b[0] == 1 and game.setWindow(SettingsWindow().setLastOpen(self)) or True
		
		self._widgets.append(Button(Location.CENTER, 0, 0.35, 0.4, 0.08, RenderableString("\\.00FCE8AD\\01SHUT DOWN"), Description([RenderableString("结束游戏")]), textLocation=Location.CENTER))
		self._widgets[3].onMouseDown = lambda x, y, b: b[0] == 1 and game.quit() or True
		self._widgets[0].color = PresetColors.color
		self._widgets[1].color = PresetColors.color
		self._widgets[2].color = PresetColors.color
		self._widgets[3].color = PresetColors.color.clone()
		self._widgets[3].color.hovering = 0xffee0000
		self._widgets[0].textColor = PresetColors.textColor
		self._widgets[1].textColor = PresetColors.textColor
		self._widgets[2].textColor = PresetColors.textColor
		self._widgets[3].textColor = PresetColors.textColor.clone()
		self._widgets[3].textColor.hovering = 0xffeeeeee
		Music_player.background_play(0)
	
	# self._widgets.append(Button(Location.CENTER, 0, 0.45, 0.4, 0.08, RenderableString("\\.00FCE8AD\\01DEBUG"), Description([RenderableString("设置")]), textLocation=Location.CENTER))
	# self._widgets[4].onMouseDown = lambda x, y, b: b[0] == 1 and game.setWindow(GuidanceWindow().setLastOpen(self)) or True
	
	def render(self, delta: float) -> None:
		super().render(delta)
		size: BlockVector = renderer.getSize()
		renderer.renderString(RenderableString('\\.00FCE8AD\\00捡 蛋'), int(size.x / 2), int(size.y / 4), 0xff000000, Location.CENTER)
		renderer.renderString(RenderableString('\\.00FCE8AD\\02Pikyor Egg!'), int(size.x / 2), int(size.y / 4) + font.realFontHeight + 2, 0xff000000, Location.CENTER)
	
	def tick(self) -> None:
		interact.keys[pygame.K_ESCAPE].deals()  # 舍弃ESC消息


class LoadWindow(Window):
	def __init__(self):
		super().__init__("Load")
		self._widgets.append(Button(Location.LEFT_TOP, 0, 0, 0.09, 0.12, RenderableString('\\01Back'), Description([RenderableString("返回")]), Location.CENTER))
		self._widgets[0].onMouseDown = lambda x, y, b: b[0] == 1 and game.setWindow(self.lastOpen) or True
		if os.path.exists('user') and os.path.exists('user/archive'):
			def packer(s: str, bt: Button, time: int = 3):
				string, clicks, btn = s, [time], bt
				
				def _func(x, y, b):
					if not btn.active:
						return True
					if b[0] == 1:
						archive = Archive(string)
						archive.read()
						game.setWorld(World.load(archive.dic))
						game.setWindow(None)
						archive.close()
					elif b[2] == 1:
						if clicks[0] > 1:
							clicks[0] -= 1
							btn.description.d[1] = RenderableString(f"\\#ffee0000右键{clicks[0]}次以删除存档")
						else:
							archive = Archive(string)
							archive.delete()
							btn.description.d[0] = RenderableString(f"\\#ffee0000无法加载已删除的存档")
							btn.description.d[1] = RenderableString(f"\\#ffee0000存档已删除")
							btn.active = False
					return True
				
				return _func
			
			dl = os.listdir('user/archive')
			dl = [i for i in dl if i.endswith(".json")]
			self.count = len(dl)
			for i in range(self.count):
				button = Button(Location.CENTER, 0, -0.4 + i * 0.1, 0.4, 0.08, RenderableString('\\10' + dl[i][:-5]), Description([RenderableString("加载此存档"), RenderableString("\\#ffee0000右键3次以删除存档")]), Location.CENTER)
				button.onMouseDown = packer(dl[i][:-5], button)
				self._widgets.append(button)
		else:
			self.count = 0
		self.scroll = 0
	
	def tick(self) -> None:
		if interact.keys[pygame.K_ESCAPE].deals():
			game.setWindow(self.lastOpen or StartWindow())
		scr = interact.scroll.dealScroll()
		if scr != 0:
			self.scroll += scr
			if self.count > 9:
				self.scroll = utils.frange(self.scroll, 0, self.count - 9)
				for i in range(1, self.count + 1):
					self._widgets[i].y = -0.4 + 0.1 * (i - self.scroll - 1)
				self.onResize()
			else:
				self.scroll = 0
	
	def setLastOpen(self, last: 'Window') -> 'Window':
		self.lastOpen = last
		if isinstance(last, StartWindow):
			self._texture = resourceManager.getOrNew('window/start')
			for w in self._widgets:
				w.color = PresetColors.color
				w.textColor = PresetColors.textColor
		return self


class PauseWindow(Window):
	def __init__(self):
		super().__init__("Pause")
		self._widgets.append(Button(Location.CENTER, 0, -0.3, 0.4, 0.08, RenderableString('\\01Continue'), Description([RenderableString("继续游戏")]), Location.CENTER))
		self._widgets[0].onMouseDown = lambda x, y, b: b[0] == 1 and game.setWindow(None) or True
		self._widgets.append(Button(Location.CENTER, 0, -0.2, 0.4, 0.08, RenderableString('\\01Settings'), Description([RenderableString("设置")]), Location.CENTER))
		self._widgets[1].onMouseDown = lambda x, y, b: b[0] == 1 and game.setWindow(SettingsWindow().setLastOpen(self)) or True
		self._widgets.append(Button(Location.CENTER, 0, -0.1, 0.4, 0.08, RenderableString('\\01Load'), Description([RenderableString("\\#ffee0000放弃保存\\r并读取存档")]), Location.CENTER))
		self._widgets[2].onMouseDown = lambda x, y, b: b[0] == 1 and game.setWindow(LoadWindow().setLastOpen(self)) or True
		self._widgets.append(Button(Location.CENTER, 0, 0, 0.4, 0.08, RenderableString('\\01Task Window'), Description([]), Location.CENTER))
		from window.ingame import TaskWindow
		self._widgets[3].onMouseDown = lambda x, y, b: b[0] == 1 and game.setWindow(TaskWindow().setLastOpen(self)) or True
		self._widgets.append(Button(Location.CENTER, 0, 0.1, 0.4, 0.08, RenderableString('\\01Save'), Description([RenderableString("保存游戏")]), Location.CENTER))
		
		def _4(x, y, b) -> bool:
			if b[0] == 1:
				self._widgets[4].description = Description([RenderableString("\\#ffFCE8AD保存中……")])
				game.getWorld().save()
				self._widgets[4].description = Description([RenderableString("\\#ffFCE8AD保存完成")])
			return True
		
		self._widgets[4].onMouseDown = _4
		
		class Des(Description):
			def __init__(self):
				super().__init__()
				self.exitClick = 0
				self.exitTime = 0
				self.content = [[RenderableString('\\.ffee0000退出游戏'), RenderableString('\\#ffee0000\\.00ff0000不要忘了保存！')], [RenderableString('\\#ffee0000\\.00ff0000再按一次退出游戏'), RenderableString('\\#ffee0000\\.00ff0000不要忘了保存！！！')]]
			
			def generate(self) -> list['RenderableString']:
				return self.content[self.exitClick]
		
		des = Des()
		self._widgets.append(Button(Location.CENTER, 0, 0.2, 0.4, 0.08, RenderableString('\\01Exit'), des, Location.CENTER))
		
		def _5(x, y, b) -> bool:
			if b[0] == 1:
				if des.exitClick == 1:
					game.setWorld(None)
					game.setWindow(StartWindow())
					return True
				des.exitTime = 20
				des.exitClick = 1
			return True
		
		def _5t():
			if des.exitTime == 1:
				des.exitClick = 0
			des.exitTime -= 1
		
		self._widgets[5].color = PresetColors.exitColor
		self._widgets[5].textColor = PresetColors.exitText
		self._widgets[5].onMouseDown = _5
		self._widgets[5].onTick = _5t


class SettingsWindow(Window):
	def __init__(self):
		super().__init__("Settings")
		
		class Des(Description):
			def __init__(self):
				super().__init__()
			
			def generate(self) -> list['RenderableString']:
				return [
					RenderableString('\\#ff66ccee使用4:3屏幕比例 <'),
					RenderableString('\\#ff666666使用16:9屏幕比例')
				] if renderer.is4to3.get() else [
					RenderableString('\\#ff666666使用4:3屏幕比例'),
					RenderableString('\\#ff66ccee使用16:9屏幕比例 <')
				]
		
		self._widgets.append(Button(Location.LEFT_TOP, 0, 0, 0.09, 0.12, RenderableString('\\01Back'), Description([RenderableString("返回")]), Location.CENTER))
		self._widgets[0].onMouseDown = lambda x, y, b: b[0] == 1 and game.setWindow(self.lastOpen or (StartWindow() if game.getWorld() is None else None)) or True
		self._widgets.append(Button(Location.CENTER, 0, -0.3, 0.4, 0.08, RenderableString('\\01Screen \\#ff66ccee4:3\\r\\01 | 16:9' if renderer.is4to3.get() else '\\01Screen 4:3 | \\#ff66ccee16:9'), Des(), Location.CENTER))
		
		def _1(x, y, b):
			if b[0] == 1:
				renderer.is4to3.set(not renderer.is4to3.get())
				self._widgets[1].name = RenderableString('\\01Screen \\#ff66ccee4:3\\r\\01 | 16:9' if renderer.is4to3.getNew() else '\\01Screen 4:3 | \\#ff66ccee16:9')
			return True
		
		self._widgets[1].onMouseDown = _1
		from utils.util import utils
		
		class Des2(Description):
			def __init__(self):
				super().__init__()
				self._color = 0
			
			def generate(self) -> list['RenderableString']:
				return [
					RenderableString('\\#ff66cceeTRACE <' if utils.logLevel == 0 else 'Trace'),
					RenderableString('\\#ff66cceeDEBUG <' if utils.logLevel == 1 else 'Debug'),
					RenderableString('\\#ff66cceeINFO <' if utils.logLevel == 2 else 'Info'),
					RenderableString('\\#ff66cceeWARN <' if utils.logLevel == 3 else 'Warn'),
					RenderableString('\\#ff66cceeERROR <' if utils.logLevel == 4 else 'Error')
				]
		
		def _2(x, y, b):
			if b[0] == 1:
				if utils.logLevel == 4:
					utils.logLevel = 0
				else:
					utils.logLevel += 1
			elif b[2] == 1:
				if utils.logLevel == 0:
					utils.logLevel = 4
				else:
					utils.logLevel -= 1
			else:
				return True
			self._widgets[2].name = RenderableString(['\\01LogLevel \\#ff66cceeT\\r\\01|D|I|W|E', '\\01LogLevel T|\\#ff66cceeD\\r\\01|I|W|E', '\\01LogLevel T|D|\\#ff66cceeI\\r\\01|W|E', '\\01LogLevel T|D|I|\\#ff66cceeW\\r\\01|E', '\\01LogLevel T|D|I|W|\\#ff66cceeE'][utils.logLevel])
			return True
		
		self._widgets.append(Button(Location.CENTER, 0, -0.2, 0.4, 0.08, RenderableString(['\\01LogLevel \\#ff66cceeT\\r\\01|D|I|W|E', '\\01LogLevel T|\\#ff66cceeD\\r\\01|I|W|E', '\\01LogLevel T|D|\\#ff66cceeI\\r\\01|W|E', '\\01LogLevel T|D|I|\\#ff66cceeW\\r\\01|E', '\\01LogLevel T|D|I|W|\\#ff66cceeE'][utils.logLevel]), Des2()))
		self._widgets[2].onMouseDown = _2
		self._widgets.append(Button(Location.CENTER, -0.1, -0.1, 0.2, 0.08, RenderableString('\\01Show FPS' if renderer.displayFPS else '\\01Hide FPS'), Description([RenderableString("是否显示FPS")]), Location.CENTER))
		
		def _3(x, y, b):
			if b[0] == 1:
				renderer.displayFPS = not renderer.displayFPS
				self._widgets[3].name = RenderableString('\\01Show FPS' if renderer.displayFPS else '\\01Hide FPS')
			return True
		
		self._widgets[3].onMouseDown = _3
		self._widgets.append(Button(Location.CENTER, 0.1, -0.1, 0.2, 0.08, RenderableString('\\01Show TPS' if renderer.displayFPS else '\\01Hide TPS'), Description([RenderableString("是否显示TPS")]), Location.CENTER))
		
		def _4(x, y, b):
			if b[0] == 1:
				renderer.displayTPS = not renderer.displayTPS
				self._widgets[4].name = RenderableString('\\01Show TPS' if renderer.displayTPS else '\\01Hide TPS')
			return True
		
		self._widgets[4].onMouseDown = _4
		self._widgets.append(Button(Location.CENTER, -0.1, 0, 0.2, 0.08, RenderableString('\\01 Music: \\#ff66cceeON' if Music_player.turnon_music else '\\01Music: OFF'), Description([
			RenderableString('\\#ff66ccee打开可爱的音乐 <' if Music_player.turnon_music else '打开可爱的音乐'),
			RenderableString('关掉可爱的音乐' if Music_player.turnon_music else '\\#ff66ccee关掉可爱的音乐 <')
		]), Location.CENTER))
		
		def _5(x, y, b):
			if b[0] == 1:
				Music_player.background_volume_press(not Music_player.turnon_music)
				
				self._widgets[5].description.d = [
					RenderableString('\\#ff66ccee打开可爱的音乐 <' if Music_player.turnon_music else '打开可爱的音乐'),
					RenderableString('关掉可爱的音乐' if Music_player.turnon_music else '\\#ff66ccee关掉可爱的音乐 <')
				]
				self._widgets[5].name = RenderableString('\\01 Music: \\#ff66cceeON' if Music_player.turnon_music else '\\01Music: OFF')
			return True
		
		self._widgets[5].onMouseDown = _5
		self._widgets.append(Button(Location.CENTER, 0.1, 0, 0.2, 0.08, RenderableString('\\01 Sound: \\#ff66cceeON' if Music_player.turnon_sound else '\\01Sound: OFF'), Description([
			RenderableString('\\#ff66ccee打开超级古怪的音效 <' if Music_player.turnon_sound else '打开超级古怪的音效'),
			RenderableString('关掉超级古怪的音效' if Music_player.turnon_sound else '\\#ff66ccee关掉超级古怪的音效 <'),
		]), Location.CENTER))
		
		def _6(x, y, b):
			if b[0] == 1:
				Music_player.sound_volume_press(not Music_player.turnon_sound)
				
				self._widgets[6].description.d = [
					RenderableString('\\#ff66ccee打开超级古怪的音效 <' if Music_player.turnon_sound else '打开超级古怪的音效'),
					RenderableString('关掉超级古怪的音效' if Music_player.turnon_sound else '\\#ff66ccee关掉超级古怪的音效 <'),
				]
				self._widgets[6].name = RenderableString('\\01Sound: \\#ff66cceeON' if Music_player.turnon_sound else '\\01Sound: OFF')
			return True
		
		self._widgets[6].onMouseDown = _6
		
		self._widgets.append(Button(Location.CENTER, 0, 0.1, 0.4, 0.08, RenderableString('\\01ScrollLock' if renderer.lockScroll else '\\01ScrollRelease'), Description([RenderableString("地图缩放锁定" if renderer.lockScroll else '滚动滚轮以改变地图缩放')]), Location.CENTER))
		
		def _7(x, y, b):
			if b[0] == 1:
				renderer.lockScroll = not renderer.lockScroll
				self._widgets[7].description = Description([RenderableString('地图缩放锁定' if renderer.lockScroll else '滚动滚轮以改变地图缩放')])
				self._widgets[7].name = RenderableString('\\01ScrollLock' if renderer.lockScroll else '\\01ScrollRelease')
			return True
		
		self._widgets[7].onMouseDown = _7
		
		self._widgets.append(s8 := Slider(Location.CENTER, 0, 0.2, 0.4, 0.08, RenderableString('\\.00000000\\01Music Volume'), Description([RenderableString("音乐音量")]), Location.CENTER))
		s8.value = Music_player.volume_music if Music_player.turnon_music else Music_player.volume_music_before
		s8.onDrag = Music_player.music_volume_drag
		s8.barColor.active = 0x9966ccee
		s8.barColor.hovering = 0xff66ccee
		
		self._widgets.append(s9 := Slider(Location.CENTER, 0, 0.3, 0.4, 0.08, RenderableString('\\.00000000\\01Sound Volume'), Description([RenderableString("音效音量")]), Location.CENTER))
		s9.value = Music_player.volume_sound if Music_player.turnon_sound else Music_player.volume_sound_before
		s9.onDrag = Music_player.sound_volume_drag
		s9.barColor.active = 0x9966ccee
		s9.barColor.hovering = 0xff66ccee
	
	def setLastOpen(self, last: 'Window') -> 'Window':
		self.lastOpen = last
		if isinstance(last, StartWindow):
			self._texture = resourceManager.getOrNew('window/start')
			for w in self._widgets:
				w.color = PresetColors.color
				w.textColor = PresetColors.textColor
		return self


class DeathWindow(Window):
	def __init__(self):
		super().__init__("You Died!")
		self._widgets.append(Button(Location.CENTER, 0, 0.1, 0.4, 0.08, RenderableString('\\01Restart'), Description([RenderableString("复活")]), Location.CENTER))
		from world.world import DynamicWorld
		self._widgets[0].onMouseDown = lambda x, y, b: b[0] == 1 and (game.setWorld(DynamicWorld(game.getWorld(0)._name, game.getWorld(0)._seedNumber)) or game.setWindow(None)) or True
		self._widgets.append(Button(Location.CENTER, 0, 0.2, 0.4, 0.08, RenderableString('\\01Load'), Description([RenderableString("加载存档")]), Location.CENTER))
		self._widgets[1].onMouseDown = lambda x, y, b: b[0] == 1 and game.setWindow(LoadWindow().setLastOpen(self)) or True
		self._widgets.append(Button(Location.CENTER, 0, 0.3, 0.4, 0.08, RenderableString('\\01Exit'), Description([RenderableString('退出游戏')]), Location.CENTER))
		self._widgets[2].color = PresetColors.exitColor
		self._widgets[2].textColor = PresetColors.exitText
		self._widgets[2].onMouseDown = lambda x, y, b: b[0] == 1 and (game.setWorld(None) or game.setWindow(StartWindow())) or True
	
	def render(self, delta: float) -> None:
		w, h = renderer.getSize().getTuple()
		renderer.fill(0xffee0000, int(0.3 * w), int(0.3 * h), int(0.4 * w), int(0.2 * h))
		renderer.renderString(RenderableString("\\01\\#ff000000You are dead"), int(0.5 * w), int(0.4 * h), 0xff000000, Location.CENTER, 0xffee0000)
	
	def tick(self) -> None:
		interact.keys[pygame.K_ESCAPE].deals()


class EggFactoryWindow(Window):
	def __init__(self):
		super().__init__("Babybirth")
		self._texture = resourceManager.getOrNew('window/start')
		
		class Pulling(PullObject):
			def __init__(this, x: float, y: float, name: str, description: Description):
				this.kw = name
				name = RenderableString('\\01' + name)
				super().__init__(Location.CENTER, x, y, name.length() / renderer.getCanvas().get_width() + renderer.getSystemScale() / 2000, 0.08, name, description, textLocation=Location.CENTER, texture=None)
				
				def up(mx, my, buttons):
					if not this.pull:
						return True
					this.pull = False
					if mx > renderer.getCanvas().get_width() * 0.7:
						res = 10 * (my - (renderer.getCanvas().get_height() >> 2)) / renderer.getCanvas().get_height()
						res = utils.frange(res, 0, 4.9)
						if self._selected[0] is this:
							self._selected[0] = None
							self.sortPresent()
						elif self._selected[1] is this:
							self._selected[1] = None
							self.sortPresent()
						elif self._selected[2] is this:
							self._selected[2] = None
							self.sortPresent()
						elif self._selected[3] is this:
							self._selected[3] = None
							self.sortPresent()
						elif self._selected[4] is this:
							self._selected[4] = None
							self.sortPresent()
						if 0 <= res < 5:
							self._selected[int(res)] = this
							self.sortPresent()
							self.sortSelected()
				
				this.onMouseUp = up
		
		self.Pulling = Pulling
		self._selected: list[Pulling | None] = [None, None, None, None, None]
		self._product: Surface | int | None = None
		words = ai.words + ['butterfly-bow', 'runic', 'demonic', 'angelic', 'music', 'C', 'champion', 'second-best', 'hearty', 'grassy', 'rabit', 'flowery']
		words = random.sample(words, 19) + ['pythonic']
		ai.asyncWords()
		xp = -0.4
		yp = -0.4
		for i in words:
			p = Pulling(0, 0, i, Description([RenderableString("1")]))
			xp += p.width
			if xp > 0.2:
				xp = -0.4 + p.width
				yp += 0.1
			p.x = xp - p.width / 2
			p.y = yp
			xp += 0.02
			self._widgets.append(p)
		self._widgets.append(confirmButton := Button(Location.RIGHT_BOTTOM, 0, 0, 0.3, 0.08, RenderableString("\\.00FCE8AD\\00确认"), Description([RenderableString("按下确认就不能修改啦")]), textLocation=Location.CENTER))
		
		def confirm(x, y, buttons):
			if buttons[0] == 1 and confirmButton.active:
				from LLA import ai_decision
				self._product = 1
				ai_decision.asyncEgg([j.kw for j in self._selected if j is not None], game.getWorld().getRandom())
				game.setWindow(EggProductWindow().setWords([j.kw for j in self._selected if j is not None]).setLastOpen(self.lastOpen))
				confirmButton.active = False
			return True
		
		confirmButton.onMouseDown = confirm
	
	def tick(self) -> None:
		if egg_generate.eggGenerated:
			self._product = egg_generate.eggGenerated
			egg_generate.eggGenerated = None
	
	def sortPresent(self):
		xp = -0.4
		yp = -0.4
		for p in self._widgets:
			if isinstance(p, self.Pulling) and p not in self._selected:
				xp += p.width
				if xp > 0.2:
					xp = -0.4 + p.width
					yp += 0.1
				p.x = xp - p.width / 2
				p.y = yp
				xp += 0.02
				p.onResize()
	
	def sortSelected(self):
		if self._selected[0] and not self._selected[0].pull:
			self._selected[0].x = 0.35
			self._selected[0].y = -0.2
			self._selected[0].onResize()
		if self._selected[1] and not self._selected[1].pull:
			self._selected[1].x = 0.35
			self._selected[1].y = -0.1
			self._selected[1].onResize()
		if self._selected[2] and not self._selected[2].pull:
			self._selected[2].x = 0.35
			self._selected[2].y = 0
			self._selected[2].onResize()
		if self._selected[3] and not self._selected[3].pull:
			self._selected[3].x = 0.35
			self._selected[3].y = 0.1
			self._selected[3].onResize()
		if self._selected[4] and not self._selected[4].pull:
			self._selected[4].x = 0.35
			self._selected[4].y = 0.2
			self._selected[4].onResize()
	
	def renderBackground(self, delta: float, at: BlockVector = BlockVector()) -> None:
		self._texture.renderAtInterface(BlockVector())
		size: BlockVector = renderer.getSize()
		sfc = Surface((w := size.x * 0.3, size.y))
		h = size.y * 0.1
		sfc.fill((0xff, 0xff, 0xff), (0, size.y * 0.25, w, h))
		sfc.fill((0xff, 0xff, 0xff), (0, size.y * 0.45, w, h))
		sfc.fill((0xff, 0xff, 0xff), (0, size.y * 0.65, w, h))
		sfc.set_alpha(0x88)
		renderer.getCanvas().blit(sfc, (size.x * 0.7 + 1, 0))
		renderer.renderString(RenderableString('\\01You are laying'), int(size.x * 0.85), size.y >> 3, 0xffeeeeee, Location.BOTTOM)
		renderer.renderString(RenderableString('\\01A(An)'), int(size.x * 0.85), size.y >> 3, 0xffeeeeee, Location.TOP)
		renderer.renderString(RenderableString('\\01Egg'), int(size.x * 0.85), int(size.y * 0.85), 0xffeeeeee, Location.BOTTOM)


class EggProductWindow(Window):
	def __init__(self):
		super().__init__("Egg Product")
		self._texture = resourceManager.getOrNew('window/start')
		self._product = None
		self._renderable = None
		self.keywords = []
		self._widgets.append(Button(Location.BOTTOM, 0, 0, 1, 0.08, RenderableString("\\.00FCE8AD\\00保存"), Description([RenderableString("\\#ffeeee00永远保存我的蛋！")]), textLocation=Location.CENTER))
		
		def save(x, y, buttons):
			if buttons[0] == 1:
				if self._product is not None:
					assert isinstance(self._product, Surface)
					if not os.path.exists("user/archive"):
						os.makedirs("user/archive")
					name = f"user/archive/my_" + "_".join(self.keywords) + "_egg.bmp"
					pygame.image.save(self._product, name)
					if not game.getWorld(0).ending:
						from window.ingame import EndPlotWindow
						game.setWindow(EndPlotWindow())
					else:
						game.setWindow(None)
			return True
		
		self._widgets[-1].onMouseDown = save
	
	def setWords(self, words: list[str]) -> 'EggProductWindow':
		self.keywords = words
		return self
	
	def tick(self) -> None:
		if egg_generate.eggGenerated:
			self._product = egg_generate.eggGenerated
			self._renderable = pygame.transform.scale_by(self._product, renderer.getSystemScale() * 0.1)
			egg_generate.eggGenerated = None
	
	def onResize(self) -> None:
		super().onResize()
		if self._product:
			self._renderable = pygame.transform.scale_by(self._product, renderer.getSystemScale() * 0.1)
	
	def render(self, delta: float) -> None:
		if isinstance(self._renderable, Surface):
			renderer.getCanvas().blit(self._renderable, (renderer.getCanvas().get_width() - self._renderable.get_width() >> 1, renderer.getCanvas().get_height() - self._renderable.get_height() >> 1))
			renderer.renderString(RenderableString(f"\\01\\#ff000000Your " + ", ".join(self.keywords) + " egg!"), renderer.getCanvas().get_width() >> 1, renderer.getCanvas().get_height() >> 4, 0xffeeeeee, Location.CENTER)
		else:
			renderer.renderString(RenderableString("\\#ff000000亲爱的AI正在准备你的鸡蛋"), renderer.getCanvas().get_width() >> 1, renderer.getCanvas().get_height() >> 3, 0xffeeeeee, Location.CENTER)
