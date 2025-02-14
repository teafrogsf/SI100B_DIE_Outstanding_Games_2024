import pygame
from pygame import Surface

from interact.interacts import interact
from music.music import Music_player
from render import font
from render.renderer import Location, renderer
from render.resource import Texture, resourceManager
from utils.game import game
from utils.text import RenderableString, Description
from utils.vector import Vector, BlockVector
from window.input import SeedWindow
from window.widget import Button, PullObject
from window.window import Window, PresetColors
from world.world import DynamicWorld


class StatusWindow(Window):
	def __init__(self):
		super().__init__("Status", None)
		from entity.skill import Skill
		self.backgroundColor = 0x88000000
		self.skillSelecting: tuple[Skill, Button] | None = None
		y: float = -0.4
		
		def _0t():
			if self.skillSelecting is None:
				return True
			player = game.getWorld().getPlayer()
			s = self.skillSelecting
			if s is None:
				self._widgets[0].name = RenderableString('升级')
				self._widgets[0].description.d = [RenderableString("请选择一个技能")]
				self._widgets[0].active = False
			elif s[0].getMaxLevel() <= s[0].getLevel():
				self._widgets[0].name = RenderableString('等级已满')
				self._widgets[0].description.d = [RenderableString("技能已满级")]
				self._widgets[0].active = False
			elif s[0].upgradeCost() > player.growth_value:
				self._widgets[0].name = RenderableString('无法升级')
				self._widgets[0].description.d = [RenderableString(f"成长值不足：{player.growth_value:.2f}/{s[0].upgradeCost():.2f}")]
				self._widgets[0].active = False
			else:
				self._widgets[0].name = RenderableString('升级！')
				self._widgets[0].description.d = [RenderableString("消耗" + str(s[0].upgradeCost()) + "成长值")]
				self._widgets[0].active = True
			return True
		
		def _0c(x, y_, b_):
			if b_[0] == 1:
				if self.skillSelecting == -1:
					return True
				player = game.getWorld().getPlayer()
				s = self.skillSelecting
				if s is None:
					return True
				if not self._widgets[0].active:
					return True
				cost = s[0].upgradeCost()
				if s[0].upgrade():
					player.growth_value -= cost
					s[1].name = s[0].getName()
			return True
		
		self._widgets.append(Button(Location.RIGHT, -0.05, 0.3, 0.2, 0.1, RenderableString('升级'), Description([RenderableString("请选择一个技能")]), textLocation=Location.CENTER))
		self._widgets[0].active = False
		self._widgets[0].tick = _0t
		self._widgets[0].onMouseDown = _0c
		
		def _1(s, bt):
			def wrapper(x, y_, b_):
				if b_[0] == 1:
					self.skillSelecting = s, bt
				return True
			
			return wrapper
		
		for sk in game.getWorld().getPlayer().skills.values():
			b = Button(Location.CENTER, -0.1, y, 0.2, 0.05, sk.getName(), sk.description, Location.CENTER)
			b.onMouseDown = _1(sk, b)
			self._widgets.append(b)
			y += 0.05
		
		y = -0.4
		for sk in game.getWorld().getPlayer().activeSkills:
			b = Button(Location.CENTER, 0.1, y, 0.2, 0.05, sk.getName(), sk.description, Location.CENTER)
			b.onMouseDown = _1(sk, b)
			self._widgets.append(b)
			y += 0.05
	
	def render(self, delta: float) -> None:
		player = game.getWorld().getPlayer()
		if player is None:
			return
		size = renderer.getSize()
		player.getTexture().renderAtInterface()
		renderer.renderString(RenderableString(f"\\01Growth: {player.growth_value:.2f} / 100"), int(size.x * 0.15), int(size.y * 0.5), 0xffeeee55, Location.BOTTOM)
		renderer.renderString(RenderableString(f"\\01Sticks: {player.backpack_stick}\\#ffddbb66 / 100"), int(size.x * 0.15), int(size.y * 0.5), 0xffddbb66, Location.TOP)
		s = self.skillSelecting
		if s is not None:
			sfc = s[0].texture.getSystemScaledSurface()
			renderer.getCanvas().blit(sfc, (renderer.getSize().x * 0.85 - (sfc.get_width() >> 1), sfc.get_height()))
			renderer.getCanvas().blit(sfc, (renderer.getSize().x * 0.85 - (sfc.get_width() >> 1), sfc.get_height()))
			
			renderer.renderString(s[0].getName(), int(size.x * 0.85), y := int(size.y * 0.4), 0xffeeee55, Location.TOP, 0, 1)
			y += font.realFontHeight
			for d in s[0].description.d:
				renderer.renderString(d, int(size.x * 0.85), y, 0xffeeee55, Location.TOP, 0, -1)
				y += font.realHalfHeight
	
	def tick(self) -> None:
		if interact.keys[pygame.K_ESCAPE].deals() or interact.keys[pygame.K_e].deals():
			game.setWindow(self.lastOpen)


