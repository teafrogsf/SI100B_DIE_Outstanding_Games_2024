from typing import Callable

from pygame import Surface

from render.renderable import Renderable
from render.renderer import renderer, Location
from render.resource import Texture
from utils.game import game
from utils.text import Description, RenderableString
from utils.util import utils

from utils.vector import BlockVector


class ColorSet:
	def __init__(self, isText: bool = True):
		if isText:
			self.inactive: int = 0xff444444
			self.active: int = 0xffeeeeee
			self.hovering: int = 0xff000000
			self.click: int = 0xff000000
		else:
			self.inactive: int = 0xffaaaaaa
			self.active: int = 0xff111111
			self.hovering: int = 0xffeeeeee
			self.click: int = 0xffcccccc
	
	def clone(self) -> 'ColorSet':
		ret = ColorSet()
		ret.active = self.active
		ret.inactive = self.inactive
		ret.hovering = self.hovering
		ret.click = self.click
		return ret


class Widget(Renderable):
	"""
	你可以为控件定义很多属性。属性中，所有带on前缀的都应当是函数类型的事件响应器。\n
	以下所有的事件都可以置None，或者传入回调函数。\n
	大多数事件回调类型都是(x: int, y: int) -> bool，返回true则表示阻断事件传递。\n
	onHover，鼠标浮游在控件上时调用。\n
	onClick，鼠标点击时触发。指的是，鼠标按下，且抬起时触发。\n
	onMouseDown，鼠标按下。\n
	onMouseUp，鼠标抬起。\n
	onTick，每tick调用。\n
	_x, _y, _w, _h与公开的x, y, width, height不同。前者的单位是屏幕像素；后者的单位是窗口，例如x=0.5意味着x坐标位于屏幕的一半。
	"""
	
	def __init__(self, location: Location, x: float, y: float, width: float, height: float, name: RenderableString, description: Description, textLocation: Location = Location.CENTER, texture: Texture = None):
		"""
		创建控件。注意，位置取屏幕的相对位置。如果取LEFT_TOP，则x, y指代控件左上角与窗口左上角的相对位置；如果取RIGHT，则x, y分别指代控件右边与窗口右边的相对位置，和控件正中央与屏幕纵向正中央的相对位置
		:param location: 位置
		:param x: 横坐标，一般取-1~1，表示窗口占比
		:param y: 纵坐标，一般取-1~1，表示窗口占比
		:param width: 宽度
		:param height: 高度
		:param name: 控件显示名称
		:param description: 控件描述
		:param texture: 控件背景纹理
		"""
		super().__init__(texture)
		self.location: Location = location
		self.textLocation: Location = textLocation
		self.x: float = x
		self.y: float = y
		self.width: float = width
		self.height: height = height
		self.name: RenderableString = name
		self.description: Description = description
		self._x: int = 0
		self._y: int = 0
		self._w: int = 0
		self._h: int = 0
		self._isMouseIn: bool = False
		self.active: bool = True
		self.onHover: Callable[[int, int, tuple[int, int, int]], bool] | None = None
		self.onClick: Callable[[int, int, tuple[int, int, int]], bool] | None = None
		self.onMouseUp: Callable[[int, int, tuple[int, int, int]], bool] | None = None
		self.onMouseDown: Callable[[int, int, tuple[int, int, int]], bool] | None = None
		self.onTick: Callable[[], int] | None = None
		self.color: ColorSet = ColorSet(False)
		self.textColor: ColorSet = ColorSet(True)
	
	def render(self, delta: float) -> None:
		if self._texture is not None:
			self._texture.renderAtInterface(BlockVector(self._x, self._y))
		else:
			colorSelector = self.color.inactive if not self.active else self.color.active if not self._isMouseIn else self.color.hovering
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
		match self.textLocation:
			case Location.LEFT_TOP:
				renderer.renderString(self.name, self._x, self._y, self.textColor.inactive if not self.active else self.textColor.active if not self._isMouseIn else self.textColor.hovering, Location.LEFT_TOP, self.color.inactive if not self.active else self.color.active if not self._isMouseIn else self.color.hovering)
			case Location.LEFT:
				renderer.renderString(self.name, self._x, self._y + (self._h >> 1), self.textColor.inactive if not self.active else self.textColor.active if not self._isMouseIn else self.textColor.hovering, Location.LEFT, self.color.inactive if not self.active else self.color.active if not self._isMouseIn else self.color.hovering)
			case Location.LEFT_BOTTOM:
				renderer.renderString(self.name, self._x, self._y + self._h, self.textColor.inactive if not self.active else self.textColor.active if not self._isMouseIn else self.textColor.hovering, Location.LEFT_BOTTOM, self.color.inactive if not self.active else self.color.active if not self._isMouseIn else self.color.hovering)
			case Location.TOP:
				renderer.renderString(self.name, self._x + (self._w >> 1), self._y, self.textColor.inactive if not self.active else self.textColor.active if not self._isMouseIn else self.textColor.hovering, Location.TOP, self.color.inactive if not self.active else self.color.active if not self._isMouseIn else self.color.hovering)
			case Location.CENTER:
				renderer.renderString(self.name, self._x + (self._w >> 1), self._y + (self._h >> 1), self.textColor.inactive if not self.active else self.textColor.active if not self._isMouseIn else self.textColor.hovering, Location.CENTER, self.color.inactive if not self.active else self.color.active if not self._isMouseIn else self.color.hovering)
			case Location.BOTTOM:
				renderer.renderString(self.name, self._x + (self._w >> 1), self._y + self._h, self.textColor.inactive if not self.active else self.textColor.active if not self._isMouseIn else self.textColor.hovering, Location.BOTTOM, self.color.inactive if not self.active else self.color.active if not self._isMouseIn else self.color.hovering)
			case Location.RIGHT_TOP:
				renderer.renderString(self.name, self._x + self._w, self._y, self.textColor.inactive if not self.active else self.textColor.active if not self._isMouseIn else self.textColor.hovering, Location.RIGHT_TOP, self.color.inactive if not self.active else self.color.active if not self._isMouseIn else self.color.hovering)
			case Location.RIGHT:
				renderer.renderString(self.name, self._x + self._w, self._y + (self._h >> 1), self.textColor.inactive if not self.active else self.textColor.active if not self._isMouseIn else self.textColor.hovering, Location.RIGHT, self.color.inactive if not self.active else self.color.active if not self._isMouseIn else self.color.hovering)
			case Location.RIGHT_BOTTOM:
				renderer.renderString(self.name, self._x + self._w, self._y + self._h, self.textColor.inactive if not self.active else self.textColor.active if not self._isMouseIn else self.textColor.hovering, Location.RIGHT_BOTTOM, self.color.inactive if not self.active else self.color.active if not self._isMouseIn else self.color.hovering)
	
	def onResize(self) -> None:
		"""
		根据预设调整具体位置。可以重写，但是注意逻辑和算法不要错了
		"""
		windowSize: BlockVector = renderer.getSize()
		self._w, self._h = int(self.width * windowSize.x), int(self.height * windowSize.y)
		match self.location:
			case Location.LEFT_TOP:
				self._x, self._y = int(self.x * windowSize.x), int(self.y * windowSize.y)
			case Location.LEFT:
				self._x, self._y = int(self.x * windowSize.x), (windowSize.y - self._h >> 1) + int(self.y * windowSize.y)
			case Location.LEFT_BOTTOM:
				self._x, self._y = int(self.x * windowSize.x), int(windowSize.y - self._h + self.y * windowSize.y)
			case Location.TOP:
				self._x, self._y = (windowSize.x - self._w >> 1) + int(self.x * windowSize.x), int(self.y * windowSize.y)
			case Location.CENTER:
				self._x, self._y = (windowSize.x - self._w >> 1) + int(self.x * windowSize.x), (windowSize.y - self._h >> 1) + int(self.y * windowSize.y)
			case Location.BOTTOM:
				self._x, self._y = (windowSize.x - self._w >> 1) + int(self.x * windowSize.x), int(windowSize.y - self._h + self.y * windowSize.y)
			case Location.RIGHT_TOP:
				self._x, self._y = int((windowSize.x - self._w) + self.x * windowSize.x), int(self.y * windowSize.y)
			case Location.RIGHT:
				self._x, self._y = int((windowSize.x - self._w) + self.x * windowSize.x), (windowSize.y - self._h >> 1) + int(self.y * windowSize.y)
			case Location.RIGHT_BOTTOM:
				self._x, self._y = int((windowSize.x - self._w) + self.x * windowSize.x), int(windowSize.y - self._h + self.y * windowSize.y)
	
	def isMouseIn(self, x: int, y: int):
		self._isMouseIn = self._x <= x <= self._x + self._w and self._y <= y <= self._y + self._h
		if self._isMouseIn:
			game.floatWindow.change(self.description)
		return self._isMouseIn
	
	def tick(self) -> None:
		"""
		可以重写，默认为调用self.onTick
		:return:
		"""
		if self.onTick is not None:
			self.onTick()
	
	def click(self, x: int, y: int, buttons: tuple[int, int, int]) -> bool:
		if self.onClick is not None:
			return self.onClick(x, y, buttons)
	
	def passHover(self, x: int, y: int, buttons: tuple[int, int, int]):
		if self.onHover is not None:
			return self.onHover(x, y, buttons)
	
	def passClick(self, x: int, y: int, buttons: tuple[int, int, int]):
		if self.onClick is not None:
			return self.onClick(x, y, buttons)
	
	def passMouseDown(self, x: int, y: int, buttons: tuple[int, int, int]):
		if self.onMouseDown is not None:
			return self.onMouseDown(x, y, buttons)
	
	def passMouseUp(self, x: int, y: int, buttons: tuple[int, int, int]):
		if self.onMouseUp is not None:
			return self.onMouseUp(x, y, buttons)


