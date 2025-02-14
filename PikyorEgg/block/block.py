from typing import TYPE_CHECKING, Union

from block.manager import blockManager
from entity.manager import entityManager
from render.resource import resourceManager
from utils.element import Element
from utils.game import game
from utils.error import InvalidOperationException, neverCall
from utils.text import RenderableString, BlockDescription, Description
from utils.vector import Vector, BlockVector
from music.music import Music_player

if TYPE_CHECKING:
	from entity.entity import Entity
	from render.resource import Texture


class Block(Element):
	def __init__(self, blockID: str, name: str, description: 'BlockDescription', position: 'BlockVector', texture: 'Texture'):
		super().__init__(name, description, texture)
		self._position: 'BlockVector' = position.clone()
		self._blockID: str = blockID
		self._holding: list[Element] = []
	
	def tick(self) -> None:
		pass
	
	def passTick(self) -> None:
		self.tick()
		if len(self._holding) > 0:
			for h in self._holding:
				h.passTick()
	
	def render(self, delta: float) -> None:
		self.getTexture().renderAsBlock(self._position)
		if len(self._holding) > 0:
			for h in self._holding:
				h.passRender(delta)
	
	def canPass(self, entity: Union['Entity', None] = None) -> bool:
		"""
		必须重写。标志当前挡块是否允许特定实体通过
		:param entity: 要检测的实体
		"""
		neverCall(f"{type(self)}.canPass未重写")
		return True
	
	def getPosition(self) -> 'Vector':
		return self._position.getVector()
	
	def getBlockPosition(self) -> 'BlockVector':
		return self._position.clone()
	
	def getDescription(self) -> list[Description]:
		return [self.description] + [b.description for b in self._holding]
	
	def tryHold(self, block: Element) -> bool:
		"""
		可重写。尝试让该方块叠加一个新的元素
		:param block: 要叠加的元素
		:return: True - 能, False - 否
		"""
		return False
	
	def holdAppend(self, element: Element) -> None:
		"""
		可重写。强行叠加一个元素。失败的时候可能会直接抛错
		:param element: 要叠加的元素
		"""
		if not self.tryHold(element):
			raise InvalidOperationException("无法叠加元素")
		self._holding.append(element)
	
	def getHolding(self) -> list[Element]:
		"""
		获取当前方块上叠加的元素
		"""
		return self._holding
	
	def holdRemove(self, element: Element) -> bool:
		"""
		删除一个叠加的方块
		:param element: 对象本身
		:return: 是否成功删除了方块
		"""
		if self._holding.__contains__(element):
			self._holding.remove(element)
			return True
		else:
			return False
	
	def save(self) -> dict:
		return {
			'position': {
				'x': self._position.x,
				'y': self._position.y
			},
			'id': self._blockID,
			'holding': [b.save() for b in self._holding]
		}
	
	@classmethod
	def load(cls, d: dict, block: Union['Block', None] = None) -> 'Block':
		"""
		可以用来加载最基本的方块内容，主要是叠加方块
		:param d: 方块字典
		:param block: 默认None，用于识别手动或自动调用。手动调用必须传入方块
		"""
		if block is None:
			raise InvalidOperationException(f"Block类不应被直接加载：ID {d['id']}")
		block._holding = [blockManager.get(b['id']).load(b) for b in d['holding']]
		return block
	
	def __str__(self):
		return f"{type(self).__name__}({self.name})"
	
	def __repr__(self):
		return self.__str__()


class Ground(Block):
	"""
	类地面方块
	"""
	
	def __init__(self, blockID: str, name: str, description: 'BlockDescription', position: 'BlockVector', texture: 'Texture'):
		super().__init__(blockID, name, description, position, texture)
	
	def tryHold(self, block: Element) -> bool:
		if len(self._holding) < 1:
			if isinstance(block, Block) and block._blockID.startswith('hold.'):
				return True
		return False
	
	def canPass(self, entity: Union['Entity', None] = None) -> bool:
		if len(self._holding) == 0:
			return True
		for h in self._holding:
			if not h.canPass(entity):
				return False
		return True


class Wall(Block):
	"""
	类墙方块
	"""
	
	def __init__(self, blockID: str, name: str, description: 'BlockDescription', position: 'BlockVector', texture: 'Texture'):
		super().__init__(blockID, name, description, position, texture)
	
	def canPass(self, entity: Union['Entity', None] = None) -> bool:
		return False