class TaskWindow(Window):
	def __init__(self):
		super().__init__("Task")
		self._texture = resourceManager.getOrNew('window/task')
		self._texture.adaptsMap(False)
		self._texture.systemScaleOffset = 0.02
		self._texture.adaptsSystem(True)
		self._texture.renderAtInterface(BlockVector(30, 30))
		self.progress = game.getWorld().getPlayer().progress
		self.looking = 1
		
		X = ["暂未解锁"] * 5
		for i in range(self.progress):
			X[i] = "解锁"
		
		self._widgets.append(Button(Location.CENTER, -0.2, -0.12, 0.12, 0.08, RenderableString("\\.00FCE8AD\\01TASK 1"), Description([RenderableString(X[0])]), textLocation=Location.CENTER))
		self._widgets.append(Button(Location.CENTER, -0.2, -0.03, 0.12, 0.08, RenderableString("\\.00FCE8AD\\01TASK 2"), Description([RenderableString(X[1])]), textLocation=Location.CENTER))
		self._widgets.append(Button(Location.CENTER, -0.2, 0.06, 0.12, 0.08, RenderableString("\\.00FCE8AD\\01TASK 3"), Description([RenderableString(X[2])]), textLocation=Location.CENTER))
		self._widgets.append(Button(Location.CENTER, -0.2, 0.15, 0.12, 0.08, RenderableString("\\.00FCE8AD\\01TASK 4"), Description([RenderableString(X[3])]), textLocation=Location.CENTER))
		self._widgets.append(Button(Location.CENTER, -0.2, 0.24, 0.12, 0.08, RenderableString("\\.00FCE8AD\\01TASK 5"), Description([RenderableString(X[4])]), textLocation=Location.CENTER))
		self._widgets.append(Button(Location.CENTER, -0.2, -0.21, 0.12, 0.08, RenderableString("\\.00FCE8AD\\01Tutorial"), Description([RenderableString("技能的教程，来学不亏")]), textLocation=Location.CENTER))
		
		self._widgets[5].onMouseDown = lambda x, y, b: b[0] == 1 and game.setWindow(GuidanceWindow().setLastOpen(self)) or True
		
		for i in range(self.progress, 5):
			self._widgets[i].active = False
		
		self._backgroundLocation = Location.CENTER
		color = PresetColors.color.clone()
		color.hovering = 0
		textColor = PresetColors.color.clone()
		textColor.hovering = 0xffcfc490
		textColor.active = 0xff000000
		textColor.inactive = 0xff888888
		self._widgets[0].color = color
		self._widgets[1].color = color
		self._widgets[2].color = color
		self._widgets[3].color = color
		self._widgets[4].color = color
		self._widgets[5].color = color
		self._widgets[0].textColor = textColor
		self._widgets[1].textColor = textColor
		self._widgets[2].textColor = textColor
		self._widgets[3].textColor = textColor
		self._widgets[4].textColor = textColor
		self._widgets[5].textColor = textColor
		
		def _1(x, y, b) -> bool:
			self.looking = 1
			return True
		
		def _2(x, y, b) -> bool:
			self.looking = 2
			return True
		
		def _3(x, y, b) -> bool:
			self.looking = 3
			return True
		
		def _4(x, y, b) -> bool:
			self.looking = 4
			return True
		
		def _5(x, y, b) -> bool:
			self.looking = 5
			return True
		
		if self.progress == 5:
			self._widgets[4].onMouseDown = _5
		if self.progress >= 4:
			self._widgets[3].onMouseDown = _4
		if self.progress >= 3:
			self._widgets[2].onMouseDown = _3
		if self.progress >= 2:
			self._widgets[1].onMouseDown = _2
		if self.progress >= 1:
			self._widgets[0].onMouseDown = _1
	
	def onResize(self) -> None:
		if renderer.is4to3.get():
			self._widgets[0].x = -0.33
			self._widgets[1].x = -0.33
			self._widgets[2].x = -0.33
			self._widgets[3].x = -0.33
			self._widgets[4].x = -0.33
			self._widgets[5].x = -0.33
		else:
			self._widgets[0].x = -0.25
			self._widgets[1].x = -0.25
			self._widgets[2].x = -0.25
			self._widgets[3].x = -0.25
			self._widgets[4].x = -0.25
			self._widgets[5].x = -0.25
		super().onResize()
	
	def render(self, delta: float) -> None:
		super().render(delta)
		size: BlockVector = renderer.getSize()
		if self.looking == 1:
			renderer.renderString(RenderableString('\\.ffEFE4B0\\00任务1：' if self.progress <= 1 else '\\.ffEFE4B0\\00已完成任务1：'), int((0.58 if renderer.is4to3.get() else 0.56) * size.x), (size.y >> 1) - font.realFontHeight, 0xff000000, Location.BOTTOM)
			renderer.renderString(RenderableString('\\.ffEFE4B0\\00胸有大志，吃100颗米粒！'), int((0.58 if renderer.is4to3.get() else 0.56) * size.x), size.y >> 1, 0xff000000, Location.TOP)
			renderer.renderString(RenderableString('\\.ffEFE4B0\\10\\#ffee0000会有技能随机掉落'), int((0.58 if renderer.is4to3.get() else 0.56) * size.x), (size.y >> 1) + font.realFontHeight, 0xff000000, Location.TOP)
		
		if self.looking == 2:
			renderer.renderString(RenderableString('\\.ffEFE4B0\\00任务2：' if self.progress <= 2 else '\\.ffEFE4B0\\00已完成任务2：'), int((0.58 if renderer.is4to3.get() else 0.56) * size.x), (size.y >> 1) - font.realFontHeight, 0xff000000, Location.BOTTOM)
			renderer.renderString(RenderableString('\\.ffEFE4B0\\00年少有为，织鸡窝！'), int((0.58 if renderer.is4to3.get() else 0.56) * size.x), size.y >> 1, 0xff000000, Location.TOP)
			renderer.renderString(RenderableString('\\.ffEFE4B0\\10\\#ffee0000100树枝+H键可以给你带来一个大大的鸡窝'), int((0.58 if renderer.is4to3.get() else 0.56) * size.x), (size.y >> 1) + font.realFontHeight, 0xff000000, Location.TOP)
		
		if self.looking == 3:
			renderer.renderString(RenderableString('\\.ffEFE4B0\\00任务3：' if self.progress <= 3 else '\\.ffEFE4B0\\00已完成任务3：'), int((0.58 if renderer.is4to3.get() else 0.56) * size.x), (size.y >> 1) - font.realFontHeight, 0xff000000, Location.BOTTOM)
			renderer.renderString(RenderableString('\\.ffEFE4B0\\00老巫婆鸡，指点迷津！'), int((0.58 if renderer.is4to3.get() else 0.56) * size.x), size.y >> 1, 0xff000000, Location.TOP)
			renderer.renderString(RenderableString('\\.ffEFE4B0\\10\\#ffee0000你也许有看到一个炫酷的传送门，3秒定律'), int((0.58 if renderer.is4to3.get() else 0.56) * size.x), (size.y >> 1) + font.realFontHeight, 0xff000000, Location.TOP)
		
		if self.looking == 4:
			renderer.renderString(RenderableString('\\.ffEFE4B0\\00任务4：' if self.progress <= 4 else '\\.ffEFE4B0\\00已完成任务4：'), int((0.58 if renderer.is4to3.get() else 0.56) * size.x), (size.y >> 1) - font.realFontHeight, 0xff000000, Location.BOTTOM)
			renderer.renderString(RenderableString('\\.ffEFE4B0\\00你需要获得公鸡的受精！'), int((0.58 if renderer.is4to3.get() else 0.56) * size.x), size.y >> 1, 0xff000000, Location.BOTTOM)
			renderer.renderString(RenderableString('\\.ffEFE4B0\\10\\#ffee0000杀死一只母鸡可以让公鸡恢复单身狗'), int((0.58 if renderer.is4to3.get() else 0.56) * size.x), (size.y >> 1) + font.realFontHeight, 0xff000000, Location.TOP)
		
		if self.looking == 5:
			renderer.renderString(RenderableString('\\.ffEFE4B0\\00任务5：' if self.progress <= 5 else '\\.ffEFE4B0\\00已完成任务5：'), int((0.58 if renderer.is4to3.get() else 0.56) * size.x), (size.y >> 1) - font.realFontHeight, 0xff000000, Location.BOTTOM)
			renderer.renderString(RenderableString('\\.ffEFE4B0\\00快带公鸡回家下蛋'), int((0.58 if renderer.is4to3.get() else 0.56) * size.x), size.y >> 1, 0xff000000, Location.TOP)
			renderer.renderString(RenderableString('\\.ffEFE4B0\\10\\#ffee0000你可以给鸡蛋选择不同的描述'), int((0.58 if renderer.is4to3.get() else 0.56) * size.x), (size.y >> 1) + font.realFontHeight, 0xff000000, Location.TOP)
		
		renderer.renderString(RenderableString('\\.ffEFE4B0\\10左侧点击选择任务，Tab键返回'), int((0.58 if renderer.is4to3.get() else 0.56) * size.x), int(size.y * 0.8), 0xff000000, Location.BOTTOM)
	
	def passRender(self, delta: float, at: Vector | None = None) -> None:
		s = Surface(renderer.getCanvas().get_size())
		s.fill(self.backgroundColor & 0xffffff)
		s.set_alpha(self.backgroundColor >> 24)
		renderer.getCanvas().blit(s, (0, 0))
		super().passRender(delta, at)
	
	def tick(self) -> None:
		super().tick()
		if interact.keys[pygame.K_TAB].deals():
			game.setWindow(self.lastOpen)


