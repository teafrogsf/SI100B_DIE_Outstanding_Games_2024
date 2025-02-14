import random

import pygame
from typing import TYPE_CHECKING, Union, Callable

from entity.active_skill import Active
from entity.manager import entityManager, skillManager
from entity.skill import Skill
from utils.util import utils
from window.window import DeathWindow, EggFactoryWindow

if TYPE_CHECKING:
	from block.block import Block
	from entity.enemy import EnemyChicken

from interact.interacts import interact
from utils.vector import Vector, BlockVector, Matrices
from render.resource import resourceManager
from utils.game import game
from utils.text import RenderableString, EntityDescription
from render.resource import Texture
from utils.element import Element
from music.music import Music_player


class Entity(Element):
	def __init__(self, entityID: str, name: str, description: EntityDescription, texture: list[Texture], position: Vector):
		"""
		:param name: 实体名称
		:param description: 实体描述，字符串列表
		:param texture: 纹理列表，一般认为[0][1]是前面，[2][3]是后，[4][5]是左，[6][7]是右。可以参考class Player的构造函数
		"""
		super().__init__(name, description, texture[0])
		self._position: Vector = position.clone()
		self._textureSet: list[Texture] = texture
		self._id: str = entityID
		self.uuid: int = -1
	
	def passTick(self) -> None:
		"""
		内置函数，不应当额外调用，不应当随意重写。
		重写时必须注意调用父类的同名函数，防止遗漏逻辑。
		除非你一定要覆写当中的代码，否则尽量不要重写这个函数。
		"""
		self.tick()
	
	def tick(self) -> None:
		"""
		交由具体类重写
		"""
		pass
	
	def render(self, delta: float) -> None:
		self._texture.renderAtMap(self._position)
	
	def setPosition(self, position: Vector) -> None:
		self._position.set(position)
	
	def getPosition(self) -> Vector:
		return self._position.clone()
	
	def updatePosition(self, delta: float | None = None) -> Vector:
		return self._position.clone()
	
	def save(self) -> dict:
		return {
			"id": self._id,
			"uuid": self.uuid,
			"position": self._position.save(),
			"name": self.name,
		}
	
	@classmethod
	def load(cls, d: dict, entity: Union['Entity', None] = None) -> Union['Entity', None]:
		"""
		:param d: 加载字典
		:param entity: 默认None，用于区分手动调用和自动调用。手动调用必须传入，理论上不允许自动调用
		:return: 返回entity
		"""
		entity._id = d["id"]
		entity.name = d["name"]
		entity.uuid = d["uuid"] if "uuid" in d else -1
		entity._position = Vector.load(d["position"])
		return entity


class Damageable:
	"""
	所有有血条的实体都要额外继承这个类
	"""
	
	def __init__(self, maxHealth: float = 100, health: float | None = None):
		self._health: float = health or maxHealth
		self._maxHealth: float = maxHealth
		self._isAlive: bool = True
	
	def onDeath(self) -> None:
		"""
		死亡时调用，可重写
		"""
		game.getWorld().removeEntity(self)
	
	def onHeal(self, amount: float) -> float:
		"""
		被治疗时调用，并且在这里实际应用回复。如果已经死亡，则即便恢复了也不会调用这个函数。可重写
		:param amount: 治疗量
		:return: 实际治疗量
		"""
		if amount <= 0:
			return 0
		delta: float = self._maxHealth - self._health
		if amount >= delta:
			self._health = self._maxHealth
			return delta
		else:
			self._health += amount
			return amount
	
	def onDamage(self, amount: float, src: Entity) -> float:
		"""
		被伤害时调用，并且在这里实际应用伤害。如果已经死亡，则即便伤害了也不会调用这个函数。返回时，可以忽略负血量的问题直接返回原始伤害值。可重写
		:param amount: 伤害量
		:param src: 伤害来源
		:return: 实际伤害量
		"""
		if amount < 0:
			return 0
		if amount >= self._health:
			self._health = 0
			self._isAlive = False
			self.onDeath()
			return amount
		else:
			self._health -= amount
			return amount
	
	def setHealth(self, health: float) -> None:
		"""
		设置生命值
		"""
		if health <= 0:
			self._health = 0
			return
		if health >= self._maxHealth:
			self._health = self._maxHealth
			return
		self._health = health
	
	def setMaxHealth(self, maxHealth: float) -> None:
		self._maxHealth = maxHealth
	
	def getHealth(self) -> float:
		return self._health
	
	def getMaxHealth(self) -> float:
		return self._maxHealth
	
	def heal(self, amount: float) -> float:
		"""
		执行治疗
		:param amount: 治疗量
		:return: 实际治疗值
		"""
		if not self._isAlive:
			return 0
		return self.onHeal(amount)
	
	def damage(self, amount: float, src: 'Entity') -> float:
		"""
		执行伤害
		:param amount: 伤害量
		:param src: 伤害来源
		:return: 实际伤害量
		"""
		if not self._isAlive:
			return 0
		return self.onDamage(amount, src)
	
	def save(self) -> dict:
		return {
			"health": self._health,
			"maxHealth": self._maxHealth,
			"isAlive": self._isAlive
		}
	
	@classmethod
	def load(cls, d: dict, entity: Union['Damageable', None]) -> 'Damageable':
		entity._health = d["health"]
		entity._maxHealth = d["maxHealth"]
		entity._isAlive = d["isAlive"]
		return entity