class GrassBlock(Ground):
	def __init__(self, position: 'BlockVector'):
		super().__init__('nature.grass', "草地", BlockDescription(self, [RenderableString("\\#FF4BAB25青色的草地")]), position, resourceManager.getOrNew('block/grass'))
	
	def tick(self) -> None:
		if self.canPass():
			rd = game.getWorld().getRandom()
			if len(game.getWorld().getEntities()) <= 300 and rd.random() < 0.00001 * (300 - len(game.getWorld().getEntities())):
				game.getWorld().addEntity(entityManager.get(rd.choice(['entity.stick', 'entity.rice']))(Vector(rd.random() + self._position.x, rd.random() + self._position.y)))
	
	@classmethod
	def load(cls, d: dict, block=None) -> 'GrassBlock':
		ret = GrassBlock(BlockVector.load(d['position']))
		super().load(d, ret)
		return ret


class PathBlock(Ground):
	def __init__(self, position: 'BlockVector'):
		super().__init__('nature.path', "草径", BlockDescription(self, [RenderableString("\\#FF4BAB25土黄色的道路")]), position, resourceManager.getOrNew('block/path'))
	
	@classmethod
	def load(cls, d: dict, block=None) -> 'PathBlock':
		ret = PathBlock(BlockVector.load(d['position']))
		super().load(d, ret)
		return ret


class FarmlandBlock(Ground):
	def __init__(self, position: 'BlockVector'):
		super().__init__('nature.farmland', "耕地", BlockDescription(self, [RenderableString("\\#FF733706肥沃的泥土")]), position, resourceManager.getOrNew('block/farmland'))
	
	@classmethod
	def load(cls, d: dict, block=None) -> 'FarmlandBlock':
		ret = FarmlandBlock(BlockVector.load(d['position']))
		super().load(d, ret)
		return ret


class ErrorBlock(Ground):
	def __init__(self, position: 'BlockVector'):
		super().__init__('system.error', "错误方块", BlockDescription(self, [RenderableString("\\#FFEE0000错误方块")]), position, resourceManager.getOrNew('no_texture'))
	
	@classmethod
	def load(cls, d: dict, block=None) -> 'ErrorBlock':
		ret = ErrorBlock(BlockVector.load(d['position']))
		super().load(d, ret)
		return ret


class Fence(Wall):
	def __init__(self, position: BlockVector):
		super().__init__('hold.fence', '栅栏', BlockDescription(self, [RenderableString('栅栏'), RenderableString('\\/    家的感觉，家的舒适，家的安全')]), position, resourceManager.getOrNew('block/fence'))
	
	@classmethod
	def load(cls, d: dict, block=None) -> 'Block':
		block = Fence(BlockVector.load(d['position']))
		return super().load(d, block)


class SafetyLine(Wall):
	def __init__(self, position: BlockVector):
		super().__init__('hold.safety_line', '栅栏', BlockDescription(self, [RenderableString('栅栏'), RenderableString('  \\/    关门，关狗！')]), position, resourceManager.getOrNew('block/safety_line'))
	
	def canPass(self, entity: Union['Entity', None] = None) -> bool:
		from entity.entity import Player, Rooster
		if isinstance(entity, Player) or isinstance(entity, Rooster):
			return True
		return False
	
	@classmethod
	def load(cls, d: dict, block=None) -> 'Block':
		block = SafetyLine(BlockVector.load(d['position']))
		return super().load(d, block)


class WitchBlock(Ground):
	def __init__(self, position: BlockVector):
		super().__init__('witch.blue', "巫婆世界方块", BlockDescription(self, [RenderableString("\\#FFEE0000巫婆世界方块")]), position, resourceManager.getOrNew('block/witch'))
	
	@classmethod
	def load(cls, d: dict, block=None) -> 'WitchBlock':
		ret = WitchBlock(BlockVector.load(d['position']))
		super().load(d, ret)
		return ret


gateBlockTimer: int = 60


