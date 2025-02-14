from utils.util import times
from utils.vector import Vector
from render.resource import Texture


class Renderable:
	"""
	所有能渲染的东西都继承这个类，game.py:class Game除外
	"""
	def __init__(self, texture: Texture | None):
		self._texture: Texture = texture
	
	def render(self, delta: float) -> None:
		"""
		渲染时调用
		:param delta: tick偏移。由于20tick/s但是渲染至少60f/s，每tick至少渲染3次。为了保证一些移动的流畅性，delta用于辅助计算移动部件的位置。delta的值为(timePresent - timeLastTick) / timeEveryTick
		"""
		pass
	
	def passRender(self, delta: float, at: Vector | None = None) -> None:
		"""
		用于内部调用，尽可能地避免重写。重写时必须调用父类方法
		"""
		self.render(delta)
		
	def getTexture(self) -> Texture:
		return self._texture
