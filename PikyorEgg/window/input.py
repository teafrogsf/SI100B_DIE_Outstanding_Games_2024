import asyncio
import os
import time

import pygame.event
from pygame import Surface

from interact.interacts import interact
from render import font
from render.font import Font
from render.renderer import Location, renderer
from utils.game import game
from utils.text import RenderableString, Description
from utils.util import utils
from window.widget import Widget, Button
from window.window import Window
from LLA import chat_with_ai as ai
from utils.text import font as _f

aiHistory: list = []
asyncAiTask = None
asyncTasks = asyncio.get_event_loop()  # 必须必须在main中最后关闭
asyncTasks.create_task(ai.getWords())


def adaptText(text: str, width: int, font: Font) -> list[str]:
	def isEmptyChar(c: chr) -> bool:
		if c == ' ' or c == '\n' or c == '\t' or c == '\r' or c == '\b' or c == '\v' or c == '\f' or c == '\0':
			return True
		return False
	
	def realAdaptText(_txt, _width, _font):
		texts = []
		_font = _font.get(False, False, False, False)
		length = len(_txt)
		pr = 0
		pe = min(30, length)
		space = _txt[:length - len(_txt.lstrip())]
		if len(space) != 0:
			dw = _font.size(space)[0]
			while dw > 0.3 * _width and len(space) != 0:
				space = space[:-1]
				dw = _font.size(space)
			if len(space) == 0:
				space = None
			else:
				_width -= dw
		else:
			space = None
		while pr < length:
			while _font.size(_txt[pr:pe])[0] < _width:
				pe += 1
				if pe >= length:
					break
			while _font.size(_txt[pr:pe])[0] > _width:
				if pe - pr == 1:
					break
				pe -= 1
			if pe < length:
				ori_pe = pe
				while not isEmptyChar(_txt[pe]):
					if pe == pr:
						pe = ori_pe
						break
					pe -= 1
			texts.append((_txt[pr:pe]) if space is None else (space + _txt[pr:pe]))
			pr = pe
			pe = min(30 + pr, length)
			continue
		return texts
	parses = []
	p, i = 0, 0
	while i < len(text):
		# 检查换行符
		if text[i] == '\n':
			parses.append(text[p:i])
			i += 1
			p = i
			continue
		i += 1
	if p != i:
		parses.append(text[p:i])
	ret = []
	for i in parses:
		ret.extend(realAdaptText(i, width, font))
	return ret


async def adaptAiReply(txt: str, aiHistory: list, window: 'AiWindow') -> None:
	res = await ai.send(txt)
	from render import font
	lis = adaptText(res['content'], int(0.7 * renderer.getCanvas().get_width()), font.allFonts[10])
	autoScroll = False
	if window.rendering - len(aiHistory) < 2:
		autoScroll = True
	aiHistory.append(RenderableString('\\10\\#ffee44cc' + res['role']))
	aiHistory.extend(lis)
	await asyncio.sleep(0.1)
	if autoScroll:
		window.rendering = len(aiHistory)