class MoveableEntity(Entity):
	def __init__(self, entityID: str, name: str, description: EntityDescription, texture: list[Texture], position: Vector, speed: float = 0):
		super().__init__(entityID, name, description, texture, position)
		self.__renderInterval: int = 6
		self.__velocity: Vector = Vector(0, 0)
		self._maxSpeed: float = speed
		self._setVelocity: Vector = Vector(0, 0)
		self._renderPosition: Vector = Vector()
		self._textureSet: list[Texture] = texture
		self.basicMaxSpeed: float = speed
		self.modifiedMaxSpeed: float = speed
		self.moveable: int = 0  # 防止多个源同时禁用移动，而其中一个较先解锁导致问题
		self.lastDelta: float = 0
	
	def setVelocity(self, v: Vector) -> None:
		"""
		设置速度
		:param v: 目标值
		"""
		self._setVelocity.set(v)
	
	def getVelocity(self) -> Vector:
		return self.__velocity.clone()
	
	def processMove(self) -> None:
		if self.moveable:
			return
		if (vLength := self._setVelocity.length()) == 0:
			self.__velocity.set(0, 0)
			return
		rayTraceResult: list[tuple[Union['Block', BlockVector], Vector]] = game.getWorld().rayTraceBlock(self._position, self._setVelocity, vLength)
		for block, vector in rayTraceResult:
			block: Union['Block', BlockVector]  # 命中方块，或者命中方块坐标
			vector: Vector  # 起始点->命中点
			if not isinstance(block, BlockVector):
				if block.canPass(self):  # 可通过方块，跳过
					continue
				block = block.getBlockPosition()
			block: BlockVector
			newPosition: Vector = self._position + vector
			newVelocity: Vector = self._setVelocity - vector
			rel: list[tuple[BlockVector, Vector]] | BlockVector | None = block.getRelativeBlock(newPosition, newVelocity)
			if rel is None:  # 在中间
				continue
			elif isinstance(rel, BlockVector):  # 撞边不撞角
				vel2: Vector = (Matrices.xOnly if rel.x == 0 else Matrices.yOnly) @ newVelocity
				for b, v in game.getWorld().rayTraceBlock(newPosition, vel2, vel2.length()):
					if not isinstance(b, BlockVector):
						if b.canPass(self):
							continue
						# 还得判断钻缝的问题
						b = b.getBlockPosition()
					grb = b.getRelativeBlock(newPosition + v, v)
					if not isinstance(grb, list) or len(grb) == 0:
						continue
					b2 = game.getWorld().getBlockAt(grb[0][0])
					if b2 is None or not b2.canPass(self):
						self.__velocity.set(vector + v)
						return
				# 钻缝问题处理结束
				# 退出for循环，说明全部通过
				self.__velocity.set(vector + vel2)
				return
			elif not rel:  # 空列表
				continue  # 不影响移动
			else:  # 撞角
				if len(rel) == 1:  # 碰一边
					relativeBlock: Union['Block', None] = game.getWorld().getBlockAt(rel[0][0])
					if relativeBlock is None or not relativeBlock.canPass(self):  # 碰一边，然后恰好撞墙
						self.__velocity.set(vector)
					else:
						self.__velocity.set(vector + rel[0][1])
					return
				# 碰一边处理结束，顶角处理开始
				# 都能过的话，无脑，0优先。
				# 然后这里好像还要再trace一次新的方向看看
				relativeBlock: Union['Block', None] = game.getWorld().getBlockAt(rel[0][0])
				if relativeBlock is not None and relativeBlock.canPass(self):  # 0能过，trace新方向
					for b, v in game.getWorld().rayTraceBlock(newPosition, rel[0][1], rel[0][1].length()):
						if not isinstance(b, BlockVector):
							if b.canPass(self):
								continue
							# 还得判断钻缝的问题
							b = b.getBlockPosition()
						grb = b.getRelativeBlock(newPosition + v, v)
						if not isinstance(grb, list) or len(grb) == 0:
							continue
						b2 = game.getWorld().getBlockAt(grb[0][0])
						if b2 is None or not b2.canPass(self):
							self.__velocity.set(vector + v)
							return
					# 钻缝问题处理结束
					# 退出for循环，说明全部通过
					self.__velocity.set(vector + rel[0][1])
					return
				relativeBlock = game.getWorld().getBlockAt(rel[1][0])
				if relativeBlock is not None and relativeBlock.canPass(self):  # 1能过，trace新方向
					for b, v in game.getWorld().rayTraceBlock(newPosition, rel[1][1], rel[1][1].length()):
						if not isinstance(b, BlockVector):
							if b.canPass(self):
								continue
							# 还得判断钻缝的问题
							b = b.getBlockPosition()
						grb = b.getRelativeBlock(newPosition + v, v)
						if not isinstance(grb, list) or len(grb) == 0:
							continue
						b2 = game.getWorld().getBlockAt(grb[0][0])
						if b2 is None or not b2.canPass(self):
							self.__velocity.set(vector + v)
							return
					# 钻缝问题处理结束
					# 退出for循环，说明全部通过
					self.__velocity.set(vector + rel[1][1])
					return
				# 都不能过
				self.__velocity.set(vector)
				return
		self.__velocity.set(self._setVelocity)
		return
	
	def passTick(self) -> None:
		self._position.add(self.__velocity)
		self.lastDelta = 0
		self.processMove()
		if abs(self.__velocity.x) >= abs(self.__velocity.y):
			if self.__velocity.x < 0:
				self.__renderInterval -= 1
				if self._texture is self._textureSet[4]:
					if self.__renderInterval <= 0:
						self.__renderInterval = 6
						self._texture = self._textureSet[5]
				elif self._texture is self._textureSet[5]:
					if self.__renderInterval <= 0:
						self.__renderInterval = 6
						self._texture = self._textureSet[4]
				else:
					self._texture = self._textureSet[4]
			elif self.__velocity.x > 0:
				self.__renderInterval -= 1
				if self._texture is self._textureSet[6]:
					if self.__renderInterval <= 0:
						self.__renderInterval = 6
						self._texture = self._textureSet[7]
				elif self._texture is self._textureSet[7]:
					if self.__renderInterval <= 0:
						self.__renderInterval = 6
						self._texture = self._textureSet[6]
				else:
					self._texture = self._textureSet[6]
		else:
			if self.__velocity.y < 0:
				self.__renderInterval -= 1
				if self._texture is self._textureSet[2]:
					if self.__renderInterval <= 0:
						self.__renderInterval = 6
						self._texture = self._textureSet[3]
				elif self._texture is self._textureSet[3]:
					if self.__renderInterval <= 0:
						self.__renderInterval = 6
						self._texture = self._textureSet[2]
				else:
					self._texture = self._textureSet[2]
			elif self.__velocity.y > 0:
				self.__renderInterval -= 1
				if self._texture is self._textureSet[0]:
					if self.__renderInterval <= 0:
						self.__renderInterval = 6
						self._texture = self._textureSet[1]
				elif self._texture is self._textureSet[1]:
					if self.__renderInterval <= 0:
						self.__renderInterval = 6
						self._texture = self._textureSet[0]
				else:
					self._texture = self._textureSet[0]
		super().passTick()
	
	def updatePosition(self, delta: float | None = None) -> Vector:
		if delta is None:
			return self._renderPosition.clone()
		ld = self.lastDelta
		if ld > delta:
			delta = (ld + 1) / 2
		self._renderPosition = self._position + self.__velocity * delta
		return self._renderPosition.clone()
	
	def render(self, delta: float) -> None:
		self._texture.renderAtMap(self._renderPosition)
	
	def save(self) -> dict:
		ret = super().save()
		ret.update({
			"velocity": self.__velocity.save(),
			"basicMaxSpeed": self.basicMaxSpeed
		})
		return ret
	
	@classmethod
	def load(cls, d: dict, entity: Union['Entity', None] = None) -> Union['Entity', None]:
		entity._velocity = Vector.load(d["velocity"])
		entity.basicMaxSpeed = d["basicMaxSpeed"]
		entity.modifiedMaxSpeed = entity.basicMaxSpeed
		Entity.load(d, entity)
		return entity


