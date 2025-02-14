"""
这里相当于游戏资源管理器。所有的游戏资源（列表）都在这里。
"""
import pygame

from interact.interacts import interact
from music.music import Music_player
from render.renderer import renderer
from typing import TYPE_CHECKING, Union

from utils.sync import SynchronizedStorage
from utils.text import RenderableString
from utils.util import utils
from utils.vector import Vector

if TYPE_CHECKING:
	from world.world import World
	from window.window import Window, FloatWindow
	from window.hud import Hud


class Game:
	def __init__(self):
		self._mainWorld: Union['World', None] = None
		self.running: bool = True
		self.tickCount: int = 0
		self._window: SynchronizedStorage[Union['Window', None]] = SynchronizedStorage[Union['Window', None]](None)
		self.floatWindow: Union['FloatWindow', None] = None  # 在主程序中初始化
		self.hud: Union['Hud', None] = None
		self.world: dict[int, 'World'] = {}
		self.mouseAtMap: Vector = Vector()
	
	def tick(self) -> None:
		notPause: bool = True
		if self._window.get() is not None:
			self._window.get().passTick()
			notPause = not self._window.get().pauseGame()
		self._window.apply(self._window.getNew())
		if self._mainWorld is not None and notPause:
			self._mainWorld.tick()
		self.processMouse()
		self.tickCount += 1
	
	def render(self, delta: float) -> None:
		"""
		渲染所有内容。
		"""
		if delta > 1:
			delta = 1
		elif delta < 0:
			delta = 0
		elif self._window.get() is not None and self._window.get().pauseGame():
			delta = 1
		renderer.begin(delta, self._window.get() is None)
		self.mouseAtMap = interact.mouse.clone().subtract(renderer.getCenter()).getVector().divide(renderer.getMapScale()).add(renderer.getCamera().get())  # 由tick触发计算移动至render触发计算
		if self._mainWorld is not None:
			self._mainWorld.passRender(delta)
		self.hud.render(delta)
		if self._window.get() is not None:
			self._window.get().passRender(delta)
		self.floatWindow.render(delta)
		renderer.end()
	
	def setWindow(self, window: Union['Window', None]) -> None:
		interact.scroll.dealScroll()
		interact.keys[pygame.K_ESCAPE].deals()
		self._window.set(window)
		if window is not None:
			window.onResize()
	
	def getWindow(self) -> Union['Window', None]:
		return self._window.getNew()
	
	def setWorld(self, world: Union['World', int, None]) -> None:
		if isinstance(world, int):
			self._mainWorld = self.world[world]
		else:
			self._mainWorld = world
			if world is not None:
				self.world[self._mainWorld.getID()] = world
		if self._mainWorld is None:
			renderer.cameraAt(None)
		else:
			renderer.cameraAt(self._mainWorld.getPlayer())
			Music_player.background_play(self._mainWorld.getID() + 1)
	
	def getWorld(self, worldID: int | None = None) -> Union['World', None]:
		if worldID is not None:
			return self.world[worldID]
		return self._mainWorld
	
	def quit(self) -> None:
		self.running = False
	
	def processMouse(self, event: pygame.event.Event | None = None):
		if self._mainWorld is not None and self._window.get() is None:
			# self.mouseAtMap = interact.mouse.clone().subtract(renderer.getCenter()).getVector().divide(renderer.getMapScale()).add(renderer.getCamera().get())  # 废弃代码段：移动至render触发计算
			target1, target2 = None, None
			targetDist1, targetDist2 = 1, 1
			for e in (self._mainWorld.getEntities() + [self._mainWorld.getPlayer()]):
				if (dist := e.getPosition().add(e.getTexture().getOffset()).distanceManhattan(self.mouseAtMap)) < 0.5 and dist < targetDist2:
					if dist < targetDist1:
						target1, target2 = e, target1
						targetDist1, targetDist2 = dist, targetDist1
					else:
						target2 = e
						targetDist2 = dist
			self.floatWindow.clear()
			if target2 is not None:
				self.floatWindow.submit(target1.description)
				self.floatWindow.submit(target2.description)
			elif target1 is not None:
				self.floatWindow.submit(target1.description)
			block = self._mainWorld.getBlockAt(self.mouseAtMap.getBlockVector())
			if block is not None:
				self.floatWindow.submit(block.getDescription())
			if interact.left.deals():
				if target1 is not None:
					renderer.cameraAt(target1)
					game.hud.sendMessage(RenderableString(f'\\#cc66ccee视角锁定在：{target1.__class__.__name__} (UUID {target1.uuid}))'))
		if event is not None:
			if event.buttons[1] == 1 and self._window.get() is None:
				renderer.cameraOffset.subtract(Vector(event.rel[0], event.rel[1]).divide(renderer.getMapScale()))


game = Game()