class Button(Widget):
	def __init__(self, location: Location, x: float, y: float, width: float, height: float, name: RenderableString, description: Description, textLocation: Location = Location.CENTER, texture: Texture = None):
		super().__init__(location, x, y, width, height, name, description, textLocation, texture)


class Slider(Widget):
	def __init__(self, location: Location, x: float, y: float, width: float, height: float, name: RenderableString, description: Description, textLocation: Location = Location.CENTER, texture: Texture = None):
		super().__init__(location, x, y, width, height, name, description, textLocation, texture)
		self.offset = BlockVector()
		self.pull: bool = False
		self.value: float = 0
		self.onDrag: Callable[[float], None] | None = None
		self.barColor: ColorSet = ColorSet()
		self.barColor.inactive = (~self.color.inactive & 0xffffff) | ((self.color.inactive >> 2) & 0xff000000)
		self.barColor.hovering = (~self.color.hovering & 0xffffff) | ((self.color.hovering >> 2) & 0xff000000)
		self.barColor.active = (~self.color.active & 0xffffff) | ((self.color.active >> 2) & 0xff000000)
		self.barColor.click = (~self.color.click & 0xffffff) | ((self.color.click >> 2) & 0xff000000)

	def isMouseIn(self, x: int, y: int):
		if self.pull:
			self.value = utils.frange((x - self._x) / self._w, 0, 1)
			if self.onDrag:
				self.onDrag(self.value)
			return True
		return super().isMouseIn(x, y)
	
	def passMouseDown(self, x: int, y: int, buttons: tuple[int, int, int]):
		if buttons[0] == 1:
			self.pull = True
		if self.onMouseDown is not None:
			return self.onMouseDown(x, y, buttons)
	
	def passMouseUp(self, x: int, y: int, buttons: tuple[int, int, int]):
		if buttons[0] == 1:
			self.pull = False
		if self.onMouseUp is not None:
			return self.onMouseUp(x, y, buttons)
	
	def render(self, delta: float) -> None:
		if self._texture is not None:
			self._texture.renderAtInterface(BlockVector(self._x, self._y))
		else:
			colorSelector = self.color.inactive if not self.active else self.color.active if not self._isMouseIn else self.color.hovering
			colorReversed = self.barColor.inactive if not self.active else self.barColor.active if not self._isMouseIn else self.barColor.hovering
			head = colorSelector & 0xff000000
			head2 = colorReversed & 0xff000000
			colorSelector -= head
			colorSelector = ((colorSelector >> 16) & 0xff, (colorSelector >> 8) & 0xff, colorSelector & 0xff)
			colorReversed = ((colorReversed >> 16) & 0xff, (colorReversed >> 8) & 0xff, colorReversed & 0xff)
			if head == 0xff000000:
				renderer.getCanvas().fill(colorSelector, (self._x, self._y, self._w, self._h))
			elif head != 0:
				s = Surface((self._w, self._h))
				s.fill(colorSelector)
				s.set_alpha(head >> 24)
				renderer.getCanvas().blit(s, (self._x, self._y))
			if head2 == 0xff000000:
				renderer.getCanvas().fill(colorReversed, (self._x, self._y, self._w * self.value, self._h))
			elif head2 != 0:
				s = Surface((self._w * self.value, self._h))
				s.fill(colorReversed)
				s.set_alpha(head2 >> 24)
				renderer.getCanvas().blit(s, (self._x, self._y))
		name = self.name.clone().append(f'\\01: {self.value * 100:.2f}%')
		match self.textLocation:
			case Location.LEFT_TOP:
				renderer.renderString(name, self._x, self._y, self.textColor.inactive if not self.active else self.textColor.active if not self._isMouseIn else self.textColor.hovering, Location.LEFT_TOP, self.color.inactive if not self.active else self.color.active if not self._isMouseIn else self.color.hovering)
			case Location.LEFT:
				renderer.renderString(name, self._x, self._y + (self._h >> 1), self.textColor.inactive if not self.active else self.textColor.active if not self._isMouseIn else self.textColor.hovering, Location.LEFT, self.color.inactive if not self.active else self.color.active if not self._isMouseIn else self.color.hovering)
			case Location.LEFT_BOTTOM:
				renderer.renderString(name, self._x, self._y + self._h, self.textColor.inactive if not self.active else self.textColor.active if not self._isMouseIn else self.textColor.hovering, Location.LEFT_BOTTOM, self.color.inactive if not self.active else self.color.active if not self._isMouseIn else self.color.hovering)
			case Location.TOP:
				renderer.renderString(name, self._x + (self._w >> 1), self._y, self.textColor.inactive if not self.active else self.textColor.active if not self._isMouseIn else self.textColor.hovering, Location.TOP, self.color.inactive if not self.active else self.color.active if not self._isMouseIn else self.color.hovering)
			case Location.CENTER:
				renderer.renderString(name, self._x + (self._w >> 1), self._y + (self._h >> 1), self.textColor.inactive if not self.active else self.textColor.active if not self._isMouseIn else self.textColor.hovering, Location.CENTER, self.color.inactive if not self.active else self.color.active if not self._isMouseIn else self.color.hovering)
			case Location.BOTTOM:
				renderer.renderString(name, self._x + (self._w >> 1), self._y + self._h, self.textColor.inactive if not self.active else self.textColor.active if not self._isMouseIn else self.textColor.hovering, Location.BOTTOM, self.color.inactive if not self.active else self.color.active if not self._isMouseIn else self.color.hovering)
			case Location.RIGHT_TOP:
				renderer.renderString(name, self._x + self._w, self._y, self.textColor.inactive if not self.active else self.textColor.active if not self._isMouseIn else self.textColor.hovering, Location.RIGHT_TOP, self.color.inactive if not self.active else self.color.active if not self._isMouseIn else self.color.hovering)
			case Location.RIGHT:
				renderer.renderString(name, self._x + self._w, self._y + (self._h >> 1), self.textColor.inactive if not self.active else self.textColor.active if not self._isMouseIn else self.textColor.hovering, Location.RIGHT, self.color.inactive if not self.active else self.color.active if not self._isMouseIn else self.color.hovering)
			case Location.RIGHT_BOTTOM:
				renderer.renderString(name, self._x + self._w, self._y + self._h, self.textColor.inactive if not self.active else self.textColor.active if not self._isMouseIn else self.textColor.hovering, Location.RIGHT_BOTTOM)