class DeprecatedPlayer(MoveableEntity, Damageable):
	def __init__(self, name: str):
		"""
		创建玩家
		"""
		MoveableEntity.__init__(self, "player", name, EntityDescription(self), [
			resourceManager.getOrNew('player/no_player_1'),
			resourceManager.getOrNew('player/no_player_2'),
			resourceManager.getOrNew('player/no_player_b1'),
			resourceManager.getOrNew('player/no_player_b2'),
			resourceManager.getOrNew('player/no_player_l1'),
			resourceManager.getOrNew('player/no_player_l2'),
			resourceManager.getOrNew('player/no_player_r1'),
			resourceManager.getOrNew('player/no_player_r2'),
		], Vector(), 0.16)
		Damageable.__init__(self, 100)
		self.hunger = 0
	
	def onDeath(self) -> None:
		utils.info('死亡')
	
	def tick(self) -> None:
		v: Vector = Vector()
		if game.getWindow() is None:
			if interact.keys[pygame.K_w].peek():
				v.add(0, -1)
			if interact.keys[pygame.K_a].peek():
				v.add(-1, 0)
			if interact.keys[pygame.K_s].peek():
				v.add(0, 1)
			if interact.keys[pygame.K_d].peek():
				v.add(1, 0)
		self.setVelocity(v.normalize().multiply(self._maxSpeed))
	
	@classmethod
	def load(cls, d: dict, entity=None) -> 'DeprecatedPlayer':
		p = DeprecatedPlayer(d['name'])
		super().load(d, p)
		return p


class Rice(Entity):
	def __init__(self, position: Vector):
		super().__init__('entity.rice', '米粒', EntityDescription(self, [RenderableString("\\#FFFFD700黄色的米粒")]), [resourceManager.getOrNew('entity/rice')], position)
	
	def tick(self) -> None:
		player = game.getWorld().getPlayer()
		if player is not None and player.getPosition().distanceManhattan(self.getPosition()) <= 0.6:
			Music_player.sound_play(0)
			player.grow(1, self)
			game.getWorld().removeEntity(self)
	
	@classmethod
	def load(cls, d: dict, entity: Union['Entity', None] = None) -> Union['Entity', None]:
		e = Rice(Vector.load(d['position']))
		return Entity.load(d, e)


class Stick(Entity):
	def __init__(self, position: Vector):
		super().__init__('entity.stick', '树枝', EntityDescription(self, [RenderableString("\\#FFFFD700\\/坚硬的树枝"), RenderableString("\\#ffffd700用来搭窝")]), [resourceManager.getOrNew('entity/stick')], position)
	
	def tick(self) -> None:
		player = game.getWorld().getPlayer()
		if player is not None and player.getPosition().distanceManhattan(self.getPosition()) <= 0.6:
			Music_player.sound_play(1)
			player.pick(3, self)
			game.getWorld().removeEntity(self)
	
	@classmethod
	def load(cls, d: dict, entity: Union['Entity', None] = None) -> Union['Entity', None]:
		e = Stick(Vector.load(d['position']))
		return Entity.load(d, e)