class InputWidget(Widget):
	
	def __init__(self, location: Location, x: float, y: float, width: float, height: float, name: RenderableString, description: Description, maxChar: int = 200):
		super().__init__(location, x, y, width, height, name, description, Location.LEFT, None)
		self._maxTextCount: int = 30
		self.textColor.click = self.textColor.hovering = self.textColor.active
		self.caret: int = 0
		self._caretOffset: int = 0  # 用于输入法那头的选中
		self._caret: int = -1  # 用于选中
		self.caretBlinkTime: int = -10
		self._realText: str = ''
		self._displayText: str | None = None
		self._dealTimeLimit: int = -1  # 长按按键时的响应时间间隔
		self._keyDealing: int = -1
		self._inputting: bool = False
	
	@staticmethod
	def emptyChar(c: chr) -> bool:
		if c == ' ' or c == '\n' or c == '\t' or c == '\r' or c == '\b' or c == '\v' or c == '\f' or c == '\0':
			return True
		return False
	
	def __checkKey(self, keyCode: int, lastDeal) -> int:
		status = interact.keys[keyCode] if keyCode < interact.KEY_COUNT else interact.specialKeys[keyCode & interact.KEY_COUNT]
		if self._keyDealing == -1 or self._keyDealing != keyCode:  # 争夺处理，无处理
			ret = status.dealPressTimes()
			if status.deals():
				self._keyDealing = keyCode
				self._dealTimeLimit = -1
				return max(ret, 1)
		else:  # 就在处理自身
			if not status.peek():
				self._keyDealing = 0
				return lastDeal
			ret = status.dealPressTimes()
			return max(ret, 1)
		return lastDeal
	
	def tick(self) -> None:
		if not self._inputting:
			self._dealTimeLimit = 8
			self.caretBlinkTime = -10
			if False:
				interact.keys[pygame.K_BACKSPACE].deals()
				interact.keys[pygame.K_DELETE].deals()
				interact.specialKeys[pygame.K_UP & interact.KEY_COUNT].deals()
				interact.specialKeys[pygame.K_DOWN & interact.KEY_COUNT].deals()
				interact.specialKeys[pygame.K_LEFT & interact.KEY_COUNT].deals()
				interact.specialKeys[pygame.K_RIGHT & interact.KEY_COUNT].deals()
			self._displayText = None
			self.caret = len(self._realText)
			return
		if self.caretBlinkTime <= -10:
			self.caretBlinkTime = 10
		else:
			self.caretBlinkTime -= 1
		if self._dealTimeLimit > 0:
			self._dealTimeLimit -= 1
		deals = self.__checkKey(pygame.K_BACKSPACE, 0)  # 当前应当处理的按键
		deals = self.__checkKey(pygame.K_DELETE, deals)
		deals = self.__checkKey(pygame.K_UP, deals)
		deals = self.__checkKey(pygame.K_DOWN, deals)
		deals = self.__checkKey(pygame.K_LEFT, deals)
		deals = self.__checkKey(pygame.K_RIGHT, deals)
		if deals == 0:
			self._dealTimeLimit = 8
			self._keyDealing = -1
		if self._dealTimeLimit > 0:
			self._dealTimeLimit -= 1
		else:
			if self._dealTimeLimit == -1:
				self._dealTimeLimit = 8  # 时间限制
			match self._keyDealing:
				case pygame.K_BACKSPACE:
					if self._caret != -1:
						self._caret, self.caret = min(self._caret, self.caret), max(self._caret, self.caret)
						self._realText = self._realText[:self._caret] + self._realText[self.caret:]
						self._caret = -1
						deals -= 1
					if deals > 0:  # 需要单个删除
						self.caret = min(self.caret, len(self._realText))
						if self.caret <= deals:
							if self.caret >= len(self._realText):
								self._realText = ''
							else:
								self._realText = self._realText[self.caret:]
						else:
							self._realText = self._realText[:self.caret - deals] + self._realText[self.caret:]
							self.caret -= deals
					self._keyDealing = pygame.K_BACKSPACE
					self._displayText = None
					self.caretBlinkTime = 10
				case pygame.K_DELETE:
					if self._caret != -1:
						self._caret, self.caret = min(self._caret, self.caret), max(self._caret, self.caret)
						self._realText = self._realText[:self._caret] + self._realText[self.caret:]
						self._caret = -1
						deals -= 1
					if deals > 0:  # 需要单个删除
						self.caret = min(self.caret, len(self._realText))
						if self.caret + deals >= len(self._realText):
							self._realText = self._realText[:self.caret]
						else:
							self._realText = self._realText[:self.caret] + self._realText[self.caret + deals:]
					self.caretBlinkTime = 10
				case pygame.K_LEFT:
					crt = self.caret
					crt -= deals
					if crt < 0:
						self.caret = 0
					else:
						self.caret = crt
					self.caretBlinkTime = 10
				case pygame.K_RIGHT:
					crt = self.caret
					crt += deals
					if crt > len(self._realText):
						self.caret = len(self._realText)
					else:
						self.caret = crt
					self.caretBlinkTime = 10
	
	def onInput(self, event) -> None:
		if not self._inputting:
			return
		assert isinstance(event, pygame.event.Event)
		assert event.type == pygame.TEXTINPUT
		self.caretBlinkTime = 10
		if self._caret != -1:
			self._caret, self.caret = min(self._caret, self.caret), max(self._caret, self.caret)
			self._realText = self._realText[:self._caret] + event.text + self._realText[self.caret:]
			self._caret = -1
		else:
			if self.caret >= len(self._realText):
				self._realText += event.text
				self.caret = len(self._realText)
			else:
				self._realText = self._realText[:self.caret] + event.text + self._realText[self.caret:]
				self.caret += len(event.text)
		self._displayText = None
		self._caretOffset = 0
	
	def onEdit(self, event) -> None:
		if not self._inputting:
			return
		assert isinstance(event, pygame.event.Event)
		assert event.type == pygame.TEXTEDITING
		self.caretBlinkTime = 10
		if self._caret != -1:
			self._caret, self.caret = min(self._caret, self.caret), max(self._caret, self.caret)
			self._displayText = self._realText[:self._caret] + event.text + self._realText[self.caret:]
		else:
			if self.caret >= len(self._realText):
				self._displayText = self._realText + event.text
			else:
				self._displayText = self._realText[:self.caret] + event.text + self._realText[self.caret:]
		self._caretOffset = event.start
	
	def render(self, delta: float) -> None:
		colorSelector = self.color.inactive if not self.active else self.color.active
		head = colorSelector & 0xff000000
		colorSelector -= head
		colorSelector = ((colorSelector >> 16) & 0xff, (colorSelector >> 8) & 0xff, colorSelector & 0xff)
		if head == 0xff000000:
			renderer.getCanvas().fill(colorSelector, (self._x, self._y, self._w, self._h))
		elif head != 0:
			s = Surface((self._w, self._h))
			s.fill(colorSelector)
			s.set_alpha(head >> 24)
			renderer.getCanvas().blit(s, (self._x, self._y))
		text = self._realText if self._displayText is None else self._displayText
		texts = []
		font = _f.allFonts[10].get(False, False, False, False)
		length = len(text)
		pr = 0
		pe = min(30, length)
		while pr < length:
			while font.size(text[pr:pe])[0] < self._w:
				pe += 1
				if pe >= length:
					break
			while font.size(text[pr:pe])[0] > self._w:
				if pe - pr == 1:
					break
				pe -= 1
			texts.append(text[pr:pe])
			pr = pe
			pe = min(30 + pr, length)
			continue
		if len(texts) == 0:
			offset = renderer.getOffset()
			rect = (self._x + offset.x, offset.y + self._y, 0, 0)
			pygame.key.set_text_input_rect(rect)
			if self.caretBlinkTime > 0:
				renderer.getCanvas().blit(font.render('  ', True, ((self.textColor.active >> 16) & 0xff ^ 0xff, (self.textColor.active >> 8) & 0xff ^ 0xff, self.textColor.active & 0xff ^ 0xff), ((self.color.active >> 16) & 0xff ^ 0xff, (self.color.active >> 8) & 0xff ^ 0xff, self.color.active & 0xff ^ 0xff)), (self._x, self._y))
		else:
			y0 = 0
			cc = self.caret + self._caretOffset
			c0 = self.caret
			sfc = Surface((self._w, self._h))
			sfc.fill(((self.color.active >> 16) & 0xff, (self.color.active >> 8) & 0xff, self.color.active & 0xff))
			for i in texts:
				sfc.blit(font.render(i, True, ((self.textColor.active >> 16) & 0xff, (self.textColor.active >> 8) & 0xff, self.textColor.active & 0xff), ((self.color.active >> 16) & 0xff, (self.color.active >> 8) & 0xff, self.color.active & 0xff)), (0, y0))
				if c0 > len(i):
					c0 -= len(i)
				else:
					offset = renderer.getOffset()
					rect = (self._x + font.size(i[:c0])[0] + offset.x, offset.y + y0 + self._y, 0, 0)
					pygame.key.set_text_input_rect(rect)
				if self.caretBlinkTime > 0:
					if cc > len(i):
						cc -= len(i)
					else:
						sfc.blit(font.render(i[cc] if cc < len(i) else '  ', True, ((self.textColor.active >> 16) & 0xff ^ 0xff, (self.textColor.active >> 8) & 0xff ^ 0xff, self.textColor.active & 0xff ^ 0xff), ((self.color.active >> 16) & 0xff ^ 0xff, (self.color.active >> 8) & 0xff ^ 0xff, self.color.active & 0xff ^ 0xff)), (font.size(i[:cc])[0], y0))
				y0 += _f.realHalfHeight
			renderer.getCanvas().blit(sfc, (self._x, self._y))
	
	def catch(self, val: bool = True) -> None:
		self._inputting = val
		if val:
			pygame.key.start_text_input()
		else:
			pygame.key.stop_text_input()
	
	def popText(self) -> str:
		text = self._realText
		self._realText = ''
		self._displayText = ''
		return text
	
	def getText(self) -> str:
		return self._realText


