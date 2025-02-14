from threading import Lock

import pygame.image
from pygame import Surface
from utils.vector import Vector, BlockVector
from render.renderer import renderer
from utils.util import utils


# 锁定窗口比例，要么4:3，要么16:9。主要按高度分配


class Texture:
	"""
	注意，资源渲染的计算方式不同。如果是基于地图渲染，请使用renderAtMap，会根据game.camera等自动计算相对位置。Vector给出相对于地图的位置。如果是基于屏幕渲染，例如额外窗口、UI部分，请使用renderAtInterface，会自动适应margin等，并采用Vector给出浮点数的屏幕相对值。
	"""
	
	def __init__(self, file: str):
		self._mapObject: bool = True
		self._uiObject: bool = False
		self._systemObject: bool = False
		self._file = open(f'assets/texture/{file}.bmp', 'rb')
		self._surface: Surface = pygame.image.load_basic(self._file)
		self.systemScaleOffset: float = 0.0252
		self.uiScaleOffset: float = 0.0252
		self._mapScaled: Surface | None = renderer.mapScaleSurface(self._surface) if self._mapObject else None
		self._uiScaled: Surface | None = None
		self._systemScaled: Surface | None = None
		self._offset: Vector | None = None
	
	def adaptsMap(self, val: bool = True) -> None:
		if self._mapObject != val:
			self._mapObject = val
			self._mapScaled: Surface | None = renderer.mapScaleSurface(self._surface)
	
	def adaptsUI(self, val: bool = True) -> None:
		if self._uiObject != val:
			self._uiObject = val
			self._uiScaled: Surface | None = renderer.uiScaleSurface(self._surface, self.uiScaleOffset)
	
	def adaptsSystem(self, val: bool = True) -> None:
		if self._systemObject != val:
			self._systemObject = val
			self._systemScaled: Surface | None = renderer.systemScaleSurface(self._surface, self.systemScaleOffset)
	
	def renderAtInterface(self, at: BlockVector = BlockVector()) -> None:
		s = self._uiScaled if self._uiScaled is not None else self._systemScaled if self._systemScaled is not None else self._surface
		renderer.getCanvas().blit(s, at.getTuple())
	
	def renderAsBlock(self, at: BlockVector, fromPos: BlockVector | None = None, fromSize: BlockVector | None = None):
		"""
		相对于地图渲染
		:param at: 地图位置
		:param fromPos: 源图起始点
		:param fromSize: 源图截取大小
		:return:
		"""
		renderer.renderAsBlock(self._mapScaled if self._mapScaled is not None else self._surface, at if self._offset is None else self._offset + at.getVector(), fromPos, fromSize)
	
	def renderAtMap(self, at: Vector, fromPos: Vector | None = None, fromSize: Vector | None = None):
		"""
		相对于地图渲染
		:param at: 地图位置
		:param fromPos: 源图起始点
		:param fromSize: 源图截取大小
		:return:
		"""
		renderer.renderAtMap(self._mapScaled if self._mapScaled is not None else self._surface, at if self._offset is None else at + self._offset, fromPos, fromSize)
	
	def changeMapScale(self) -> None:
		if self._mapObject:
			self._mapScaled = renderer.mapScaleSurface(self._surface)
	
	def changeUiScale(self) -> None:
		if self._uiObject:
			self._uiScaled = renderer.uiScaleSurface(self._surface, self.uiScaleOffset)
	
	def changeSystemScale(self) -> None:
		if self._systemObject:
			self._systemScaled = renderer.systemScaleSurface(self._surface, self.systemScaleOffset)
	
	def getSurface(self) -> Surface:
		"""
		获取pygame的Surface。除非必要，尽可能地不要修改Surface
		"""
		return self._surface
	
	def getMapScaledSurface(self) -> Surface:
		"""
		获取适应过地图缩放的pygame的Surface。除非必要，尽可能地不要修改Surface
		"""
		return self._mapScaled
	
	def getUiScaledSurface(self) -> Surface:
		"""
		获取适应过UI缩放的pygame的Surface。除非必要，尽可能地不要修改Surface
		"""
		return self._uiScaled if self._uiObject else self._systemScaled
	
	def getSystemScaledSurface(self) -> Surface:
		return self._systemScaled
	
	def setOffset(self, offset: Vector | None) -> None:
		"""
		设置偏移。默认情况下会以地图位置为中心渲染（例如位于(0, 0)则会渲染在(-0.8, -0.8, 0.8, 0.8)）
		:param offset: 偏移量
		"""
		self._offset = None if offset is None else (offset / 16)
	
	def getOffset(self) -> Vector:
		return Vector() if self._offset is None else self._offset.clone()


class ResourceManager:
	def __init__(self):
		self._lock: Lock = Lock()
		self._textures: dict[str, Texture] = {}
		try:
			self._textures['no_texture'] = Texture('no_texture')
		except FileNotFoundError:
			raise FileNotFoundError("没有找到默认纹理")
	
	def getOrNew(self, key: str):
		if key in self._textures:
			return self._textures[key]
		try:
			self._lock.acquire()
			resource: Texture = Texture(key)
			self._textures[key] = resource
			resource.changeMapScale()
			self._lock.release()
			return resource
		except FileNotFoundError:
			self._textures[key] = self._textures['no_texture']
			utils.error(f"没有找到纹理{key}，已经用默认纹理替代")
			self._lock.release()
			return self._textures[key]
	
	def get(self, key: str) -> Texture:
		if key not in self._textures:
			raise KeyError(f"资源{key}不存在")
		return self._textures[key]
	
	def has(self, key: str) -> bool:
		return key in self._textures
	
	def register(self, key: str, resource: Texture):
		if key in self._textures:
			raise KeyError(f"资源{key}已存在")
		else:
			self._lock.acquire()
			self._textures[key] = resource
			resource.changeMapScale()
			self._lock.release()
	
	def changeMapScale(self) -> None:
		"""
		仅在main.py, renderThread中调用
		"""
		self._lock.acquire()
		for texture in self._textures.values():
			texture.changeMapScale()
		self._lock.release()
	
	def changeScale(self) -> None:
		"""
		仅在main.py, renderThread中调用
		"""
		self._lock.acquire()
		for texture in self._textures.values():
			if renderer.uiScaleChanged():
				texture.changeUiScale()
			if renderer.systemScaleChanged():
				texture.changeSystemScale()
			if renderer.mapScaleChanged():
				texture.changeMapScale()
		self._lock.release()


resourceManager: ResourceManager = ResourceManager()