class Clue(Entity):
	def __init__(self, position: Vector, i):
		super().__init__(f'entity.clue{i}', '线索', EntityDescription(self, [RenderableString("\\#FFFFD700通往真理的线索")]), [resourceManager.getOrNew('entity/clue')], position)
		self.num = i
	
	def tick(self) -> None:
		player = game.getWorld().getPlayer()
		if player is not None and player.getPosition().distanceManhattan(self.getPosition()) <= 0.6:
			Music_player.sound_play(1)
			from window.ingame import QuestionWindow
			game.setWindow(QuestionWindow(self.num))
			game.getWorld().removeEntity(self)
	
	@classmethod
	def load(cls, d: dict, entity: Union['Entity', None] = None) -> Union['Entity', None]:
		e = Stick(Vector.load(d['position']))
		return Entity.load(d, e)


skillGet: list[int] = [10, 22, 36, 52, 70, 90, 112, 136, 162, 190, 220, 252, 286, 322, 360, 400, 442, 486, 532, 580]


class Player(MoveableEntity, Damageable):
	def __init__(self, position: Vector):
		MoveableEntity.__init__(self, 'player', 'Chick', EntityDescription(self, [RenderableString("\\#FFFFD700黄色的小鸡"), RenderableString('\\/    也就是你')]), [
			resourceManager.getOrNew('player/chick_1'),
			resourceManager.getOrNew('player/chick_1'),
			resourceManager.getOrNew('player/chick_b1'),
			resourceManager.getOrNew('player/chick_b1'),
			resourceManager.getOrNew('player/chick_l1'),
			resourceManager.getOrNew('player/chick_l1'),
			resourceManager.getOrNew('player/chick_r1'),
			resourceManager.getOrNew('player/chick_r1'),
		], position, 0.12)
		Damageable.__init__(self, 100)
		self.totalGrowth: float = 0
		self.growth_value: float = 0  # 成长值初始化为0
		self.backpack_stick: float = 0  # 背包里树枝数量初始化为0
		self.preDeath: list[Callable[[], bool]] = []  # () -> bool是否取消
		self.preDamage: list[Callable[[float, Entity], float]] = []  # (float值, Entity来源) -> float更改后的值
		self.postDamage: list[Callable[[float, Entity], None]] = []  # (float值, Entity来源) -> None
		self.preTick: list[Callable[[], None]] = []
		self.postTick: list[Callable[[], None]] = []
		self.preGrow: list[Callable[[int, Entity | str], int]] = []
		self.postGrow: list[Callable[[int, Entity | str], None]] = []
		self.prePick: list[Callable[[int, Entity | str], None]] = []
		self.postPick: list[Callable[[int, Entity | str], None]] = []
		self.skills: dict[int, Skill] = {}
		self.activeSkills: list[Active] = []
		self.skillSelecting: int = -1
		self.__allSkills: dict[int, type] = skillManager.dic.copy()
		self.__allSkills.pop(0)
		self.progress = 1
		self.selectingRooster: int | Rooster | None = None
		self.nearestRooster: Rooster | None = None
		self.nearestRoosterDistance: float = 100
	
	def onDeath(self) -> None:
		flag = True
		for i in self.preDeath:
			if i():
				flag = False
		if flag:
			utils.info('死亡')
			game.setWindow(DeathWindow())
		else:
			self._isAlive = True
	
	def onDamage(self, amount: float, src: Entity) -> float:
		for i in self.preDamage:
			amount = i(amount, src)
		amount = Damageable.onDamage(self, amount, src)
		for i in self.postDamage:
			i(amount, src)
		return amount
	
	def save(self) -> dict:
		data = MoveableEntity.save(self)
		data.update(Damageable.save(self))
		data['growth_value'] = self.growth_value
		sks = []
		for sk in self.skills.values():
			sks.append(sk.save())
		for sk in self.activeSkills:
			sks.append(sk.save())
		data['skills'] = sks
		data['totalGrowth'] = self.totalGrowth
		data['progress'] = self.progress
		data['rooster'] = None if self.selectingRooster is None else self.selectingRooster.uuid
		return data
	
	@classmethod
	def load(cls, d: dict, entity: Union['Player', None] = None) -> 'Player':
		chicken = Player(Vector.load(d['position']))
		chicken.growth_value = d['growth_value']
		chicken.totalGrowth = d['totalGrowth']
		chicken.progress = d['progress'] if 'progress' in d else 1
		chicken.selectingRooster = d['rooster'] if 'rooster' in d and d['rooster'] != -1 else None
		for sk in d['skills']:
			s: Skill = skillManager.get(sk['id']).load(sk)
			chicken.__allSkills.pop(sk['id'])
			if sk['id'] >= 100:
				assert isinstance(s, Active)
				chicken.activeSkills.append(s)
			else:
				chicken.skills[sk['id']] = s
			s.init(chicken)
			if s.getLevel() != -1:
				s.upgrade()
		MoveableEntity.load(d, chicken)
		Damageable.load(d, chicken)
		return chicken
	
	def grow(self, amount: float, src: Entity | str) -> float:
		for i in self.preGrow:
			amount = i(amount, src)
		if self.growth_value == 100 or amount < 0:
			return 0
		val = self.growth_value + amount
		if val > 100:
			self.growth_value = 100
			ret = amount + 100 - self.growth_value
		else:
			self.growth_value = val
			ret = amount
		self.totalGrowth += ret
		for i in self.postGrow:
			i(ret, src)
		while self.totalGrowth > skillGet[len(self.skills) + len(self.activeSkills)]:
			if len(self.__allSkills) <= 0:
				break
			if len(self.skills) == 0:
				k = 1
			else:
				k = game.getWorld().getRandom().sample(sorted(self.__allSkills), 1)[0]
			sk: Skill = self.__allSkills.pop(k)()
			sk.upgrade()
			if isinstance(sk, Active):
				self.activeSkills.append(sk)
				game.hud.sendMessage(RenderableString('你获得了新的主动技能：') + self.activeSkills[-1].getName())
			else:
				self.skills[k] = sk
				game.hud.sendMessage(RenderableString('你获得了新的被动技能：') + self.skills[k].getName())
		if self.growth_value >= 100 and self.progress == 1:
			game.hud.sendMessage(RenderableString('\\#ffeeee00\\.ffee6666恭喜你，解锁了新的任务'))
			self.progress = 2
		return ret
	
	def pick(self, amount: int, src: Entity | str) -> int:
		for i in self.prePick:
			amount = i(amount, src)
		if self.backpack_stick == 100:
			return 0
		val = self.backpack_stick + amount
		if val > 100:
			self.backpack_stick = 100
			ret = amount + 100 - self.backpack_stick
		else:
			self.backpack_stick = val
			ret = amount
		for i in self.postPick:
			i(ret, src)
		return ret
	
	def nurture(self):
		self.setPosition(Vector(0, 0))
		if self.progress == 3:
			from window.ingame import NurturingWindow
			game.hud.sendMessage(RenderableString('\\#ffeeee00\\.ffee6666恭喜你，解锁了新的任务'))
			game.setWindow(NurturingWindow())
			self.progress = 4
		elif self.progress > 3:
			game.hud.sendMessage(RenderableString('\\#ffee0000你已经接受过教诲了'))
		else:
			game.hud.sendMessage(RenderableString('\\#ffee0000需要先完成前面的任务才可以接受巫婆鸡的教诲'))
	
	def tick(self) -> None:
		for i in self.preTick:
			i()
		v: Vector = Vector()
		if game.getWindow() is None:
			if interact.keys[pygame.K_w].peek():
				v.add(0, -1)
			if interact.keys[pygame.K_a].peek():
				v.add(-1, 0)
			if interact.keys[pygame.K_s].peek():
				v.add(0, 1)
			if interact.keys[pygame.K_d].peek():
				v.add(1, 0)
			if interact.specialKeys[pygame.K_LSHIFT & interact.KEY_COUNT].peek():
				self._maxSpeed = self.modifiedMaxSpeed * 0.5
			elif interact.specialKeys[pygame.K_LCTRL & interact.KEY_COUNT].peek():
				self._maxSpeed = self.modifiedMaxSpeed * 2
			else:
				self._maxSpeed = self.modifiedMaxSpeed
			# TODO: debug作弊代码，待删除
			if interact.keys[pygame.K_q].deals():
				self.grow(100, self)
				self.growth_value = 0
				self.grow(100, self)
				self.growth_value = 0
				self.grow(100, self)
				for i in self.skills.values():
					while i.upgrade():
						pass
					i.coolDown = 0
				for i in self.activeSkills:
					while i.upgrade():
						pass
					i.coolDown = 0
				self.pick(100, self)
			# debug
			if interact.keys[pygame.K_r].deals():
				if self.progress > 3:
					if self.selectingRooster is not None:
						if abs(self._position.x) > 3 or abs(self._position.y) > 3:
							game.hud.sendMessage(RenderableString("\\#ffee0000你已经选择了公鸡啦，莫要二心~"))
							game.hud.sendMessage(RenderableString("\\#ffee0000速速回到你自己的窝里去下蛋）~"))
						elif abs(self.selectingRooster.getPosition().x) > 3 or abs(self.selectingRooster.getPosition().y) > 3:
							game.hud.sendMessage(RenderableString("\\#ffee0000你的公鸡太远了，快去把他找回来"))
						else:
							game.setWindow(EggFactoryWindow())
					elif self.nearestRooster is None:
						game.hud.sendMessage(RenderableString("\\#ffee0000你附近没有单身公鸡，快去找找吧~"))
					else:
						near = self.nearestRooster
						self.selectingRooster = near
						near.description.d[0] = RenderableString("\\#ffeeee00你\\r的\\#ff4488ee公鸡")
						near.selected = True
						self.progress += 1
						game.hud.sendMessage(RenderableString('\\#ff0000ee你看着你选中的公鸡……'))
						game.hud.sendMessage(RenderableString('\\#ff0000ee回家下蛋！'))
						game.hud.sendMessage(RenderableString('\\#ffeeee00\\.ffee6666恭喜你，解锁了新的任务'))
				else:
					game.hud.sendMessage(RenderableString("\\#ffee0000你还没有接受教诲，别急着找公鸡~"))
			if interact.right.deals():
				self.skillSelecting = -1
			for i in range(9):
				push = interact.keys[pygame.K_1 + i].deals() & 1
				if i >= len(self.activeSkills):
					continue
				if push:
					if self.skillSelecting == i:
						self.activeSkills[self.skillSelecting].onUse(game.mouseAtMap)
						self.skillSelecting = -1
					else:
						self.skillSelecting = i
			if interact.keys[pygame.K_e].deals():
				from window.ingame import StatusWindow
				game.setWindow(StatusWindow())
			if interact.keys[pygame.K_RETURN].deals():
				from window.input import AiWindow
				game.setWindow(AiWindow())
			if interact.keys[pygame.K_h].deals():
				if self.progress < 2:
					game.hud.sendMessage(RenderableString('\\#ffee0000你还没有解锁这个任务~'))
				elif self.backpack_stick < 100:
					game.hud.sendMessage(RenderableString('\\#ffee0000你还没有足够的木棒来搭窝~'))
				elif self.progress == 2 and -3 < self._position.x < 3 and -3 < self._position.y < 3:
					game.hud.sendMessage(RenderableString('\\#ffeeee00\\.ffee6666恭喜你，解锁了新的任务'))
					self.backpack_stick = 0
					self.progress = 3
					from window.ingame import BuildingWindow
					game.setWindow(BuildingWindow())
					game.getWorld().addEntity(entityManager.get('entity.coop')(self._position.clone()))
				else:
					game.hud.sendMessage(RenderableString('\\#ffee0000请在家里搭窝，不然蛋会被捣蛋的狐狸偷走~'))
		if self.moveable == 0:
			self.setVelocity(v.normalize().multiply(self._maxSpeed))
		else:
			self.setVelocity(Vector(0, 0))
		for i in self.postTick:
			i()
	
	def renderSkill(self, delta: float) -> None:
		for i in range(len(self.activeSkills)):
			self.activeSkills[i].render(delta, game.mouseAtMap, i == self.skillSelecting)
	
	def render(self, delta: float) -> None:
		super().render(delta)
		if self.progress > 4 and abs(self._position.x) < 3 and abs(self._position.y) < 3:
			from render import font
			from render.renderer import renderer
			sfc = font.allFonts[10].get(False, False, False, False).render('按R下蛋！', False, (0xee, 0x66, 0x66), (0, 0, 0))
			sfc.set_colorkey((0, 0, 0))
			renderer.renderAtMap(sfc, self.updatePosition().add(Vector(0.5, -0.6)))


