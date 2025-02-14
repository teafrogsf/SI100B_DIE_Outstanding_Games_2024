import random
from typing import Union, TYPE_CHECKING

import pygame

from block.manager import blockManager
from entity.manager import entityManager
from interact.interacts import interact
from render.renderer import renderer
from save.save import Archive
from utils.util import utils
from utils.game import game
from utils.text import RenderableString

if TYPE_CHECKING:
	from entity.entity import Entity, Player

from render.renderable import Renderable
from utils.vector import Vector, BlockVector
from block.block import Block, BrickWallBlock, BrickGroundBlock, GateBlock


class World(Renderable):
	def __init__(self, worldID: int, name: str, seed: int | None = None):
		super().__init__(None)
		self._name: str = name
		self._player: Union['Player', None] = None
		self._id: int = worldID
		self._entityList: set['Entity'] = set['Entity']()
		self._ground: dict[int, Block] = dict[int, Block]()
		self._seed: random.Random = random.Random(seed or 0)
		self._seedNumber: int = seed or 0
		self.maxUuid: int = 0
		self.ending: bool = False
	
	def clearUuid(self):
		self.maxUuid = 0
	
	def newUuid(self) -> int:
		self.maxUuid += 1
		return self.maxUuid - 1
	
	@staticmethod
	def generateDefaultWorld(seed: int | None = None) -> 'World':
		w: World = World(-1, "__DEFAULT_WORLD__")
		rd = random.Random(seed or 0)
		for i in range(-10, 10):
			for j in range(-10, 10):
				v = BlockVector(i, j)
				w._ground[hash(v)] = blockManager.dic[rd.sample(blockManager.dic.keys(), 1)[0]](v)
		w.addEntity(entityManager.get('enemy.dog')())
		return w
	
	def tick(self) -> None:
		for e in self._entityList.copy():
			e.passTick()
		for b in self._ground.values():
			if b is None:
				continue
			b.passTick()
		if self._player is not None:
			self._player.passTick()
		if game.getWindow() is None:
			if interact.keys[pygame.K_ESCAPE].deals():
				from window.window import PauseWindow
				game.setWindow(PauseWindow())
			if interact.keys[pygame.K_TAB].deals():
				from window.ingame import TaskWindow
				game.setWindow(TaskWindow())
			if interact.keys[pygame.K_SPACE].deals():
				if renderer.getCameraAt() is None:
					renderer.cameraAt(self.getPlayer())
					game.hud.sendMessage(RenderableString('\\#cc66ccee视角锁定'))
				elif renderer.cameraOffset.lengthManhattan() == 0:
					game.hud.sendMessage(RenderableString('\\#cc00cc00视角解锁'))
					renderer.cameraAt(None)
				else:
					game.hud.sendMessage(RenderableString('\\#cc7755ee居中锁定'))
					renderer.cameraOffset.set(0, 0)
	
	def render(self, delta: float) -> None:
		ct = renderer.getCenter().getVector().divide(renderer.getMapScale())
		block2 = ct.clone().add(renderer.getCamera().get()).getBlockVector().add(1, 1)
		block1 = ct.reverse().add(renderer.getCamera().get()).getBlockVector()
		newList = []
		y2 = block2.y + 2
		for e in iter(self._entityList.copy()):
			p = e.getPosition()
			if p.x < block1.x or p.x > block2.x or p.y < block1.y or p.y > y2:
				continue
			if renderer.getCameraAt() is not e:
				e.updatePosition(delta)
			newList.append(e)
		p = self._player.getPosition()
		if renderer.getCameraAt() is not self._player:
			self._player.updatePosition(delta)
		if block1.x <= p.x <= block2.x and block1.y <= p.y <= y2:
			newList.append(self._player)
		newList.sort(key=lambda k: k.updatePosition().y)
		newListLength = len(newList)
		e = 0
		j = block1.y
		while j <= block2.y:
			i = block1.x
			while i <= block2.x:
				b = self._ground.get(hash(BlockVector(i, j)))
				if b is None:
					i += 1
					continue
				b.render(delta)
				i += 1
			j += 1
			while e < newListLength:
				if newList[e].updatePosition().y <= j:
					newList[e].render(delta)
					e += 1
				else:
					break
		self._player.renderSkill(delta)
	
	def setPlayer(self, player: 'Player') -> None:
		self._player = player
		if player is not None:
			renderer.cameraAt(player)
	
	def getPlayer(self) -> Union['Player', None]:
		return self._player
	
	def addEntity(self, entity: 'Entity') -> None:
		self._entityList.add(entity)
		if entity.uuid == -1:
			entity.uuid = self.newUuid()
		else:
			utils.warn(f"entity的uuid为{entity.uuid}，期待值-1")
	
	def removeEntity(self, entity: 'Entity') -> None:
		self._entityList.remove(entity)
	
	def getEntities(self) -> list['Entity']:
		return list(self._entityList)
	
	def getBlockAt(self, point: Vector | BlockVector) -> Block | None:
		return self._ground.get(hash(point if isinstance(point, BlockVector) else point.clone().getBlockVector()))
	
	def setBlockAt(self, point: BlockVector, block: Block) -> None:
		"""
		设置方块
		"""
		# b = self._ground[hash(point)]
		self._ground[hash(point)] = block
	
	def getRandom(self) -> random.Random:
		return self._seed
	
	def getID(self) -> int:
		return self._id
	
	def rayTraceBlock(self, start: Vector, direction: Vector, length: float, width: float = 0) -> list[tuple[Block | BlockVector, Vector]]:
		"""
		平面上查找某一起点、射线、长度范围内的所有方块
		:param start: 起始点
		:param direction: 射线方向
		:param length: 追踪长度
		:param width: 循迹宽度，默认0
		:return: 元组列表，距离小到大排序。如果方块为None，则第一个参数为方块向量，否则为方块；第二个参数是起始点方向向的命中点（没有宽度偏移）
		"""
		if utils.fequal(direction.x, 0) and utils.fequal(direction.y, 0):
			return []
		result: list[tuple[Block | BlockVector, Vector]] = []
		dcb: BlockVector = direction.directionalCloneBlock()
		if dcb.x == 0 and start.xInteger():
			dcb.x = 1
		if dcb.y == 0 and start.yInteger():
			dcb.y = 1
		directionFix: Vector = direction.directionalClone().multiply(width + 1)
		checkEnd: BlockVector = start.clone().add(direction.clone().normalize().multiply(length)).add(directionFix).getBlockVector()
		checkStart: BlockVector = start.clone().subtract(directionFix).getBlockVector()
		for i in [checkStart.x] if dcb.x == 0 else range(checkStart.x - dcb.x, checkEnd.x + dcb.x, dcb.x):
			for j in [checkStart.y] if dcb.y == 0 else range(checkStart.y - dcb.y, checkEnd.y + dcb.y, dcb.y):
				if i == 3 and j == -3:
					pass
				blockPos: BlockVector = BlockVector(i, j)
				hitResult: Vector | None = blockPos.getHitPoint(start, direction)
				if hitResult is not None and hitResult.length() < length:
					result.append((self._ground[hash(blockPos)] if hash(blockPos) in self._ground.keys() else blockPos.clone(), hitResult.clone()))
		return result
	
	def save(self) -> None:
		archive: Archive = Archive(self._name)
		w = archive.dic['world'] = {}
		e = archive.dic['entity'] = []
		archive.dic['name'] = self._name
		archive.dic['id'] = self._id
		archive.dic['player'] = self._player.save()
		archive.dic['maxUuid'] = self.maxUuid
		archive.dic['ending'] = self.ending
		archive.dic['seed_num'] = self._seedNumber
		for p, b in self._ground.items():
			w[p] = b.save()
		for f in self._entityList:
			e.append(f.save())
		utils.info(archive.dic['id'])
		archive.write()
		archive.close()
	
	@classmethod
	def load(cls, d: dict) -> 'World':
		utils.info('id' in d)
		world = cls(d['id'], d['name'])
		world._player = entityManager.get('player').load(d['player'])
		world.maxUuid = d['maxUuid'] if 'maxUuid' in d else 0
		world.ending = d['ending'] if 'ending' in d else False
		world._seedNumber = d['seed_num'] if 'seed_num' in d else 0
		world._seed.seed(world._seedNumber)
		for i in (dictWorld := d['world']):
			dictBlock = dictWorld[i]
			block = blockManager.get(dictBlock['id']).load(dictBlock)
			world._ground[hash(block.getBlockPosition())] = block
		from entity.entity import Rooster
		from entity.enemy import EnemyChicken
		roosters = []
		for e in d['entity']:
			world._entityList.add(e := entityManager.get(e['id']).load(e))
			if isinstance(e, Rooster):
				roosters.append(e)
		for e in roosters:
			if not isinstance(e.couple, int):
				e.couple = None
				e.description.d[0] = RenderableString("\\#ff4488ee单身\\r的\\#ff4488ee公鸡")
				continue
			for i in world._entityList:
				if i.uuid != e.couple:
					continue
				if not isinstance(i, EnemyChicken):
					utils.warn(f'{i.uuid}对应的类型不是母鸡。存档可能损坏')
					e.couple = None
				e.couple = i
				e.center = i.center
				utils.info(f'{e.couple.uuid}配对成功')
				break
			else:
				utils.warn(f'{e.couple}配对失败。存档可能损坏')
		if world._player.selectingRooster != -1:
			for e in roosters:
				if e.uuid == world._player.selectingRooster:
					e.selected = True
					world._player.selectingRooster = e
					e.description.d[0] = RenderableString("\\#ffeeee00你\\r的\\#ff4488ee公鸡")
				else:
					e.selected = False
		return world
	
	def __str__(self) -> str:
		return f'World(blocks = {len(self._ground)}, {self._ground})'


