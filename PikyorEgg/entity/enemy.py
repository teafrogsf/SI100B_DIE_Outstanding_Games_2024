from typing import Union

from entity.entity import Entity, Damageable, MoveableEntity
from entity.manager import entityManager
from render.resource import Texture, resourceManager
from utils.util import utils
from utils.game import game
from utils.text import RenderableString, EntityDescription
from utils.vector import Vector


class Enemy(MoveableEntity, Damageable):
	def __init__(self, entityID: str, name: str, description: EntityDescription, texture: list[Texture], position: Vector, health: float = 100, speed: float = 0.06):
		MoveableEntity.__init__(self, entityID, name, description, texture, position, speed)
		Damageable.__init__(self, health)
		self._attackTimer: int = 0
		self._attackCoolDown: int = 10
		self._lockOn: Entity | None = None
		self._hasAI: bool = True
		self._aiVelocity: Vector = Vector(0, 0)  # AI建议的实体移动速度。
		self._randomVelocity: Vector = Vector(0, 0)  # 随机移动
	
	def ai(self) -> None:
		"""
		执行敌人的行动。在Entity.tick()前调用，也就是设置速度会被立刻应用。
		应当将AI建议的速度保存在_aiVelocity。
		可重写。
		"""
		pass
	
	def setAI(self, enabled: bool) -> None:
		"""
		设置敌人是否拥有AI
		"""
		self._hasAI = enabled
	
	def passTick(self) -> None:
		if self._hasAI:
			self.ai()
			self.setVelocity(self._aiVelocity)
		elif self._aiVelocity.lengthManhattan() != 0:
			self._aiVelocity.set(0, 0)
			self.setVelocity(Vector())
		if self._randomVelocity.lengthManhattan() != 0:
			if self._aiVelocity.lengthManhattan() == 0:
				self.setVelocity(self._randomVelocity)
				if game.getWorld().getRandom().random() < 0.01:
					self._randomVelocity.set(0, 0)
			else:
				self._randomVelocity.set(0, 0)
		else:
			if game.getWorld().getRandom().random() < 0.01:
				vel = Vector(game.getWorld().getRandom().random() - 0.5, game.getWorld().getRandom().random() - 0.5)
				if vel.lengthManhattan() != 0:
					vel.normalize().multiply(self.modifiedMaxSpeed * 0.4)
					self._randomVelocity = vel
		MoveableEntity.passTick(self)
	
	def save(self) -> dict:
		d = MoveableEntity.save(self)
		d['attackTimer'] = self._attackTimer
		d['attackCoolDown'] = self._attackCoolDown
		d['hasAI'] = self._hasAI
		d['aiVelocity'] = self._aiVelocity.save()
		return d
	
	@classmethod
	def load(cls, d: dict, entity: Union['Entity', None] = None) -> Union['Entity', None]:
		assert entity is not None
		assert isinstance(entity, Enemy)
		MoveableEntity.load(d, entity)
		entity._attackTimer = d['attackTimer']
		entity._attackCoolDown = d['attackCoolDown']
		entity._hasAI = d['hasAI']
		entity._aiVelocity = Vector.load(d['aiVelocity'])
		return entity


_EnemyUnit: RenderableString = RenderableString("\\#ffee7766    敌对单位")


def enemyUnit() -> RenderableString:
	return _EnemyUnit


def searchRange(sr: int) -> RenderableString:
	return RenderableString(f"\\#ffeedd66    搜索范围 {sr}")


def basicDamage(bd: float) -> RenderableString:
	return RenderableString(f"\\#ffee6677    基础伤害 {bd}")


