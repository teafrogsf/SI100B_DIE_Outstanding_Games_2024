from enum import Enum
from typing import Union, TYPE_CHECKING

from interact.interacts import interact
from render import font
from save import configs
from utils.util import utils
from utils.text import RenderableString

if TYPE_CHECKING:
	from entity.entity import Entity

import pygame
from pygame import Surface
from utils.vector import Vector, BlockVector
from utils.error import IllegalStatusException, InvalidOperationException
from utils.sync import SynchronizedStorage


# from utils.game import game
# 不可以import game，否则会导致循环导入


class Location(Enum):
	LEFT_TOP = 0
	"""
	左上角
	"""
	LEFT = 1
	"""
	左居中
	"""
	LEFT_BOTTOM = 2
	"""
	左下角
	"""
	TOP = 3
	"""
	上居中
	"""
	CENTER = 4
	"""
	正中心
	"""
	BOTTOM = 5
	"""
	下居中
	"""
	RIGHT_TOP = 6
	"""
	右上角
	"""
	RIGHT = 7
	"""
	右居中
	"""
	RIGHT_BOTTOM = 8
	"""
	右下角
	"""


class Renderer:
	def __init__(self):
		super().__init__()
		self._screen: Surface | None = None  # 屏幕
		self._size: tuple[float, float] = (0, 0)
		
		self._canvas: Surface | None = None  # 用于预绘制的画布
		self._canvasSize: BlockVector = BlockVector()
		self._canvasCenter: BlockVector = BlockVector()
		
		self._isRendering: bool = False
		
		self.cameraOffset: Vector = Vector(0.0, 0.0)
		self._camera: SynchronizedStorage[Vector] = SynchronizedStorage[Vector](Vector(0.0, 0.0))
		self._cameraAt: Union['Entity', None] = None
		
		self._systemScale: int = 1  # 系统窗口导致的缩放
		self._systemScaleChanged: bool = True
		self._mapScale: int = 1  # 自定义的地图缩放
		self._mapScaleChanged: bool = True
		self._uiScale: int = 1  # UI单独的缩放
		self._uiScaleChanged: bool = True
		
		self._offset: BlockVector = BlockVector()
		
		self._customMapScale: float = 1.0
		self._customUiScale: float = 1.0
		self._mapBasis: BlockVector = BlockVector()
		self._mapObjectBasis: BlockVector = BlockVector()
		self.is4to3: SynchronizedStorage[bool] = SynchronizedStorage[bool](True)
		
		self.displayFPS: bool = False
		self.displayTPS: bool = False
		self.tps: float = 0
		self.fps: float = 0
		self.lockScroll: bool = False
	
	def setScreen(self, screen: Surface) -> None:
		"""
		设置屏幕Surface
		"""
		self._screen = screen
		self._size = screen.get_size()
		if self.is4to3.get():
			if self._size[0] / self._size[1] > 4 / 3:
				self._offset = BlockVector(int(self._size[0] - self._size[1] * 4 / 3) >> 1, 0)
			elif self._size[0] / self._size[1] < 4 / 3:
				self._offset = BlockVector(0, int(self._size[1] - self._size[0] / 4 * 3) >> 1)
			else:
				self._offset = BlockVector(0, 0)
			self.setSystemScale(min(self._size[0] // 12, self._size[1] // 9))
		else:
			if self._size[0] / self._size[1] > 16 / 9:
				self._offset = BlockVector(int(self._size[0] - self._size[1] * 16 / 9) >> 1, 0)
			elif self._size[0] / self._size[1] < 16 / 9:
				self._offset = BlockVector(0, int(self._size[1] - self._size[0] / 16 * 9) >> 1)
			else:
				self._offset = BlockVector(0, 0)
			self.setSystemScale(min(self._size[0] // 16, self._size[1] // 9))
		self._canvasSize = BlockVector(self._size[0], self._size[1]).subtract(self._offset).subtract(self._offset)
		self._canvas = Surface(self._canvasSize.getTuple())
		self._canvasCenter.set(self._canvasSize.x >> 1, self._canvasSize.y >> 1)
	
	def cameraAt(self, entity: Union['Entity', None]) -> 'Entity':
		e = self._cameraAt
		self._cameraAt = entity
		return e
	
	def getCameraAt(self) -> Union['Entity', None]:
		return self._cameraAt
	
	def begin(self, delta: float, noWindow: bool) -> None:
		"""
		仅在game.render中调用
		"""
		if self._isRendering:
			raise IllegalStatusException("尝试开始绘制，但是绘制已经开始。")
		if noWindow and not self.lockScroll and interact.scroll.peekScroll() != 0:
			newScale = self._customMapScale * (0.8 ** interact.scroll.dealScroll())
			newScale = utils.frange(newScale, 0.8, 5)
			if newScale != self._customMapScale:
				self._customMapScale = newScale
				self._mapScaleChanged = True
		self._isRendering = True
		# begin apply sync
		if self._cameraAt is None:
			if self._camera.get() == self._camera.getNew():
				off = self.cameraOffset
				self.cameraOffset = Vector(0, 0)
				self._camera.apply(self._camera.getNew().add(off).clone())
			else:
				self._camera.apply(self._camera.getNew().clone())
				self.cameraOffset.set(0, 0)
		else:
			self._camera.get().set(self._cameraAt.updatePosition(delta))
			self._camera.getNew().set(self._camera.get().clone())
			self._camera.get().add(self.cameraOffset)
		self._mapBasis = self._canvasCenter.clone().subtract(self._camera.get().clone().multiply(self._mapScale).getBlockVector())
		self._mapObjectBasis = self._mapBasis.clone().subtract(self._mapScale >> 1, self._mapScale >> 1)
		self.is4to3.apply(self.is4to3.getNew())
		# end apply sync
		self._screen.fill(0)
		self._canvas.fill(0)
		
	def end(self) -> None:
		"""
		只在渲染帧结束时调用
		:return:
		"""
		if not self._isRendering:
			raise IllegalStatusException("尝试结束绘制，但是绘制尚未开始。")
		self._screen.blit(self._canvas, self._offset.getTuple())
		if self.displayFPS:
			r = RenderableString(f"\\12{self.fps:.2f} FPS")
			r.renderAt(self._screen, int(self._size[0] - r.length()), 0, 0xffee0000)
			if self.displayTPS:
				r = RenderableString(f"\\12{self.tps:.2f} TPS")
				r.renderAt(self._screen, int(self._size[0] - r.length()), font.realHalfHeight, 0xffee0000)
		elif self.displayTPS:
			r = RenderableString(f"\\12{self.tps:.2f} TPS")
			r.renderAt(self._screen, int(self._size[0] - r.length()), 0, 0xffee0000)
		pygame.display.flip()
		self._isRendering = False
	
	def assertRendering(self) -> None:
		"""
		该函数可能抛出错误。这个错误不应被手动捕捉，因为抛出这个错误说明是代码逻辑上出现了问题。一些操作应当在渲染时进行，但是在非渲染时刻进行了这一操作，就会报错
		:raises: InvalidOperationError
		"""
		if self._isRendering:
			return
		raise InvalidOperationException('操作需要在渲染时进行。当前未进行渲染。')
	
	def assertNotRendering(self) -> None:
		"""
		该函数可能抛出错误。这个错误不应被手动捕捉，因为抛出这个错误说明是代码逻辑上出现了问题。一些操作应当在非渲染时刻进行，但是在渲染时刻进行了这一操作，就会报错
		:raises: InvalidOperationError
		"""
		if not self._isRendering:
			return
		raise InvalidOperationException('操作需要在非渲染时进行。当前正在渲染。')
	
	def getSize(self) -> BlockVector:
		return self._canvasSize
	
	def getCenter(self) -> BlockVector:
		return self._canvasCenter.clone()
	
	def getCanvas(self) -> Surface:
		return self._canvas
	
	def getScreen(self) -> Surface:
		return self._screen
	
	def getCamera(self) -> SynchronizedStorage['Vector']:
		return self._camera
	
	def getOffset(self) -> BlockVector:
		return self._offset.clone()
	
	def getMapObjectBasis(self) -> BlockVector:
		return self._mapObjectBasis
	
	def getMapBasis(self) -> BlockVector:
		return self._mapBasis
	
	def fill(self, color: int, x: int, y: int, w: int, h: int) -> None:
		if color & 0xff000000 == 0xff000000:
			self._canvas.fill(((color >> 16) & 0xff, (color >> 8) & 0xff, color & 0xff), (x, y, w, h))
		else:
			s = Surface((w, h))
			s.fill(((color >> 16) & 0xff, (color >> 8) & 0xff, color & 0xff))
			s.set_alpha(color >> 24)
			self._canvas.blit(s, (x, y))
	
	def renderAtMap(self, src: Surface, mapPoint: Vector, fromPos: Vector | None = None, fromSize: Vector | None = None, pxOffset: BlockVector = None) -> None:
		"""
		按地图的方式渲染目标，会忽略margin，会考虑camera
		"""
		self.assertRendering()
		dst = self._canvas
		if fromPos is None or fromSize is None:
			p = (mapPoint * self._mapScale).getBlockVector().add(self._mapObjectBasis)
			if pxOffset is not None:
				p.add(pxOffset)
			dst.blit(src, p.getTuple())
		else:
			p = ((mapPoint + fromPos) * self._mapScale).getBlockVector().add(self._mapObjectBasis)
			if pxOffset is not None:
				p.add(pxOffset)
			dst.blit(src, p.getTuple(), (fromPos.x, fromPos.y, fromSize.x, fromSize.y))
	
	def renderAsBlock(self, src: Surface, mapPoint: BlockVector | Vector, fromPos: BlockVector | None = None, fromSize: BlockVector | None = None):
		self.assertRendering()
		if fromPos is None or fromSize is None:
			self._canvas.blit(src, self._mapBasis.clone().add(mapPoint.clone().multiply(self._mapScale)).getTuple())
		else:
			self._canvas.blit(src, self._mapBasis.clone().add((mapPoint + fromPos).multiply(self._mapScale)).getTuple(), (fromPos.x, fromPos.y, fromSize.x, fromSize.y))
	
	def renderString(self, text: RenderableString, x: int, y: int, defaultColor: int, location: Location = Location.LEFT_TOP, defaultBackground: int = 0, forceSize: int = 0) -> None:
		"""
		:param text: 要显示的文本
		:param x: 参考坐标
		:param y: 参考坐标
		:param defaultColor: 默认颜色
		:param location: 渲染位置，默认左上角
		:param defaultBackground: 默认背景色，传入0xff有助于提升性能
		:param forceSize: 强制渲染小(-1)/大(1)字体，或按原字体渲染(0 and other)
		"""
		self.assertRendering()
		if len(text.set) == 0:
			return
		height = font.realFontHeight if text.set[0].font < 10 or forceSize == 1 else font.realHalfHeight
		renderFunction = text.renderSmall if forceSize == -1 else text.renderGiant if forceSize == 1 else text.renderAt
		match location:
			case Location.LEFT_TOP:
				renderFunction(self._canvas, x, y, defaultColor, defaultBackground)
			case Location.LEFT:
				renderFunction(self._canvas, x, y - (height >> 1), defaultColor, defaultBackground)
			case Location.LEFT_BOTTOM:
				renderFunction(self._canvas, x, y - height, defaultColor, defaultBackground)
			case Location.TOP:
				renderFunction(self._canvas, x - ((text.lengthSmall() if forceSize == -1 else text.lengthGiant() if forceSize == 1 else text.length()) >> 1), y, defaultColor, defaultBackground)
			case Location.CENTER:
				renderFunction(self._canvas, x - ((text.lengthSmall() if forceSize == -1 else text.lengthGiant() if forceSize == 1 else text.length()) >> 1), y - (height >> 1), defaultColor, defaultBackground)
			case Location.BOTTOM:
				renderFunction(self._canvas, x - ((text.lengthSmall() if forceSize == -1 else text.lengthGiant() if forceSize == 1 else text.length()) >> 1), y - height, defaultColor, defaultBackground)
			case Location.RIGHT_TOP:
				renderFunction(self._canvas, x - (text.lengthSmall() if forceSize == -1 else text.lengthGiant() if forceSize == 1 else text.length()), y, defaultColor, defaultBackground)
			case Location.RIGHT:
				renderFunction(self._canvas, x - (text.lengthSmall() if forceSize == -1 else text.lengthGiant() if forceSize == 1 else text.length()), y - (height >> 1), defaultColor, defaultBackground)
			case Location.RIGHT_BOTTOM:
				renderFunction(self._canvas, x - (text.lengthSmall() if forceSize == -1 else text.lengthGiant() if forceSize == 1 else text.length()), y - height, defaultColor, defaultBackground)
	
	def setUiScale(self, scl: float) -> None:
		self._customUiScale = scl
		self._uiScaleChanged = True
	
	def setSystemScale(self, scl: int) -> None:
		self._systemScale = int(scl)
		self._systemScaleChanged = True
		self._uiScaleChanged = True
		self._mapScaleChanged = True
	
	def getSystemScale(self) -> float:
		return self._systemScale
	
	def setCustomMapScale(self, scl: float) -> None:
		self._customMapScale = scl
		self._mapScaleChanged = True
	
	def getCustomMapScale(self) -> float:
		return self._customMapScale
	
	def getMapScale(self) -> float:
		return self._mapScale
	
	def dealScreen4to3Change(self) -> bool:
		if self.is4to3.get() != self.is4to3.getNew():
			self.is4to3.apply(self.is4to3.getNew())
			self.setScreen(self._screen)
			return True
		return False
	
	def peekScaleChange(self) -> bool:
		"""
		应当仅在main.py, renderThread中调用
		:return:
		"""
		flag = False
		if self._mapScaleChanged:
			self._mapScale = int(self._customMapScale * self._systemScale)
			flag = True
		if self._uiScaleChanged:
			self._uiScale = int(self._customUiScale * self._systemScale)
			flag = True
		if self._systemScaleChanged:
			flag = True
		return flag
	
	def uiScaleChanged(self) -> bool:
		return self._uiScaleChanged
	
	def systemScaleChanged(self) -> bool:
		return self._systemScaleChanged
	
	def mapScaleChanged(self) -> bool:
		return self._mapScaleChanged

	def dealScaleChange(self) -> None:
		"""
		应当仅在main.py, renderThread中调用
		:return:
		"""
		self._uiScaleChanged = False
		self._systemScaleChanged = False
		self._mapScaleChanged = False
	
	def mapScaleSurface(self, s: Surface, size_x: int | float | None = None, size_y: int | float | None = None) -> Surface:
		"""
		应用地图缩放
		:param s: 要缩放的surface
		:param size_x: 原图x，置None默认16
		:param size_y: 原图y，置None默认16
		:return: 缩放后的表面
		"""
		return pygame.transform.scale_by(s, self._mapScale / 16)
	
	def uiScaleSurface(self, s: Surface, off: float) -> Surface:
		return pygame.transform.scale_by(s, self._uiScale * off)
	
	def systemScaleSurface(self, s: Surface, off: float) -> Surface:
		return pygame.transform.scale_by(s, self._systemScale * off)
	
	def readConfig(self, config: dict[str, any]) -> None:
		self.is4to3.set(configs.readElseDefault(config, "screenSize", False, {"4:3": True, "16:9": False}, "screenSize: {} is not supported. Using 4:3."))
		self.is4to3.apply(self.is4to3.getNew())
		self.setCustomMapScale(configs.readElseDefault(config, "customScale", 1, lambda f: utils.frange(f, 0.8, 5)))
		self.displayFPS = configs.readElseDefault(config, "displayFPS", False, {True: True, False: False}, "displayFPS: {} is not supported. Using false.")
		self.displayTPS = configs.readElseDefault(config, "displayTPS", False, {True: True, False: False}, "displayTPS: {} is not supported. Using false.")
		self.lockScroll = configs.readElseDefault(config, "lockScroll", False, {True: True, False: False}, "lockScroll: {} is not supported. Using false.")
		
	def writeConfig(self) -> dict[str, any]:
		return {
			"screenSize": "4:3" if self.is4to3.get() else "16:9",
			"customScale": self._customMapScale,
			"displayFPS": self.displayFPS,
			"displayTPS": self.displayTPS,
			"lockScroll": self.lockScroll
		}


renderer: Renderer = Renderer()