def generateRandom(seed_or_random=None) -> random.Random:
	if seed_or_random is None:
		r = random.Random()
	elif isinstance(seed_or_random, random.Random):
		r = seed_or_random
	else:
		r = random.Random(seed_or_random)
	return r


class DynamicWorld(World):
	def __init__(self, name: str, seed: int | None = None):
		super().__init__(0, name, seed)
		self.generate_map()  # 初始化地图
		player = entityManager.get('player')(Vector(0, 0))
		self.setPlayer(player)
		game.hud.sendMessage(RenderableString('第一个任务有啦！Tab查看任务吧'))
	
	def generate_map(self) -> None:
		GrassBlock = blockManager.get('nature.grass')
		Fence = blockManager.get('hold.fence')
		SafetyLine = blockManager.get('hold.safety_line')
		PathBlock = blockManager.get('nature.path')
		
		direction = Vector(self._seed.random() - 0.5, self._seed.random() - 0.5)
		while direction.length() < 0.001:
			direction = Vector(self._seed.random() - 0.5, self._seed.random() - 0.5)
		direction.normalize()
		direction2 = Vector(self._seed.random() - 0.5, self._seed.random() - 0.5)
		while direction2.length() < 0.001 or abs(direction2.normalize().dot(direction)) > 0.4:
			direction2 = Vector(self._seed.random() - 0.5, self._seed.random() - 0.5)
		direction2.normalize()
		# 第一段生成
		length1 = self._seed.random() * 10 + 30
		length2 = self._seed.random() * 10 + 15
		ref = direction * length1
		ref2 = ref * 0.75 + direction2 * length2
		center2 = (ref2 + direction2 * (length2 * 0.4)).getBlockVector()
		for i in range(-4, 4):
			flag = (i == 3 or i == -4)
			for j in range(-4, 4):
				pos = BlockVector(i, j)
				self._ground[hash(pos)] = (block := GrassBlock(pos))
				if flag or j == -4 or j == 3:
					block.holdAppend(Fence(pos) if pos.normalizeClone().subtract(direction).length() > 0.4 else SafetyLine(pos))
		for i in range(-10, 10):
			flag = (i == -10 or i == 9)
			for j in range(-7, 8):
				pos = BlockVector(center2.x + i, center2.y + j)
				self._ground[hash(pos)] = (block := GrassBlock(pos))
				if flag or j == -7 or j == 7:
					block.holdAppend(Fence(pos) if (center2 - pos).normalizeClone().subtract(direction2).length() > 0.4 else SafetyLine(pos))
				else:
					while self._seed.random() < 0.15:
						self.addEntity(entityManager.get('entity.stick')(pos.getVector().add(self._seed.random(), self._seed.random())))
		blocks = self.rayTraceBlock(Vector(0, 0), direction, length1)
		blocks2 = self.rayTraceBlock(ref * 0.75, direction2, length2)
		for i in blocks:
			if isinstance(i[0], BlockVector):
				self.setBlockAt(i[0], (PathBlock if self._seed.random() < 0.8 else GrassBlock)(i[0]))
		for i in blocks2:
			if isinstance(i[0], BlockVector):
				self.setBlockAt(i[0], (PathBlock if self._seed.random() < 0.8 else GrassBlock)(i[0]))
		
		def generateBlock(p, rate):
			if rate < 0.4:
				return
			self.setBlockAt(p, (GrassBlock if rate < 0.5 or self._seed.random() > rate else PathBlock)(p))
			if self.getBlockAt(b := BlockVector(p.x - 1, p.y - 1)) is None:
				generateBlock(b, rate - 0.1)
			if self.getBlockAt(b := BlockVector(p.x - 1, p.y)) is None:
				generateBlock(b, rate - 0.1)
			if self.getBlockAt(b := BlockVector(p.x - 1, p.y + 1)) is None:
				generateBlock(b, rate - 0.1)
			if self.getBlockAt(b := BlockVector(p.x, p.y - 1)) is None:
				generateBlock(b, rate - 0.1)
			if self.getBlockAt(b := BlockVector(p.x, p.y + 1)) is None:
				generateBlock(b, rate - 0.1)
			if self.getBlockAt(b := BlockVector(p.x + 1, p.y - 1)) is None:
				generateBlock(b, rate - 0.1)
			if self.getBlockAt(b := BlockVector(p.x + 1, p.y)) is None:
				generateBlock(b, rate - 0.1)
			if self.getBlockAt(b := BlockVector(p.x + 1, p.y + 1)) is None:
				generateBlock(b, rate - 0.1)
		
		for i in blocks + blocks2:
			if not isinstance(i[0], BlockVector):
				continue
			pos = i[0]
			if self.getBlockAt(BlockVector(pos.x - 1, pos.y - 1)) is None:
				generateBlock(pos, 0.7)
			if self.getBlockAt(BlockVector(pos.x - 1, pos.y)) is None:
				generateBlock(pos, 0.7)
			if self.getBlockAt(BlockVector(pos.x - 1, pos.y + 1)) is None:
				generateBlock(pos, 0.7)
			if self.getBlockAt(BlockVector(pos.x, pos.y - 1)) is None:
				generateBlock(pos, 0.7)
			if self.getBlockAt(BlockVector(pos.x, pos.y + 1)) is None:
				generateBlock(pos, 0.7)
			if self.getBlockAt(BlockVector(pos.x + 1, pos.y - 1)) is None:
				generateBlock(pos, 0.7)
			if self.getBlockAt(BlockVector(pos.x + 1, pos.y)) is None:
				generateBlock(pos, 0.7)
			if self.getBlockAt(BlockVector(pos.x + 1, pos.y + 1)) is None:
				generateBlock(pos, 0.7)
		
		# 第二段生成
		def generateTower(p: BlockVector, rate: float):
			for vec in [
				BlockVector(p.x - 1, p.y - 1),
				BlockVector(p.x - 1, p.y),
				BlockVector(p.x - 1, p.y + 1),
				BlockVector(p.x, p.y - 1),
				BlockVector(p.x, p.y + 1),
				BlockVector(p.x + 1, p.y - 1),
				BlockVector(p.x + 1, p.y),
				BlockVector(p.x + 1, p.y + 1),
			]:
				blk = self.getBlockAt(vec)
				if blk is None or isinstance(blk, BrickWallBlock):
					if self._seed.random() < rate:
						self.setBlockAt(vec, BrickGroundBlock(vec))
						generateTower(vec, rate - 0.07)
					elif blk is None:
						self.setBlockAt(vec, BrickWallBlock(vec))
				if blk is not None and blk._blockID.startswith('nature'):
					if self._seed.random() < rate:
						self.setBlockAt(vec, BrickGroundBlock(vec))
						generateTower(vec, rate - 0.07)
		
		self.setBlockAt(pos := ref.clone().multiply(1.2).getBlockVector(), BrickGroundBlock(pos))
		generateTower(pos, 1)
		
		# 第一段实体
		for j in self._ground.values():
			if j is None:
				continue
			if isinstance(j, BrickGroundBlock):
				p = j.getBlockPosition()
				for vec in [
					BlockVector(p.x - 1, p.y - 1),
					BlockVector(p.x - 1, p.y),
					BlockVector(p.x - 1, p.y + 1),
					BlockVector(p.x, p.y - 1),
					BlockVector(p.x, p.y + 1),
					BlockVector(p.x + 1, p.y - 1),
					BlockVector(p.x + 1, p.y),
					BlockVector(p.x + 1, p.y + 1),
				]:
					blk = self._ground.get(hash(vec))
					if blk is not None and blk._blockID.startswith('nature'):
						if self.getBlockAt(p).tryHold(fence := SafetyLine(p)):
							self.getBlockAt(p).holdAppend(fence)
			if not j.canPass():
				continue
			if abs(j.getBlockPosition().x) < 5 and abs(j.getBlockPosition().y) < 5:
				continue
			if isinstance(j, BrickGroundBlock):
				while self._seed.random() < 0.4:
					self.addEntity(entityManager.get('entity.rice')(Vector(self._seed.random() + j.getBlockPosition().x, self._seed.random() + j.getBlockPosition().y)))
				while self._seed.random() < 0.15:
					self.addEntity(entityManager.get('enemy.dog')(Vector(self._seed.random() + j.getBlockPosition().x, self._seed.random() + j.getBlockPosition().y)))
			else:
				if self._seed.random() < 0.05:
					self.addEntity(entityManager.get('entity.rice')(Vector(self._seed.random() + j.getBlockPosition().x, self._seed.random() + j.getBlockPosition().y)))
				if self._seed.random() < 0.05:
					self.addEntity(entityManager.get('entity.stick')(Vector(self._seed.random() + j.getBlockPosition().x, self._seed.random() + j.getBlockPosition().y)))
		
		# 第二段实体
		for i in range(12):
			self.addEntity(hen := entityManager.get('enemy.hen')(pos := Vector(center2.x + self._seed.random() * 18 - 9, center2.y + self._seed.random() * 13 - 6)))
			self.addEntity(entityManager.get('entity.coop')(pos))
			self.addEntity(entityManager.get('entity.rooster')(pos, hen))
		
		while True:
			for j in self._ground.values():
				if j is None:
					continue
				if not isinstance(j, BrickGroundBlock):
					continue
				if self._seed.random() < 0.01:
					gate: GateBlock = blockManager.get('hold.door')(j.getBlockPosition())
					if j.tryHold(gate):
						j.holdAppend(gate)
						break
			else:
				continue
			break