class PlotWindow(Window):
	def __init__(self):
		super().__init__("Plot")
		self._texture = resourceManager.getOrNew('window/plot_1')
		self._texture.systemScaleOffset = 0.064
		self._texture.adaptsMap(False)
		self._texture.adaptsSystem(True)
		self.Sentence = 0
		
		def _0(x, y, b) -> bool:
			if self.Sentence < 11:
				self.Sentence += 1
			else:
				game.setWindow(SeedWindow().setLastOpen(self))
			# game.setWindow(None)
			# game.setWorld(DynamicWorld('DynamicWorld'))
			return True
		
		def _1(x, y, b) -> bool:
			if self.Sentence < 11:
				self.Sentence = 11
			else:
				game.setWindow(SeedWindow().setLastOpen(self))
			# game.setWindow(None)
			# game.setWorld(DynamicWorld('DynamicWorld'))
			return True
		
		def _2(x, y, b) -> bool:
			if self.Sentence > 0:
				self.Sentence -= 1
			else:
				game.setWindow(self.lastOpen)
			return True
		
		self._widgets.append(Button(Location.BOTTOM, 0.22, 0, 0.12, 0.08, RenderableString("\\.00FFFFFF\\01NEXT"), Description([RenderableString("继续")]), textLocation=Location.CENTER))
		self._widgets[0].onMouseDown = _0
		self._widgets.append(Button(Location.BOTTOM, 0.38, 0, 0.12, 0.08, RenderableString("\\.00FFFFFF\\01SKIP"), Description([RenderableString("跳过剧情")]), textLocation=Location.CENTER))
		self._widgets[1].onMouseDown = _1
		self._widgets.append(Button(Location.BOTTOM, 0.06, 0, 0.12, 0.08, RenderableString("\\.00FFFF\\01BACK"), Description([RenderableString("上一页")]), textLocation=Location.CENTER))
		self._widgets[2].onMouseDown = _2
		
		self._widgets[0].color = PresetColors.plotColor
		self._widgets[1].color = PresetColors.plotColor
		self._widgets[2].color = PresetColors.plotColor
		
		self._widgets[0].textColor = PresetColors.plotText
		self._widgets[1].textColor = PresetColors.plotText
		self._widgets[2].textColor = PresetColors.plotText
	
	def render(self, delta: float) -> None:
		super().render(delta)
		size: BlockVector = renderer.getSize()
		if self.Sentence == 0:
			# 之前是0.62和0.28
			renderer.renderString(RenderableString('\\.0040304D\\00嘿！小家伙，你终于醒啦！'), int(size.x * 0.5), int(size.y * 0.4), 0xffffffff, Location.CENTER)
			renderer.renderString(RenderableString('\\.0040304D\\00别怕，这里很安全。'), int(size.x * 0.5), int(size.y * 0.4 + font.realFontHeight), 0xffffffff, Location.CENTER)
		if self.Sentence == 1:
			renderer.renderString(RenderableString('\\.0040304D\\00你是一只体弱多病的小鸡，'), int(size.x * 0.5), int(size.y * 0.4), 0xffffffff, Location.CENTER)
			renderer.renderString(RenderableString('\\.0040304D\\00没办法生蛋赚钱……'), int(size.x * 0.5), int(size.y * 0.4 + font.realFontHeight), 0xffffffff, Location.CENTER)
		if self.Sentence == 2:
			renderer.renderString(RenderableString('\\.0040304D\\00正因如此，你的主人不仅虐待你，'), int(size.x * 0.5), int(size.y * 0.4), 0xffffffff, Location.CENTER)
			renderer.renderString(RenderableString('\\.0040304D\\00还把你无情地抛弃在了荒草丛中。'), int(size.x * 0.5), int(size.y * 0.4 + font.realFontHeight), 0xffffffff, Location.CENTER)
		if self.Sentence == 3:
			renderer.renderString(RenderableString('\\.0040304D\\00当我发现你的时候，你浑身是伤，'), int(size.x * 0.5), int(size.y * 0.4), 0xffffffff, Location.CENTER)
			renderer.renderString(RenderableString('\\.0040304D\\00虚弱得连站都站不稳……'), int(size.x * 0.5), int(size.y * 0.4 + font.realFontHeight), 0xffffffff, Location.CENTER)
		if self.Sentence == 4:
			renderer.renderString(RenderableString('\\.0040304D\\00咱们现在来到了一个新的村庄，'), int(size.x * 0.5), int(size.y * 0.4), 0xffffffff, Location.CENTER)
			renderer.renderString(RenderableString('\\.0040304D\\00这就是你以后生活的地方啦！'), int(size.x * 0.5), int(size.y * 0.4 + font.realFontHeight), 0xffffffff, Location.CENTER)
		if self.Sentence == 5:
			renderer.renderString(RenderableString('\\.0040304D\\00接下来的日子可能不太轻松，'), int(size.x * 0.5), int(size.y * 0.4), 0xffffffff, Location.CENTER)
			renderer.renderString(RenderableString('\\.0040304D\\00你要搜集草地上的米粒来填饱肚子……'), int(size.x * 0.5), int(size.y * 0.4 + font.realFontHeight), 0xffffffff, Location.CENTER)
		if self.Sentence == 6:
			renderer.renderString(RenderableString('\\.0040304D\\00并尽可能多地收集树枝，'), int(size.x * 0.5), int(size.y * 0.4), 0xffffffff, Location.CENTER)
			renderer.renderString(RenderableString('\\.0040304D\\00为自己建造一个鸡窝……'), int(size.x * 0.5), int(size.y * 0.4 + font.realFontHeight), 0xffffffff, Location.CENTER)
		if self.Sentence == 7:
			renderer.renderString(RenderableString('\\.0040304D\\00在这个村庄里有很多邪恶的狐狸，'), int(size.x * 0.5), int(size.y * 0.4), 0xffffffff, Location.CENTER)
			renderer.renderString(RenderableString('\\.0040304D\\00你一定要注意防范他们的攻击！'), int(size.x * 0.5), int(size.y * 0.4 + font.realFontHeight), 0xffffffff, Location.CENTER)
		if self.Sentence == 8:
			renderer.renderString(RenderableString('\\.0040304D\\00你的最终目标是逆天改命，'), int(size.x * 0.5), int(size.y * 0.4), 0xffffffff, Location.CENTER)
			renderer.renderString(RenderableString('\\.0040304D\\00生一个蛋，并孵出一只小鸡！'), int(size.x * 0.5), int(size.y * 0.4 + font.realFontHeight), 0xffffffff, Location.CENTER)
		if self.Sentence == 8:
			renderer.renderString(RenderableString('\\.0040304D\\00你的最终目标是逆天改命，'), int(size.x * 0.5), int(size.y * 0.4), 0xffffffff, Location.CENTER)
			renderer.renderString(RenderableString('\\.0040304D\\00生一个蛋，并孵出一只小鸡！'), int(size.x * 0.5), int(size.y * 0.4 + font.realFontHeight), 0xffffffff, Location.CENTER)
		if self.Sentence == 9:
			renderer.renderString(RenderableString('\\.0040304D\\00游戏中你可能会用到以下快捷键：'), int(size.x * 0.5), int(size.y * 0.2 - font.realFontHeight * 1.3), 0xffffffff, Location.CENTER)
			renderer.renderString(RenderableString('\\.0040304D\\00人物移动 WASD 同时按Crtl可加速'), int(size.x * 0.5), int(size.y * 0.23 + font.realFontHeight * 0), 0xffffffff, Location.CENTER)
			renderer.renderString(RenderableString('\\.0040304D\\00状态面板 E'), int(size.x * 0.5), int(size.y * 0.23 + font.realFontHeight * 1), 0xffffffff, Location.CENTER)
			renderer.renderString(RenderableString('\\.0040304D\\00\\#ffee0000任务面板、游戏进程与技能教程\\#ffeeeeee Tab'), int(size.x * 0.5), int(size.y * 0.23 + font.realFontHeight * 2), 0xffffffff, Location.CENTER)
			renderer.renderString(RenderableString('\\.0040304D\\00暂停并打开暂停菜单 Esc'), int(size.x * 0.5), int(size.y * 0.23 + font.realFontHeight * 3), 0xffffffff, Location.CENTER)
			renderer.renderString(RenderableString('\\.0040304D\\00锁定/解锁视角 Space'), int(size.x * 0.5), int(size.y * 0.23 + font.realFontHeight * 4), 0xffffffff, Location.CENTER)
			renderer.renderString(RenderableString('\\.0040304D\\00移动视角 中键按住拖动'), int(size.x * 0.5), int(size.y * 0.23 + font.realFontHeight * 5), 0xffffffff, Location.CENTER)
			renderer.renderString(RenderableString('\\.0040304D\\00缩放地图 滚轮'), int(size.x * 0.5), int(size.y * 0.23 + font.realFontHeight * 6), 0xffffffff, Location.CENTER)
			renderer.renderString(RenderableString('\\.0040304D\\00米粒树枝作弊按键 Q'), int(size.x * 0.5), int(size.y * 0.23 + font.realFontHeight * 7), 0xffffffff, Location.CENTER)
		if self.Sentence == 10:
			renderer.renderString(RenderableString('\\.0040304D\\00忘记了也没关系，可以键入Enter'), int(size.x * 0.5), int(size.y * 0.4), 0xffffffff, Location.CENTER)
			renderer.renderString(RenderableString('\\.0040304D\\00问问知道关于游戏一切的ai系统'), int(size.x * 0.5), int(size.y * 0.4 + font.realFontHeight), 0xffffffff, Location.CENTER)
			renderer.renderString(RenderableString('\\.0040304D\\00或者\\#ff4488ee把鼠标移上去\\#ffeeeeee看看提示'), int(size.x * 0.5), int(size.y * 0.4 + (font.realFontHeight << 1)), 0xffffffff, Location.CENTER)
		if self.Sentence == 11:
			renderer.renderString(RenderableString('\\.0040304D\\00那么，话不多说'), int(size.x * 0.5), int(size.y * 0.4), 0xffffffff, Location.CENTER)
			renderer.renderString(RenderableString('\\.0040304D\\00游戏开始！'), int(size.x * 0.5), int(size.y * 0.4 + font.realFontHeight), 0xffffffff, Location.CENTER)
		
		renderer.renderString(RenderableString(f'\\.0040304D\\01Page {self.Sentence + 1} / 12'), int(size.x * 0.9), int(size.y * 0.1), 0xffffffff, Location.CENTER)
	
	def tick(self) -> None:
		if interact.keys[pygame.K_ESCAPE].deals():
			self.Sentence += 1
			if self.Sentence > 11:
				self.Sentence = 11
				game.setWindow(SeedWindow().setLastOpen(self))


