from render.renderable import Renderable
from render.resource import Texture
from utils.text import Description


class Element(Renderable):
	def __init__(self, name: str, description: Description, texture: Texture):
		super().__init__(texture)
		self.name = name
		self.description = description
	
	def save(self) -> dict:
		pass
	
	@classmethod
	def load(cls, d: dict) -> 'Element':
		pass