class GateBlock(Ground):
	def __init__(self, position: BlockVector):
		class Des(BlockDescription):
			def __init__(this, block):
				super().__init__(block)
				this.colors = [
					'\\#FFEE0000', '\\#FFEE5500', '\\#FFEEAA00',
					'\\#FFEEEE00', '\\#FFAAEE00', '\\#FF55EE00',
					'\\#FF00EE00', '\\#FF00EE55', '\\#FF00EEAA',
					'\\#FF00EEEE', '\\#FF00AAEE', '\\#FF0055EE',
					'\\#FF0000EE', '\\#FF5500EE', '\\#FFAA00EE',
					'\\#FFEE00EE', '\\#FFEE00AA', '\\#FFEE0055',
				]
				this.color = -1
			
			def generate(this) -> list['RenderableString']:
				if this.color >= 10:
					this.color = -7
				else:
					this.color += 1
				return [RenderableString('\\#ffaa4499' + this._block.getBlockPosition().getTuple().__str__())] + [RenderableString(this.colors[this.color] + '传' + this.colors[this.color - 1] + '送' + this.colors[this.color - 2] + '门'), RenderableString(f'\\#FFEE0000    停留{gateBlockTimer / 20:.2f}秒前往巫婆鸡的异世界')]
		
		super().__init__('hold.door', '传送门', Des(self), position, resourceManager.getOrNew('block/gate'))
	
	@classmethod
	def load(cls, d: dict, block=None) -> 'Block':
		block = GateBlock(BlockVector.load(d['position']))
		return super().load(d, block)
	
	def tick(self) -> None:
		player = game.getWorld().getPlayer()
		global gateBlockTimer
		if player.getVelocity().lengthManhattan() != 0:
			gateBlockTimer = 60
		elif player is not None and self._position.contains(player.getPosition()):
			gateBlockTimer -= 1
			if gateBlockTimer == 0:
				Music_player.sound_play(2)
				from world.world import WitchWorld
				world = WitchWorld()
				world.setPlayer(player)
				player.setPosition(Vector())
				game.setWorld(world)


class BrickGroundBlock(Ground):
	def __init__(self, position: BlockVector):
		super().__init__('struct.brick', "砖块", BlockDescription(self, [RenderableString("\\#FFBABABA砖块")]), position, resourceManager.getOrNew('block/brick'))
	
	def tick(self) -> None:
		if self.canPass():
			rd = game.getWorld().getRandom()
			if len(game.getWorld().getEntities()) > 300:
				return
			if rd.random() < 0.00001 * (300 - len(game.getWorld().getEntities())):
				game.getWorld().addEntity(entityManager.get('enemy.dog')(Vector(rd.random() + self._position.x, rd.random() + self._position.y)))
			if rd.random() < 0.0001 * (300 - len(game.getWorld().getEntities())):
				game.getWorld().addEntity(entityManager.get('entity.rice')(Vector(rd.random() + self._position.x, rd.random() + self._position.y)))
	
	@classmethod
	def load(cls, d: dict, block=None) -> 'BrickGroundBlock':
		ret = BrickGroundBlock(BlockVector.load(d['position']))
		super().load(d, ret)
		return ret


class BrickWallBlock(Wall):
	def __init__(self, position: BlockVector):
		super().__init__('struct.brick_wall', "砖墙", BlockDescription(self, [RenderableString("\\#FFBABABA砖墙")]), position, resourceManager.getOrNew('block/brick_wall'))
	
	@classmethod
	def load(cls, d: dict, block=None) -> 'BrickWallBlock':
		ret = BrickWallBlock(BlockVector.load(d['position']))
		super().load(d, ret)
		return ret


blockManager.register('nature.grass', GrassBlock)
blockManager.register('nature.path', PathBlock)
blockManager.register('nature.farmland', FarmlandBlock)
blockManager.register('system.error', ErrorBlock)
blockManager.register('hold.fence', Fence)
blockManager.register('hold.safety_line', SafetyLine)
blockManager.register('hold.door', GateBlock)
blockManager.register('witch.blue', WitchBlock)
blockManager.register('struct.brick', BrickGroundBlock)
blockManager.register('struct.brick_wall', BrickWallBlock)

for t in [
	resourceManager.getOrNew('block/fence')
]:
	t.getSurface().set_colorkey((0, 0, 0))
	t.getMapScaledSurface().set_colorkey((0, 0, 0))
	t.setOffset(Vector(0, -8))
for t in [
	resourceManager.getOrNew('block/safety_line'),
	resourceManager.getOrNew('block/gate')
]:
	t.getSurface().set_colorkey((0, 0, 0))
	t.getMapScaledSurface().set_colorkey((0, 0, 0))
del t