# game.setWindow(None)
# game.setWorld(DynamicWorld('DynamicWorld'))


class NurturingWindow(Window):
	def __init__(self):
		super().__init__("Nurturing......")
		Music_player.background_weaken_volume()
		Music_player.sound_play(6)
		self.nurturing_image = []
		for i in range(1, 7):
			x = resourceManager.getOrNew(f'window/nurturing/nurturing{i}')
			self.nurturing_image.append(x)
		self.timer: int = 120
		
		def _1(x, y, b) -> bool:
			if b[0] == 1:
				Music_player.sound_stop(6)
				Music_player.background_restore_volume()
				game.setWindow(self.lastOpen)
			return True
		
		self._widgets.append(Button(Location.BOTTOM, 0.2, 0, 0.12, 0.08, RenderableString('\\01SKIP'), Description([RenderableString("跳过动画")]), Location.CENTER))
		self._widgets[0].onMouseDown = _1
		self._widgets[0].color = PresetColors.plotColor
		self._widgets[0].textColor = PresetColors.plotText
	
	def render(self, delta: float) -> None:
		size = renderer.getSize()
		renderer.renderString(RenderableString("\\.ff4499ee\\00\\#ffffffff小鸡正在接受教育…………"), int(0.5 * size.x), int(0.6 * size.y), 0xffffffffff, Location.CENTER)
	
	def tick(self) -> None:
		super().tick()
		self._texture = self.nurturing_image[5 - (int(self.timer >> 2) % 6)]
		self.timer -= 1
		if self.timer == 0:
			Music_player.sound_stop(6)
			Music_player.background_weaken_volume()
			game.setWindow(None)  # 这里回去还有问题