class EnemyDog(Enemy):
	def __init__(self, position: Vector):
		super().__init__(
			"enemy.dog",
			"蠢蠢的狐狸",
			EntityDescription(
				self, [
					RenderableString("\\#ffee0000蠢蠢的狐狸"),
					RenderableString("\\#ffee55dd\\/    只会直线行走"),
					enemyUnit(),
					basicDamage(8),
					searchRange(4),
				]), [
				resourceManager.getOrNew("entity/enemy/dog_1"),
				resourceManager.getOrNew("entity/enemy/dog_2"),
				resourceManager.getOrNew("entity/enemy/dog_b1"),
				resourceManager.getOrNew("entity/enemy/dog_b2"),
				resourceManager.getOrNew("entity/enemy/dog_l1"),
				resourceManager.getOrNew("entity/enemy/dog_l2"),
				resourceManager.getOrNew("entity/enemy/dog_r1"),
				resourceManager.getOrNew("entity/enemy/dog_r2"),
			], position, 100, 0.09)
	
	def tick(self) -> None:
		if self._attackTimer:
			self._attackTimer -= 1
	
	def ai(self) -> None:
		if game.getWorld() is None:
			return
		player = game.getWorld().getPlayer()
		if player is None:
			self._lockOn = None
			self._aiVelocity.set(0, 0)
			return
		if self._lockOn is None or player is not self._lockOn:
			if player.getPosition().distanceManhattan(self.getPosition()) <= 4:
				self._lockOn = game.getWorld().getPlayer()
		else:
			if player.getPosition().distanceManhattan(self.getPosition()) > 4:
				self._lockOn = None
				self._aiVelocity.set(0, 0)
			elif utils.fequal((dist := player.getPosition().distance(self.getPosition())), 0):
				self._aiVelocity.set(0, 0)
			elif utils.fless(dist, self._maxSpeed):
				self._aiVelocity.set(0, 0)
				if self._attackTimer <= 0:
					self._lockOn.damage(8, self)
					self._attackTimer = self._attackCoolDown
			else:
				self._aiVelocity = self._lockOn.getPosition().subtract(self.getPosition()).normalize().multiply(min(self._maxSpeed, self.getPosition().distance(self._lockOn.getPosition())))
	
	@classmethod
	def load(cls, d: dict, entity: Union['Entity', None] = None) -> Union['Entity', None]:
		assert entity is None
		e = EnemyDog(Vector.load(d['position']))
		Enemy.load(d, e)
		return e