class PullObject(Widget):
	def __init__(self, location: Location, x: float, y: float, width: float, height: float, name: RenderableString, description: Description, textLocation: Location = Location.CENTER, texture: Texture = None):
		super().__init__(location, x, y, width, height, name, description, textLocation, texture, )
		self.offset = BlockVector()
		self.pull = False
			
		def down(x, y, buttons):
			self.pull = True
			self.offset.set(x - self._x, y - self._y)
			return True
	
		def up(x, y, buttons):
			self.pull = False
			return True
		
		self.onMouseDown = down
		self.onMouseUp = up

	def isMouseIn(self, x: int, y: int):
		if self.pull:
			self._x = x - self.offset.x
			self._y = y - self.offset.y
			match self.location:
				case Location.LEFT_TOP:
					self.x = self._x / renderer.getCanvas().get_width()
					self.y = self._y / renderer.getCanvas().get_height()
				case Location.LEFT:
					self.x = self._x / renderer.getCanvas().get_width()
					self.y = (self._y - (renderer.getSize().y - self._h >> 1)) / renderer.getCanvas().get_height()
				case Location.LEFT_BOTTOM:
					self.x = self._x / renderer.getCanvas().get_width()
					self.y = (self._y - (renderer.getSize().y - self._h)) / renderer.getCanvas().get_height()
				case Location.TOP:
					self.x = (self._x - (renderer.getSize().x - self._w >> 1)) / renderer.getCanvas().get_width()
					self.y = self._y / renderer.getCanvas().get_height()
				case Location.CENTER:
					self.x = (self._x - (renderer.getSize().x - self._w >> 1)) / renderer.getCanvas().get_width()
					self.y = (self._y - (renderer.getSize().y - self._h >> 1)) / renderer.getCanvas().get_height()
				case Location.BOTTOM:
					self.x = (self._x - (renderer.getSize().x - self._w >> 1)) / renderer.getCanvas().get_width()
					self.y = (self._y - (renderer.getSize().y - self._h)) / renderer.getCanvas().get_height()
				case Location.RIGHT_TOP:
					self.x = (self._x - (renderer.getSize().x - self._w)) / renderer.getCanvas().get_width()
					self.y = self._y / renderer.getCanvas().get_height()
				case Location.RIGHT:
					self.x = (self._x - (renderer.getSize().x - self._w)) / renderer.getCanvas().get_width()
					self.y = (self._y - (renderer.getSize().y - self._h >> 1)) / renderer.getCanvas().get_height()
				case Location.RIGHT_BOTTOM:
					self.x = (self._x - (renderer.getSize().x - self._w)) / renderer.getCanvas().get_width()
					self.y = (self._y - (renderer.getSize().y - self._h)) / renderer.getCanvas().get_height()
			self._isMouseIn = True
			return True
		return super().isMouseIn(x, y)