class BuildingWindow(Window):
	def __init__(self):
		super().__init__("Building......")
		Music_player.background_weaken_volume()
		Music_player.sound_play(5)
		self.building_image = []
		for i in range(0, 16):
			x = resourceManager.getOrNew(f'window/building2/building{i}')
			self.building_image.append(x)
		self.timer: int = 120
		
		def _1(x, y, b) -> bool:
			if b[0] == 1:
				Music_player.sound_stop(5)
				Music_player.background_restore_volume()
				game.setWindow(self.lastOpen)
			return True
		
		self._widgets.append(Button(Location.BOTTOM, 0.2, 0, 0.12, 0.08, RenderableString('\\01SKIP'), Description([RenderableString("跳过动画")]), Location.CENTER))
		self._widgets[0].onMouseDown = _1
		self._widgets[0].color = PresetColors.plotColor
		self._widgets[0].textColor = PresetColors.plotText
	
	def render(self, delta: float) -> None:
		w, h = renderer.getSize().getTuple()
		renderer.renderString(RenderableString("\\00\\00小鸡正在织鸡窝…………"), int(0.5 * w), int(0.7 * h), 0xffffffff, Location.CENTER)
	
	def passRender(self, delta: float, at: Vector | None = None) -> None:
		s = Surface(renderer.getCanvas().get_size())
		s.fill(self.backgroundColor & 0xffffff)
		s.set_alpha(self.backgroundColor >> 24)
		renderer.getCanvas().blit(s, (0, 0))
		super().passRender(delta, at)
	
	def tick(self) -> None:
		super().tick()
		self._texture = self.building_image[15 - (int(self.timer >> 2) % 16)]
		self._backgroundLocation = Location.CENTER
		self.timer -= 1
		if self.timer == 0:
			Music_player.sound_stop(5)
			Music_player.background_weaken_volume()
			game.setWindow(None)