class InputWindow(Window):
	def __init__(self, name):
		super().__init__(name)
		self._inputer: InputWidget = InputWidget(Location.BOTTOM, 0, -0.05, 0.8, 0.2, RenderableString(""), Description())
		self._widgets.append(self._inputer)
		self._catches: Widget | None = self._inputer
		self._inputer.catch(True)
		self._history: list = []

	def tick(self) -> None:
		if interact.keys[pygame.K_ESCAPE].dealPressTimes():
			game.setWindow(self.lastOpen)
		if interact.specialKeys[pygame.K_KP_ENTER & interact.KEY_COUNT].dealPressTimes() or interact.keys[pygame.K_RETURN & interact.KEY_COUNT].dealPressTimes():
			txt = self._inputer.popText()
			if len(txt) != 0:
				self._history.append(txt)
	
	def onInput(self, event) -> None:
		if self._catches is self._inputer:
			self._inputer.onInput(event)
	
	def onEdit(self, event) -> None:
		if self._catches is self._inputer:
			self._inputer.onEdit(event)
	
	def passMouseDown(self, x: int, y: int, buttons: tuple[int, int, int]) -> None:
		catch = None
		for widget in self._widgets:
			if widget.isMouseIn(x, y):
				catch = widget
				widget.passMouseDown(x, y, buttons)
		self._catches = catch
		self._inputer.catch(catch is self._inputer)
	
	def passMouseUp(self, x: int, y: int, buttons: tuple[int, int, int]) -> None:
		catch = None
		for widget in self._widgets:
			if widget.isMouseIn(x, y):
				catch = widget
				widget.passMouseUp(x, y, buttons)
		self._catches = catch
		self._inputer.catch(catch is self._inputer)