class Coop(Entity):
	def __init__(self, position: Vector):
		super().__init__('entity.coop', '鸡窝', EntityDescription(self, [RenderableString('鸡舍')]), [resourceManager.getOrNew('entity/coop')], position)
	
	@classmethod
	def load(cls, d: dict, entity: Union['Entity', None] = None) -> Union['Entity', None]:
		e = Coop(Vector.load(d['position']))
		return Entity.load(d, e)


class BlueEgg(Entity):
	def __init__(self, position: Vector):
		super().__init__('entity.egg.blue', '蓝色的蛋', EntityDescription(self, [RenderableString('\\#FF00D7FF蓝色的蛋'), RenderableString('\\#ff999999\\/    你别管为什么这么大')]), [a := resourceManager.getOrNew('egg/blue_egg'), a, a, a, a, a, a, a], position)
	
	@classmethod
	def load(cls, d: dict, entity: Union['Entity', None] = None) -> Union['Entity', None]:
		e = BlueEgg(Vector.load(d['position']))
		return Entity.load(d, e)


class GoldEgg(Entity):
	def __init__(self, position: Vector):
		super().__init__('entity.egg.blue', '金色的蛋', EntityDescription(self, [RenderableString('\\#FFF2B912金色的蛋'), RenderableString('\\#ff999999\\/    你别管为什么这么大')]), [a := resourceManager.getOrNew('egg/gold_egg'), a, a, a, a, a, a, a], position)
	
	@classmethod
	def load(cls, d: dict, entity: Union['Entity', None] = None) -> Union['Entity', None]:
		e = BlueEgg(Vector.load(d['position']))
		return Entity.load(d, e)