class QuestionWindow(Window):
	def __init__(self, num):
		super().__init__("Question")
		self.num = num
		
		# 题库
		self.Question = ["Which module does not belong to Python?",
		                 "Which one is not the author of the game?",
		                 "In this game, what can't the chick do?",
		                 "What is the answer of this question?"]
		self.Anwser = [["kivy", "pygame", "os", "robot"],
		               ["teasfrog", "EmsiaetKadosh", "NicolePotion", "IcyOxygenXY"],
		               ["Eat rice", "Pick up sticks", "Dig holes", "Fight with hens"],
		               ["C", "B", "A", "C"]]
		self.clue = ["字", "姐姐", "茄子", "12"]
		self.clue_position = [3, 0, 2, 1]
		self.printclue = "?"
		self.choice = 5
		self.flag = False
		self.tip = [False, 0]
		
		def _0(x, y, b) -> bool:
			self.tip[0] = True
			
			return True
		
		def _1(x, y, b) -> bool:
			self.choice = 0
			self.flag = True
			print(self.flag, self.choice)
			_w()
			return True
		
		def _2(x, y, b) -> bool:
			self.choice = 1
			self.flag = True
			print(self.flag, self.choice)
			_w()
			return True
		
		def _3(x, y, b) -> bool:
			self.choice = 2
			self.flag = True
			print(self.flag, self.choice)
			_w()
			return True
		
		def _4(x, y, b) -> bool:
			self.choice = 3
			self.flag = True
			print(self.flag, self.choice)
			_w()
			return True
		
		print()
		
		def _w():
			if self.flag == True:
				print("1")
				if self.choice == self.clue_position[self.num]:
					print("正确答案")
					self.tip[1] = 2
					self.printclue = self.clue[self.num]
					PresetColors.plotColor.active = 0xff1BA803
					self._widgets[self.choice].color = PresetColors.plotColor
					self._widgets[self.choice].textColor = PresetColors.plotText
				
				else:
					print("错误答案")
					self.tip[1] = 1
					self.printclue = "你失去本题线索"
					PresetColors.plotColor.active = 0xffD40004
					self._widgets[self.choice].color = PresetColors.plotColor
					self._widgets[self.choice].textColor = PresetColors.plotText
				
				self._widgets[0].onMouseDown = _0
				self._widgets[1].onMouseDown = _0
				self._widgets[2].onMouseDown = _0
				self._widgets[3].onMouseDown = _0
		
		def _5(x, y, b) -> bool:
			if b[0] == 1:
				game.setWindow(self.lastOpen)
				PresetColors.plotColor.active = 0xff545454
			return True
		
		self._widgets.append(Button(Location.CENTER, 0.15, -0.1, 0.30, 0.08, RenderableString(f"\\.00FFFFFF\\01{self.Anwser[self.num][0]}"), Description([RenderableString("A")]), textLocation=Location.CENTER))
		self._widgets.append(Button(Location.CENTER, 0.15, 0, 0.30, 0.08, RenderableString(f"\\.00FFFFFF\\01{self.Anwser[self.num][1]}"), Description([RenderableString("B")]), textLocation=Location.CENTER))
		self._widgets.append(Button(Location.CENTER, 0.15, 0.1, 0.30, 0.08, RenderableString(f"\\.00FFFF\\01{self.Anwser[self.num][2]}"), Description([RenderableString("C")]), textLocation=Location.CENTER))
		self._widgets.append(Button(Location.CENTER, 0.15, 0.2, 0.30, 0.08, RenderableString(f"\\.00FFFF\\01{self.Anwser[self.num][3]}"), Description([RenderableString("D")]), textLocation=Location.CENTER))
		self._widgets[0].onMouseDown = _1
		self._widgets[1].onMouseDown = _2
		self._widgets[2].onMouseDown = _3
		self._widgets[3].onMouseDown = _4
		
		self._widgets.append(Button(Location.LEFT_TOP, 0, 0, 0.09, 0.12, RenderableString('\\01Back'), Description([RenderableString("返回")]), Location.CENTER))
		self._widgets[4].onMouseDown = _5
	
	def render(self, delta: float) -> None:
		super().render(delta)
		size: BlockVector = renderer.getSize()
		renderer.renderString(RenderableString(f'\\.0040304D\\00{self.Question[self.num]}'), int(size.x * 0.65), int(size.y * 0.2), 0xffffffff, Location.CENTER)
		# 线索
		renderer.renderString(RenderableString('\\.0040304D\\00线索：'), int(size.x * 0.1), int(size.y * 0.2), 0xffffffff, Location.CENTER)
		renderer.renderString(RenderableString(f'\\.0040304D\\00{self.printclue}'), int(size.x * 0.2), int(size.y * 0.4), 0xffffffff, Location.CENTER)
		if self.tip[1] == 1 and self.tip[0] == True:
			renderer.renderString(RenderableString(f'\\.0040304D\\10正确答案：{self.Anwser[self.num][self.clue_position[self.num]]}'), int(size.x * 0.2), int(size.y * 0.55), 0xffD40004, Location.CENTER)
			renderer.renderString(RenderableString('\\.0040304D\\10只有一次答题机会呢'), int(size.x * 0.2), int(size.y * 0.6), 0xffD40004, Location.CENTER)
		
		if self.tip[1] == 2 and self.tip[0] == True:
			renderer.renderString(RenderableString('\\.0040304D\\10你已经答对了'), int(size.x * 0.2), int(size.y * 0.55), 0xff1BA803, Location.CENTER)
			renderer.renderString(RenderableString('\\.0040304D\\10还有2个线索等着你'), int(size.x * 0.2), int(size.y * 0.6), 0xff1BA803, Location.CENTER)
	
	def tick(self) -> None:
		pass