class EnemyChicken(Enemy):
	def __init__(self, position: Vector, centralPosition: Vector = None):
		super().__init__(
			"enemy.hen",
			"丰腴的情敌",
			EntityDescription(
				self, [
					RenderableString("\\#ffee0000丰腴的情敌"),
					RenderableString("\\#ffee55dd\\/    喜欢蹦蹦跳跳"),
					enemyUnit(),
					basicDamage(15),
					searchRange(2),
				]), [
				resourceManager.getOrNew("entity/enemy/hen_1"),
				resourceManager.getOrNew("entity/enemy/hen_2"),
				resourceManager.getOrNew("entity/enemy/hen_7"),
				resourceManager.getOrNew("entity/enemy/hen_8"),
				resourceManager.getOrNew("entity/enemy/hen_5"),
				resourceManager.getOrNew("entity/enemy/hen_6"),
				resourceManager.getOrNew("entity/enemy/hen_3"),
				resourceManager.getOrNew("entity/enemy/hen_4"),
			], position, 100, 0.25)
		self.center: Vector = centralPosition.clone() if centralPosition is not None else position.clone()
		self._attacked: bool = False
	
	def tick(self) -> None:
		if self._attackTimer:
			self._attackTimer -= 1
	
	def ai(self) -> None:
		if game.getWorld() is None:
			return
		player = game.getWorld().getPlayer()
		if player is None:
			self._lockOn = None
			self._aiVelocity.set(0, 0)
			return
		if self._lockOn is None or player is not self._lockOn:
			if player.getPosition().distanceManhattan(self.getPosition()) <= 2 and (player.progress > 1 or self._attacked):
				self._lockOn = game.getWorld().getPlayer()
		else:
			if player.getPosition().distanceManhattan(self.getPosition()) > 2:
				self._lockOn = None
				self._aiVelocity.set(0, 0)
			elif utils.fequal((dist := player.getPosition().distance(self.getPosition())), 0):
				self._aiVelocity.set(0, 0)
			elif utils.fless(dist, self._maxSpeed):
				self._aiVelocity.set(0, 0)
				if self._attackTimer <= 0:
					self._lockOn.damage(15, self)
					self._attackTimer = self._attackCoolDown
			else:
				self._aiVelocity = self._lockOn.getPosition().subtract(self.getPosition()).normalize().multiply(min(self._maxSpeed, self.getPosition().distance(self._lockOn.getPosition())))
	
	def passTick(self) -> None:
		if self._hasAI:
			self.ai()
			self.setVelocity(self._aiVelocity)
		elif self._aiVelocity.lengthManhattan() != 0:
			self._aiVelocity.set(0, 0)
			self.setVelocity(Vector())
		if self._position.distanceManhattan(self.center) > 3:
			if self._aiVelocity.lengthManhattan() == 0:
				self._randomVelocity = (self.center - self._position + Vector(game.getWorld().getRandom().random() * 0.5, game.getWorld().getRandom().random() * 0.5)).normalize().multiply(self._maxSpeed * 0.2)
				self.setVelocity(self._randomVelocity)
		elif self._randomVelocity.lengthManhattan() != 0:
			if self._aiVelocity.lengthManhattan() == 0:
				self.setVelocity(self._randomVelocity)
				if game.getWorld().getRandom().random() < 0.03:
					self._randomVelocity.set(0, 0)
			else:
				self._randomVelocity.set(0, 0)
		elif game.getWorld().getRandom().random() < 0.03:
			vel = Vector(game.getWorld().getRandom().random() - 0.5, game.getWorld().getRandom().random() - 0.5)
			if vel.lengthManhattan() != 0:
				vel.normalize().multiply(self.modifiedMaxSpeed * 0.1)
				self._randomVelocity = vel
		MoveableEntity.passTick(self)
	
	def onDamage(self, amount: float, src: Entity) -> float:
		if src is game.getWorld().getPlayer():
			self._attacked = True
		return super().onDamage(amount, src)
	
	@classmethod
	def load(cls, d: dict, entity: Union['Entity', None] = None) -> Union['Entity', None]:
		assert entity is None
		e = EnemyChicken(Vector.load(d['position']), Vector.load(d['center']))
		Enemy.load(d, e)
		e._attacked = d['attacked'] if 'attacked' in d else False
		return e
	
	def save(self) -> dict:
		d = Enemy.save(self)
		d['center'] = self.center.save()
		d['attacked'] = self._attacked
		return d


entityManager.register('enemy.dog', EnemyDog)
entityManager.register('enemy.hen', EnemyChicken)

for k in [
	resourceManager.getOrNew("entity/enemy/dog_1"),
	resourceManager.getOrNew("entity/enemy/dog_2"),
	resourceManager.getOrNew("entity/enemy/dog_b1"),
	resourceManager.getOrNew("entity/enemy/dog_b2"),
	resourceManager.getOrNew("entity/enemy/dog_l1"),
	resourceManager.getOrNew("entity/enemy/dog_l2"),
	resourceManager.getOrNew("entity/enemy/dog_r1"),
	resourceManager.getOrNew("entity/enemy/dog_r2"),
]:
	k.getSurface().set_colorkey((0, 0, 0))
	k.getMapScaledSurface().set_colorkey((0, 0, 0))
	k.setOffset(Vector(0, -5))
for k in [
	resourceManager.getOrNew("entity/enemy/hen_1"),
	resourceManager.getOrNew("entity/enemy/hen_2"),
	resourceManager.getOrNew("entity/enemy/hen_3"),
	resourceManager.getOrNew("entity/enemy/hen_4"),
	resourceManager.getOrNew("entity/enemy/hen_5"),
	resourceManager.getOrNew("entity/enemy/hen_6"),
	resourceManager.getOrNew("entity/enemy/hen_7"),
	resourceManager.getOrNew("entity/enemy/hen_8"),
]:
	k.getSurface().set_colorkey((0, 0, 0))
	k.getMapScaledSurface().set_colorkey((0, 0, 0))
	k.setOffset(Vector(0, -7))
del k