class RedEgg(Entity):
	def __init__(self, position: Vector):
		super().__init__('entity.egg.blue', '绯色的蛋', EntityDescription(self, [RenderableString('\\#FFB37153绯色的蛋'), RenderableString('\\#ff999999\\/    你别管为什么这么大')]), [a := resourceManager.getOrNew('egg/dark_red_egg'), a, a, a, a, a, a, a], position)
	
	@classmethod
	def load(cls, d: dict, entity: Union['Entity', None] = None) -> Union['Entity', None]:
		e = RedEgg(Vector.load(d['position']))
		return Entity.load(d, e)


class Witch(MoveableEntity):
	def __init__(self, position: Vector):
		src = resourceManager.getOrNew('entity/witch/witch')
		super().__init__('entity.witch', '老巫婆鸡', EntityDescription(self, [RenderableString('鸡长老'), RenderableString("    \\#ff994488\\/四个老巫鸡，是真是假？"), RenderableString('    \\#ffbb0000\\/确定真假之前，避开为妙'), RenderableString("    \\#ffeeeeee\\/寻找线索，解开真相")]), [src, src, src, src, src, src, src, src], position, 0.005)
		self._randomVelocity = Vector()
	
	def tick(self) -> None:
		player = game.getWorld().getPlayer()
		if player is not None and player.getPosition().distanceManhattan(self.getPosition()) <= 0.6:
			game.getWorld(0).setPlayer(player)
			game.setWorld(0)
			player.position = Vector(0, 0)
			player.nurture()
			self.description.d = [RenderableString("真·老巫鸡")]
		
		if self._randomVelocity.lengthManhattan() != 0:
			if game.getWorld().getRandom().random() < 0.01:
				self._randomVelocity.set(0, 0)
		else:
			if game.getWorld().getRandom().random() < 0.01:
				vel = Vector(game.getWorld().getRandom().random() - 0.5, game.getWorld().getRandom().random() - 0.5)
				if vel.lengthManhattan() != 0:
					vel.normalize().multiply(self._maxSpeed)
					self._randomVelocity = vel
				self.setVelocity(self._randomVelocity)