class GuidanceWindow(Window):
	def __init__(self):
		super().__init__("Guidance")
		self.page = 0
		
		self._texture = [
			[resourceManager.getOrNew('window/Guidance/page0/show')],
			[
				resourceManager.getOrNew('window/Guidance/page0/show'),
				resourceManager.getOrNew('window/Guidance/page0/rice')
			],
			[resourceManager.getOrNew('window/Guidance/page0.8/show')],
			[
				resourceManager.getOrNew('window/Guidance/page1/skill1'),
				resourceManager.getOrNew('window/Guidance/page1/skill2'),
				resourceManager.getOrNew('window/Guidance/page1/skill3'),
				resourceManager.getOrNew('window/Guidance/page1/skill4'),
				resourceManager.getOrNew('window/Guidance/page1/skill5'),
				resourceManager.getOrNew('window/Guidance/page1/skill6')
			],
			[
				resourceManager.getOrNew('window/Guidance/page1.5/show'),
				resourceManager.getOrNew('window/Guidance/page1.5/skill')
			],
			[
				resourceManager.getOrNew('window/Guidance/page2/show'),
				resourceManager.getOrNew('window/Guidance/page2/skill')
			],
			[
				resourceManager.getOrNew('window/Guidance/page3/show'),
				resourceManager.getOrNew('window/Guidance/page3/skill')
			],
			[
				resourceManager.getOrNew('window/Guidance/page4/show'),
				resourceManager.getOrNew('window/Guidance/page4/skill')
			],
			[
				resourceManager.getOrNew('window/Guidance/page5/show'),
				resourceManager.getOrNew('window/Guidance/page5/skill1'),
				resourceManager.getOrNew('window/Guidance/page5/skill2')
			],
			[
				resourceManager.getOrNew('window/Guidance/page6/1'),
				resourceManager.getOrNew('window/Guidance/page6/2'),
				resourceManager.getOrNew('window/Guidance/page6/3'),
				resourceManager.getOrNew('window/Guidance/page6/4'),
				resourceManager.getOrNew('window/Guidance/page6/5')
			]
		]
		
		self._texture_position = [
			[[0, 0.22]],
			[[0, 0.22], [0.77, 0.6]],
			[[0.12, 0.1]],
			[[0.54, 0.1], [0.08, 0.5], [0.31, 0.5], [0.54, 0.5], [0.77, 0.5], [0.31, 0.1]],
			[[0.55, 0.3], [0.2, 0.1]],
			[[0.55, 0.3], [0.2, 0.1]],
			[[0.55, 0.3], [0.2, 0.1]],
			[[0.55, 0.3], [0.2, 0.1]],
			[[0.55, 0.3], [0.23, 0.08], [0.23, 0.55]],
			[[0.05, 0.3], [0.23, 0.3], [0.41, 0.3], [0.59, 0.3], [0.77, 0.3]]
		]
		
		self._text = [
			["按E调出任务面板", "可以升级技能", "面板有技能信息", "这里将教学使用方法"],
			["如果你发现无法升级", "那就是成长值不足", "先去吃点米粒吧"],
			["1    2    3    4    5    6", "键入1-6可进入准备状态，再次点击释放", "技能获得顺序随机", "数字编号由玩家获得的技能顺序决定", "鼠标右键退出准备模式"],
			["主动技能：", "猛啄", "头槌", "肾上腺素", "闪现", "回复", "迅捷"],
			["主动技能——回复", "原地回血", "回血与激情！", "冷却时间：40s", "准备时图像："],
			["主动技能——闪现", "可以帮助你跨越一些墙", "对准后使用即可", "冷却时间：40s", "准备时图像："],
			["主动技能——猛啄", "用于近战攻击", "黄色箭头为攻击范围", "可连续使用", "准备时图像："],
			["主动技能——头槌", "远距离攻击+传送", "黄圈为攻击范围，", "冷却时间：40s", "准备时图像："],
			["主动技能——肾上腺素", "短暂的免死金牌", "主动技能——疾跑", "顾名思义，跑得更快", "使用后短暂加速", "准备时图像："],
			["至于被动技能：", "爱米", "坚毅", "揠苗", "屹立不倒", "迅捷", "去面板升级就好啦", "（）不升级容易死"]
		]
		
		self._text_position = [
			[[0.75, 0.3], [0.75, 0.4], [0.75, 0.5], [0.75, 0.6]],
			[[0.75, 0.3], [0.75, 0.4], [0.75, 0.5]],
			[[0.3, 0.45], [0.5, 0.55], [0.5, 0.65], [0.5, 0.75], [0.5, 0.85]],
			[[0.2, 0.2], [0.125, 0.85], [0.375, 0.85], [0.625, 0.85], [0.875, 0.85], [0.375, 0.45], [0.625, 0.45]],
			[[0.27, 0.5], [0.27, 0.6], [0.27, 0.7], [0.27, 0.8], [0.65, 0.2]],
			[[0.27, 0.5], [0.27, 0.6], [0.27, 0.7], [0.27, 0.8], [0.65, 0.2]],
			[[0.27, 0.5], [0.27, 0.6], [0.27, 0.7], [0.27, 0.8], [0.65, 0.2]],
			[[0.27, 0.5], [0.27, 0.6], [0.27, 0.7], [0.27, 0.8], [0.65, 0.2]],
			[[0.27, 0.35], [0.27, 0.45], [0.27, 0.82], [0.27, 0.92], [0.65, 0.85], [0.65, 0.2]],
			[[0.2, 0.2], [0.1, 0.65], [0.3, 0.65], [0.5, 0.65], [0.7, 0.65], [0.9, 0.65], [0.5, 0.75], [0.5, 0.85]]
		]
		"""
		你未来会碰到敌人，怎么办？
		大开杀戒
		吃了米，生命值会升高 完成任务
		生命值是技能升级的“货币”
		小鸡共有10个技能 5项主动技 5项被动技 每捡拾一定米粒你会随机得到技能
		技能介绍


		键入e打开状态面板

		"""
		
		def _0(x, y, b) -> bool:
			if self.page < 9:
				self.page += 1
			else:
				game.setWindow(self.lastOpen)
			
			return True
		
		def _1(x, y, b) -> bool:
			if self.page > 0:
				self.page -= 1
			else:
				game.setWindow(self.lastOpen)
			return True
		
		def _2(x, y, b) -> bool:
			if b[0] == 1:
				game.setWindow(self.lastOpen)
			
			return True
		
		self._widgets.append(Button(Location.BOTTOM, 0.36, 0, 0.12, 0.08, RenderableString("\\.00FFFFFF\\01Next"), Description([RenderableString("继续")]), textLocation=Location.CENTER))
		self._widgets[0].onMouseDown = _0
		self._widgets.append(Button(Location.BOTTOM, 0.20, 0, 0.12, 0.08, RenderableString("\\.00FFFFFF\\01Previous"), Description([RenderableString("上一页")]), textLocation=Location.CENTER))
		self._widgets[1].onMouseDown = _1
		
		self._widgets[0].color = PresetColors.plotColor
		self._widgets[1].color = PresetColors.plotColor
		
		self._widgets[0].textColor = PresetColors.plotText
		self._widgets[1].textColor = PresetColors.plotText
		
		self._widgets.append(Button(Location.LEFT_TOP, 0, 0, 0.09, 0.12, RenderableString('\\01Back'), Description([RenderableString("返回")]), Location.CENTER))
		self._widgets[2].onMouseDown = _2
	
	def renderBackground(self, delta: float, at: BlockVector = BlockVector()) -> None:
		page = self.page
		if self._texture[page] is not None:
			w, h = renderer.getCanvas().get_size()
			texture_num = len(self._texture[page])
			for i in range(texture_num):
				size: BlockVector = renderer.getSize()
				pos = Vector(size.x * self._texture_position[page][i][0], size.y * self._texture_position[page][i][1])
				pic = self._texture[page][i]
				pic.adaptsUI(True)
				pic.renderAtInterface(pos)
		
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
		page = self.page
		super().render(delta)
		size: BlockVector = renderer.getSize()
		text_num = len(self._text[page])
		
		for i in range(text_num):
			renderer.renderString(RenderableString(f'\\.0040304D\\00{self._text[page][i]}'), int(size.x * self._text_position[page][i][0]), int(size.y * self._text_position[page][i][1]), 0xffffffff, Location.CENTER)
	
	def passRender(self, delta: float, at: Vector | None = None) -> None:
		s = Surface(renderer.getCanvas().get_size())
		s.fill(self.backgroundColor & 0x000000)
		
		renderer.getCanvas().blit(s, (0, 0))
		super().passRender(delta, at)