class WitchWorld(World):
	def __init__(self):
		super().__init__(1, '老巫鸡的密室', None)
		self.generate_map()  # 初始化地图
		game.hud.sendMessage(RenderableString('\\#ffeeee00\\.ffee6666欢迎来到异世界'))
		game.hud.sendMessage(RenderableString('\\#ffeeee00\\.ffee6666每条路的尽头都有一个老巫鸡'))
		game.hud.sendMessage(RenderableString('\\#ffeeee00\\.ffee6666希望你能找到线索，并找到真正的老巫鸡'))
	
	def generate_map(self) -> None:
		for i in range(-20, 20):
			for j in range(-1, 1):
				v = BlockVector(i, j)
				block = blockManager.dic.get('witch.blue')(v)
				self._ground[hash(v)] = block
		for i in range(-1, 1):
			for j in range(-20, 20):
				v = BlockVector(i, j)
				block = blockManager.dic.get('witch.blue')(v)
				self._ground[hash(v)] = block
		
		player = entityManager.get('player')(Vector(1, 1))
		self.setPlayer(player)
		dog_position = [Vector(-4, 0), Vector(0, 4), Vector(0, -4), Vector(4, 0), Vector(1, 1), Vector(-1, -1)]
		
		for i in range(6):
			self.addEntity(entityManager.get('enemy.dog')(dog_position[i]))
		
		self.addEntity(entityManager.get('entity.witch')(Vector(0, 16)))
		
		witch_position = [Vector(-16, 0), Vector(16, 0), Vector(0, -16)]
		for j in range(1, 4):
			self.addEntity(entityManager.get(f'entity.fakewitch{j}')(witch_position[j - 1], i=j))
		
		clue_position = [Vector(-19, 0), Vector(0, 19), Vector(0, -19), Vector(19, 0)]
		for j in range(0, 4):
			self.addEntity(entityManager.get(f'entity.clue{j}')(clue_position[j], i=j))