class FakeWitch(MoveableEntity):
	def __init__(self, position: Vector, i):
		src = resourceManager.getOrNew(f'entity/witch/witch{i}')
		super().__init__(f'entity.fakewitch{i}', '老巫婆鸡', EntityDescription(self, [RenderableString('鸡长老'), RenderableString("\\#ff994488\\/    四个老巫鸡，是真是假？"), RenderableString("\\#ffbb0000\\/    确定真假之前，避开为妙"), RenderableString("\\#ffeeeeee\\/    寻找线索，解开真相")]), [src, src, src, src, src, src, src, src], position, 0.005)
		self._randomVelocity = Vector()
		self.i = i
		self.flag = [True] * 3
	
	def tick(self) -> None:
		player = game.getWorld().getPlayer()
		if player is not None and player.getPosition().distanceManhattan(self.getPosition()) <= 0.3 and self.flag[self.i - 1]:
			game.hud.sendMessage(RenderableString('\\#ffeeee00\\.ffee6666你被骗了，这不是真正的老巫婆鸡'))
			game.hud.sendMessage(RenderableString('\\#ffeeee00\\.ffee6666你还被它重伤了！'))
			player._health -= 40
			self.flag[self.i - 1] = False
			self.description.d = [RenderableString("\\#ffee0000假·老巫鸡"), RenderableString("\\#ffee0000\\/    假的老巫鸡！")]
		
		if self._randomVelocity.lengthManhattan() != 0:
			if game.getWorld().getRandom().random() < 0.01:
				self._randomVelocity.set(0, 0)
		else:
			if game.getWorld().getRandom().random() < 0.01:
				vel = Vector(game.getWorld().getRandom().random() - 0.5, game.getWorld().getRandom().random() - 0.5)
				if vel.lengthManhattan() != 0:
					vel.normalize().multiply(self._maxSpeed)
					self._randomVelocity = vel
				self.setVelocity(self._randomVelocity)


class Rooster(MoveableEntity):
	def __init__(self, position: Vector, couple):
		super().__init__('entity.rooster', '鸡', EntityDescription(self, [RenderableString("\\#ff4488ee高傲\\r的\\#ff4488ee公鸡")]), [
			resourceManager.getOrNew('entity/rooster_1'),
			resourceManager.getOrNew('entity/rooster_2'),
			resourceManager.getOrNew('entity/rooster_b1'),
			resourceManager.getOrNew('entity/rooster_b2'),
			resourceManager.getOrNew('entity/rooster_l1'),
			resourceManager.getOrNew('entity/rooster_l2'),
			resourceManager.getOrNew('entity/rooster_r1'),
			resourceManager.getOrNew('entity/rooster_r2'),
		], position, 0.2)
		self.couple: Union['EnemyChicken', None] = couple
		self.center: Vector = self.couple.center if couple is not None else None
		self._randomVelocity: Vector = Vector()
		self.selected: bool = False
	
	def tick(self) -> None:
		if self.couple is not None and not self.couple._isAlive:
			self.center = None
			self.couple = None
			self.description.d[0] = RenderableString("\\#ff4488ee单身\\r的\\#ff4488ee公鸡")
		if self.center is None:
			if self.selected:
				player = game.getWorld().getPlayer()
				relative = player.getPosition().subtract(self.getPosition())
				distance = relative.length()
				if distance < 1:
					self.setVelocity(Vector())
				else:
					self.setVelocity(relative.multiply((distance - 1) / 2))
				return
			else:
				if self._randomVelocity.lengthManhattan() != 0:
					self.setVelocity(self._randomVelocity)
					if game.getWorld().getRandom().random() < 0.03:
						self._randomVelocity.set(0, 0)
				elif game.getWorld().getRandom().random() < 0.03:
					vel = Vector(game.getWorld().getRandom().random() - 0.5, game.getWorld().getRandom().random() - 0.5)
					if vel.lengthManhattan() != 0:
						vel.normalize().multiply(self.modifiedMaxSpeed * 0.1)
						self._randomVelocity = vel
			player = game.getWorld().getPlayer()
			if player is None or player.selectingRooster is not None:
				return
			if player.nearestRooster is self:
				distance = player.getPosition().distance(self.getPosition())
				if distance >= 2:
					player.nearestRooster = None
					player.nearestRoosterDistance = 100
			else:
				distance = player.getPosition().distance(self.getPosition())
				if distance < 2 and distance < player.nearestRoosterDistance:
					player.nearestRooster = self
					player.nearestRoosterDistance = distance
		else:
			if self._position.distanceManhattan(self.center) > 4:
				self._randomVelocity = (self.center - self._position + Vector(game.getWorld().getRandom().random() * 0.5, game.getWorld().getRandom().random() * 0.5)).normalize().multiply(self._maxSpeed * 0.2)
				self.setVelocity(self._randomVelocity)
			elif self._randomVelocity.lengthManhattan() != 0:
				self.setVelocity(self._randomVelocity)
				if game.getWorld().getRandom().random() < 0.03:
					self._randomVelocity.set(0, 0)
			elif game.getWorld().getRandom().random() < 0.03:
				vel = Vector(game.getWorld().getRandom().random() - 0.5, game.getWorld().getRandom().random() - 0.5)
				if vel.lengthManhattan() != 0:
					vel.normalize().multiply(self.modifiedMaxSpeed * 0.1)
					self._randomVelocity = vel
	
	def render(self, delta: float) -> None:
		super().render(delta)
		player = game.getWorld().getPlayer()
		if player is None or player.selectingRooster is not None:
			return
		if player.nearestRooster is self:
			from render import font
			from render.renderer import renderer
			sfc = font.allFonts[10].get(False, False, False, False).render('按R选择公鸡', False, (0, 0xee, 0x66), (0, 0, 0))
			sfc.set_colorkey((0, 0, 0))
			renderer.renderAtMap(sfc, self.updatePosition().add(Vector(0.5, -0.6)))
	
	def save(self) -> dict:
		dic = super().save()
		dic.update({
			'couple': self.couple.uuid if self.couple is not None else None,
			'selected': self.selected,
		})
		return dic
	
	@classmethod
	def load(cls, d: dict, entity: Union['Entity', None] = None) -> Union['Entity', None]:
		e = Rooster(Vector.load(d['position']), None)
		e.selected = d['selected'] if 'selected' in d else False
		e.couple = d['couple'] if 'couple' in d else None
		return Entity.load(d, e)