class EndPlotWindow(Window):
	def __init__(self):
		super().__init__("Plot")
		self._texture = resourceManager.getOrNew('window/plot_1')
		self._texture.systemScaleOffset = 0.064
		self._texture.adaptsMap(False)
		self._texture.adaptsSystem(True)
		game.getWorld(0).ending = True
		self.Sentence = 0
		
		def _0(x, y, b) -> bool:
			if self.Sentence < 3:
				self.Sentence += 1
			else:
				game.setWindow(None)
			return True
		
		def _1(x, y, b) -> bool:
			game.setWindow(None)
			return True
		
		def _2(x, y, b) -> bool:
			if self.Sentence > 0:
				self.Sentence -= 1
			return True
		
		self._widgets.append(Button(Location.BOTTOM, 0.22, 0, 0.12, 0.08, RenderableString("\\.00FFFFFF\\01NEXT"), Description([RenderableString("继续")]), textLocation=Location.CENTER))
		self._widgets[0].onMouseDown = _0
		self._widgets.append(Button(Location.BOTTOM, 0.38, 0, 0.12, 0.08, RenderableString("\\.00FFFFFF\\01SKIP"), Description([RenderableString("跳过剧情")]), textLocation=Location.CENTER))
		self._widgets[1].onMouseDown = _1
		self._widgets.append(Button(Location.BOTTOM, 0.06, 0, 0.12, 0.08, RenderableString("\\.00FFFF\\01BACK"), Description([RenderableString("上一页")]), textLocation=Location.CENTER))
		self._widgets[2].onMouseDown = _2
		
		self._widgets[0].color = PresetColors.plotColor
		self._widgets[1].color = PresetColors.plotColor
		self._widgets[2].color = PresetColors.plotColor
		
		self._widgets[0].textColor = PresetColors.plotText
		self._widgets[1].textColor = PresetColors.plotText
		self._widgets[2].textColor = PresetColors.plotText
	
	def render(self, delta: float) -> None:
		super().render(delta)
		size: BlockVector = renderer.getSize()
		if self.Sentence == 0:
			# 之前是0.62和0.28
			renderer.renderString(RenderableString('\\.0040304D\\00恭喜你！'), int(size.x * 0.5), int(size.y * 0.4), 0xffffffff, Location.CENTER)
			renderer.renderString(RenderableString('\\.0040304D\\00你已成功完成所有任务，并顺利产出你的蛋'), int(size.x * 0.5), int(size.y * 0.4 + font.realFontHeight), 0xffffffff, Location.CENTER)
		if self.Sentence == 1:
			renderer.renderString(RenderableString('\\.0040304D\\00你用事实证明'), int(size.x * 0.5), int(size.y * 0.4), 0xffffffff, Location.CENTER)
			renderer.renderString(RenderableString('\\.0040304D\\00你并不是一只一无是处的小鸡'), int(size.x * 0.5), int(size.y * 0.4 + font.realFontHeight), 0xffffffff, Location.CENTER)
		if self.Sentence == 2:
			renderer.renderString(RenderableString('\\.0040304D\\00你聪明、睿智、敏捷，'), int(size.x * 0.5), int(size.y * 0.4), 0xffffffff, Location.CENTER)
			renderer.renderString(RenderableString('\\.0040304D\\00是一个负责任的妈妈'), int(size.x * 0.5), int(size.y * 0.4 + font.realFontHeight), 0xffffffff, Location.CENTER)
		if self.Sentence == 3:
			renderer.renderString(RenderableString('\\.0040304D\\00游戏到此告一段落'), int(size.x * 0.5), int(size.y * 0.4), 0xffffffff, Location.CENTER)
			renderer.renderString(RenderableString('\\.0040304D\\00我们未来见。'), int(size.x * 0.5), int(size.y * 0.4 + font.realFontHeight), 0xffffffff, Location.CENTER)


anim1 = [resourceManager.getOrNew(f'window/nurturing/nurturing{t}') for t in range(1, 7)]
anim2 = [resourceManager.getOrNew(f'window/building2/building{t}') for t in range(0, 16)]

for t in anim1:
	t.adaptsMap(False)
	t.adaptsSystem(True)
	t.systemScaleOffset *= 5
	t.adaptsSystem()
	t.getSurface().set_colorkey((0, 0, 0))

for t in anim2:
	t.adaptsMap(False)
	t.adaptsSystem(True)
	t.systemScaleOffset *= 5
	t.adaptsSystem()
	t.getSurface().set_colorkey((0, 0, 0))
	t.setOffset(Vector(-5, 0))

del t