class AiWindow(InputWindow):
	
	def __init__(self):
		super().__init__('ai')
		self.rendering: int = len(aiHistory)
		self.canRender: int = 0
	
	def tick(self) -> None:
		global aiHistory
		global asyncTasks
		global asyncAiTask
		if interact.keys[pygame.K_ESCAPE].deals():
			game.setWindow(self.lastOpen)
		if interact.specialKeys[pygame.K_KP_ENTER & interact.KEY_COUNT].deals() or interact.keys[pygame.K_RETURN & interact.KEY_COUNT].deals():
			if asyncAiTask is None or asyncAiTask.done():
				txt = self._inputer.popText()
				if len(txt) != 0:
					autoScroll = False
					if self.rendering - len(aiHistory) < 2:
						autoScroll = True
					from render import font
					aiHistory = aiHistory + [RenderableString('\\10\\#ffeeee00YOU')] + adaptText(txt, int(0.7 * renderer.getCanvas().get_width()), font.allFonts[10])
					asyncAiTask = asyncTasks.create_task(adaptAiReply(txt, aiHistory, self))
					if autoScroll:
						self.rendering = len(aiHistory)
		scr = interact.scroll.dealScroll()
		rd = self.rendering + scr
		if rd < self.canRender:
			rd = self.canRender
		if rd >= len(aiHistory):
			self.rendering = len(aiHistory)
		self.rendering = rd
	
	def render(self, delta: float) -> None:
		super().render(delta)
		from render import font
		h = int(0.6 * renderer.getCanvas().get_height())
		self.canRender: int = h // font.realHalfHeight
		x0 = int(0.1 * renderer.getCanvas().get_width())
		x1 = int(0.15 * renderer.getCanvas().get_width())
		y0 = int(0.7 * renderer.getCanvas().get_height())
		if self.rendering >= (lenHistory := len(aiHistory)):
			self.rendering = lenHistory
		for i in range(self.rendering - 1, max(self.rendering - self.canRender, 0) - 1, -1):
			y0 -= font.realHalfHeight
			text = aiHistory[i]
			if isinstance(text, RenderableString):
				text.renderAt(renderer.getCanvas(), x0, y0, 0xffffffff, 0)
			else:
				sfc = font.allFonts[10].get(False, False, False, False).render(text, True, 0xffffffff, 0)
				sfc.set_colorkey((0, 0, 0))
				renderer.getCanvas().blit(sfc, (x1, y0))


class _SeedWindow:
	nameExist = RenderableString("\\#ffee0044世界名称已存在")
	seedIllegal = RenderableString("\\#ffee4400种子必须是数字")
	both = nameExist + seedIllegal
	none = RenderableString("决定你的世界种子和世界名！")