# 注册实体
entityManager.register('entity.rice', Rice)
entityManager.register('entity.stick', Stick)
entityManager.register('player', Player)
entityManager.register('entity.coop', Coop)
entityManager.register('entity.egg.blue', BlueEgg)
entityManager.register('entity.egg.red', RedEgg)
entityManager.register('entity.egg.gold', GoldEgg)
entityManager.register('deprecated', DeprecatedPlayer)
entityManager.register('entity.witch', Witch)
entityManager.register('entity.rooster', Rooster)

for t in range(1, 4):
	entityManager.register(f'entity.fakewitch{t}', FakeWitch)

for t in range(0, 4):
	entityManager.register(f'entity.clue{t}', Clue)

for t in [
	resourceManager.getOrNew('player/no_player_1'),
	resourceManager.getOrNew('player/no_player_2'),
	resourceManager.getOrNew('player/no_player_b1'),
	resourceManager.getOrNew('player/no_player_b2'),
	resourceManager.getOrNew('player/no_player_l1'),
	resourceManager.getOrNew('player/no_player_l2'),
	resourceManager.getOrNew('player/no_player_r1'),
	resourceManager.getOrNew('player/no_player_r2'),
]:
	t.getSurface().set_colorkey((0, 0, 0))
	t.getMapScaledSurface().set_colorkey((0, 0, 0))
	t.setOffset(Vector(0, -6))
for t in [
	resourceManager.getOrNew('entity/stick'),
	resourceManager.getOrNew('entity/coop'),
	resourceManager.getOrNew('entity/witch/witch')
]:
	t.getSurface().set_colorkey((0, 0, 0))
	t.getMapScaledSurface().set_colorkey((0, 0, 0))
	t.setOffset(Vector(0, -2))

t = resourceManager.getOrNew('entity/rice')
t.setOffset(Vector(0, -3))
t.getSurface().set_colorkey((0, 0, 0))
t.getMapScaledSurface().set_colorkey((0, 0, 0))
resourceManager.getOrNew('entity/witch/witch').setOffset(Vector(0, -7))

for t in [
	resourceManager.getOrNew('player/chick_1'),
	resourceManager.getOrNew('player/chick_b1'),
	resourceManager.getOrNew('player/chick_l1'),
	resourceManager.getOrNew('player/chick_r1'),
]:
	t.systemScaleOffset *= 10
	t.adaptsSystem()
	t.getSurface().set_colorkey((1, 1, 1))
	t.getMapScaledSurface().set_colorkey((1, 1, 1))
	t.setOffset(Vector(0, -4))
for t in [
	resourceManager.getOrNew('egg/blue_egg'),
	resourceManager.getOrNew('egg/dark_red_egg'),
	resourceManager.getOrNew('egg/gold_egg')
]:
	t.getSurface().set_colorkey((0xff, 0xff, 0xff))
	t.getMapScaledSurface().set_colorkey((0xff, 0xff, 0xff))
	t.setOffset(Vector(0, -7))
for t in \
	[
		resourceManager.getOrNew(f'entity/witch/witch{i}') for i in range(1, 4)
	] + [
		resourceManager.getOrNew('entity/clue'),
		resourceManager.getOrNew('entity/rooster_1'),
		resourceManager.getOrNew('entity/rooster_2'),
		resourceManager.getOrNew('entity/rooster_b1'),
		resourceManager.getOrNew('entity/rooster_b2'),
		resourceManager.getOrNew('entity/rooster_l1'),
		resourceManager.getOrNew('entity/rooster_l2'),
		resourceManager.getOrNew('entity/rooster_r1'),
		resourceManager.getOrNew('entity/rooster_r2'),
	]:
	t.getSurface().set_colorkey((0, 0, 0))
	t.getMapScaledSurface().set_colorkey((0, 0, 0))
	t.setOffset(Vector(0, -7))

del t