class SeedWindow(InputWindow):
	def __init__(self):
		super().__init__("Seed")
		self._inputer.location = Location.CENTER
		self._inputer.x = 0
		self._inputer.y = -0.1
		self._inputer.width = 0.6
		self._inputer.height = font.realHalfHeight / renderer.getScreen().get_height()
		name = InputWidget(Location.CENTER, 0, 0, 0.6, self._inputer.height, RenderableString(""), Description())
		self._inputer = [self._inputer, name]
		self._widgets.append(name)
		self._info: RenderableString = _SeedWindow.none
		self._existNames: list[str] = []
		
		if os.path.exists('user') and os.path.exists('user/archive'):
			dl = os.listdir('user/archive')
			self._existNames = [i[:-5] for i in dl if i.endswith(".json")]
		
		def confirm(x, y, buttons):
			if buttons[0] == 1 and self._widgets[-1].active:
				worldName = self._inputer[1].getText()
				seed = self._inputer[0].getText()
				if len(seed) != 0:
					try:
						seed = int(self._inputer[0].getText())
					except Exception:
						return True
				else:
					seed = time.perf_counter_ns()
				if worldName in self._existNames:
					return True
				if len(worldName) == 0:
					worldName = f'{seed}序列世界'
					i = 0
					while worldName in self._existNames:
						i += 1
						worldName = f'{seed}序列世界（{i}）'
				from world.world import DynamicWorld
				world = DynamicWorld(worldName, seed)
				game.setWorld(world)
				game.setWindow(None)
			return True
		
		self._widgets.append(Button(Location.CENTER, 0, 0.1, 0.6, 0.08, RenderableString("\\01OK"), Description([RenderableString('创建世界')]), Location.CENTER))
		self._widgets[-1].onMouseDown = confirm
	
	def onResize(self) -> None:
		h = font.realHalfHeight / renderer.getScreen().get_height()
		self._inputer[0].height = h
		self._inputer[1].height = h
		super().onResize()

	def render(self, delta: float) -> None:
		super().render(delta)
		w, h = renderer.getCanvas().get_size()
		renderer.renderString(self._info, w >> 1, h >> 3, 0xffffffff, Location.TOP)
		renderer.renderString(RenderableString("Seed "), int(w * 0.2), int(h * 0.4), 0xffffffff, Location.RIGHT)
		renderer.renderString(RenderableString("Name "), int(w * 0.2), int(h * 0.5), 0xffffffff, Location.RIGHT)

	def tick(self) -> None:
		if interact.keys[pygame.K_ESCAPE].dealPressTimes():
			game.setWindow(self.lastOpen)
		flag1 = False
		try:
			if len(self._inputer[0].getText()) != 0:
				int(self._inputer[0].getText())
		except Exception:
			flag1 = True
		flag2 = self._inputer[1].getText() in self._existNames
		if flag1 and flag2:
			self._info = _SeedWindow.both
			self._widgets[-1].active = False
		elif flag1:
			self._info = _SeedWindow.seedIllegal
			self._widgets[-1].active = False
		elif flag2:
			self._info = _SeedWindow.nameExist
			self._widgets[-1].active = False
		else:
			self._info = _SeedWindow.none
			self._widgets[-1].active = True

	def onInput(self, event) -> None:
		utils.info(self._catches is self._inputer[0])
		if self._catches is not None and self._catches in self._inputer:
			utils.info("123")
			assert isinstance(self._catches, InputWidget)
			self._catches.onInput(event)
	
	def onEdit(self, event) -> None:
		if self._catches is not None and self._catches in self._inputer:
			assert isinstance(self._catches, InputWidget)
			self._catches.onEdit(event)
	
	def passMouseDown(self, x: int, y: int, buttons: tuple[int, int, int]) -> None:
		catch = None
		for widget in self._widgets:
			if widget.isMouseIn(x, y):
				catch = widget
				widget.passMouseDown(x, y, buttons)
		self._catches = catch
		self._inputer[0].catch(catch is self._inputer[0])
		self._inputer[1].catch(catch is self._inputer[1])
		if catch is self._inputer[0]:
			pygame.key.start_text_input()
	
	def passMouseUp(self, x: int, y: int, buttons: tuple[int, int, int]) -> None:
		catch = None
		for widget in self._widgets:
			if widget.isMouseIn(x, y):
				catch = widget
				widget.passMouseUp(x, y, buttons)
		self._catches = catch
		self._inputer[0].catch(catch is self._inputer[0])
		self._inputer[1].catch(catch is self._inputer[1])
		if catch is self._inputer[0]:
			pygame.key.start_text_input()
