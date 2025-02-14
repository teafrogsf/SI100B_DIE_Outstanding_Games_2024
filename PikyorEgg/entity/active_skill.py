import pygame
from pygame import Surface

from entity.manager import skillManager
from entity.skill import Skill
from interact.interacts import interact
from render.renderer import renderer, Location
from utils.game import game
from utils.text import SkillDescription, RenderableString, toRomanNumeral
from utils.vector import Vector, BlockVector


def renderSkill(distance: float, halfWidth: float, direction: Vector, color: int, withLine: bool = True) -> None:
	pos: Vector = game.getWorld().getPlayer().updatePosition()
	basis = renderer.getMapBasis()
	canvas: Surface = renderer.getCanvas()
	scale = renderer.getMapScale()
	ver = Vector(direction.y, -direction.x)
	ver.normalize().multiply(halfWidth)
	d = direction.clone().normalize().multiply(scale)
	rightDirection = pos + ver
	rightDirection.multiply(scale)
	leftDirection = pos - ver
	leftDirection.multiply(scale)
	pts = [
		rightDirection.getBlockVector(),
		(rightDirection + (dh := d * (distance - halfWidth))).getBlockVector(),
		(pos * scale + d * distance).getBlockVector(),
		(leftDirection + dh).getBlockVector(),
		leftDirection.getBlockVector(),
	]
	minX = min(pts, key=lambda x: x.x).x
	minY = min(pts, key=lambda x: x.y).y
	maxX = max(pts, key=lambda x: x.x).x
	maxY = max(pts, key=lambda x: x.y).y
	width = int(scale * 0.05)
	offset = BlockVector(minX - width, minY - width)
	size = (maxX - minX + width + width, maxY - minY + width + width)
	pygame.draw.lines(canvas, ((color >> 16) & 0xff, (color >> 8) & 0xff, color & 0xff), False, [(i.x + basis.x, i.y + basis.y) for i in pts], width)
	pts[0] = pts[0].subtract(offset).getTuple()
	pts[1] = pts[1].subtract(offset).getTuple()
	pts[2] = pts[2].subtract(offset).getTuple()
	pts[3] = pts[3].subtract(offset).getTuple()
	pts[4] = pts[4].subtract(offset).getTuple()
	sfc = Surface(size)
	sfc.set_alpha(color >> 24)
	sfc.set_colorkey((0, 0, 0))
	pygame.draw.polygon(sfc, ((color >> 16) & 0xff, (color >> 8) & 0xff, color & 0xff), pts)
	canvas.blit(sfc, (basis + offset).getTuple())
	if withLine:
		pygame.draw.line(renderer.getCanvas(), (0xee, 0, 0, 0x88), pos.multiply(scale).getBlockVector().add(basis).getTuple(), interact.mouse.getTuple(), max(1, int(renderer.getMapScale() / 24)))


def renderSkillRange(r: float, color: int, pos: Vector | BlockVector | None = None, withLine: bool = True) -> None:
	if pos is None:
		pos: Vector | BlockVector = game.getWorld().getPlayer().updatePosition()
	else:
		pos = pos.clone()
	basis = renderer.getMapBasis()
	canvas: Surface = renderer.getCanvas()
	scale = renderer.getMapScale()
	pos = pos.multiply(scale).getBlockVector().add(basis)
	r = int(r * scale)
	sfc = Surface((r << 1, r << 1))
	pygame.draw.circle(sfc, ((color >> 16) & 0xff, (color >> 8) & 0xff, color & 0xff), (r, r), r)
	sfc.set_alpha(color >> 24)
	sfc.set_colorkey((0, 0, 0))
	canvas.blit(sfc, (pos - BlockVector(r, r)).getTuple())
	pygame.draw.circle(canvas, ((color >> 16) & 0xff, (color >> 8) & 0xff, color & 0xff), (pos.x, pos.y), r, int(scale * 0.05))
	if withLine:
		pygame.draw.line(renderer.getCanvas(), (0xee, 0, 0, 0x88), pos.getTuple(), interact.mouse.getTuple(), max(1, int(renderer.getMapScale() / 24)))


class Active(Skill):
	def __init__(self, skillID: int, description: SkillDescription):
		super().__init__(skillID, description)
	
	def onUse(self, mouseAtMap: Vector) -> None:
		pass
	
	def onTick(self) -> None:
		if self.coolDown > 0:
			self.coolDown -= 1
	
	def render(self, delta: float, mouseAtMap: Vector | BlockVector, chosen: bool = False, isRenderIcon: bool = False) -> int | None:
		"""
		渲染效果。不管是技能释放预览，还是技能最终释放，都执行这个函数
		:param delta: tick偏移
		:param mouseAtMap: BlockVector屏幕图标，或者Vector鼠标在地图上的地图坐标，一般用于确定技能释放位置或方向
		:param chosen: 如果选中，则需要渲染技能预览
		:param isRenderIcon: 指示是否是在渲染技能图标
		:return: int在渲染技能图标后返回；非渲染技能图标时无需返回
		"""
		return super().render(delta, mouseAtMap)


class ActiveFlash(Active):
	def __init__(self):
		super().__init__(101, SkillDescription(self, [RenderableString('\\10\\#ff44aaee闪现'), RenderableString('    \\#ffaa4499向前方闪现一段距离'), RenderableString('    \\#ff4488ee冷却时间无穷秒')]))
		self.maxCoolDown = 600
		self.shouldSetPosition: Vector | None | tuple[Vector, float] = None
	
	def init(self, player) -> None:
		super().init(player)
		self.player.preTick.append(self.onTick)
	
	def getName(self=None) -> RenderableString:
		if self is None or self._level == 0:
			return RenderableString('\\10\\#ff44aaee闪现')
		else:
			return RenderableString('\\10\\#ff44aaee闪现' + (toRomanNumeral(self._level) if self._level < 5 else "(MAX)"))
	
	def getMaxLevel(self) -> int:
		return 5
	
	def upgrade(self) -> bool:
		if self._level < 5 and super().upgrade():
			self.description.d[0] = self.getName()
			self.description.d[2] = RenderableString(f'    \\#ff4488ee冷却时间{(650 - self._level * 50) / 20:.2f}秒')
			self.maxCoolDown = 650 - self._level * 50
			return True
		return False
	
	def upgradeCost(self) -> int:
		return 10
	
	def onTick(self) -> None:
		if self.coolDown > 0:
			self.coolDown -= 1
		if self.shouldSetPosition is not None:
			if isinstance(self.shouldSetPosition, Vector):
				self.player.moveable -= 1
				self.player.setPosition(self.shouldSetPosition)
				self.shouldSetPosition = 0
			elif isinstance(self.shouldSetPosition, int):
				self.shouldSetPosition = None
				self.player.moveable += 1
	
	def render(self, delta: float, at: Vector | BlockVector, chosen: bool = False, isRenderIcon: bool = False) -> None:
		if isRenderIcon:
			ret = super().render(delta, at)
			if self.coolDown > 0:
				s = Surface(self.texture.getUiScaledSurface().get_size())
				s.set_alpha(0xaa)
				renderer.getCanvas().blit(s, at.getTuple())
				renderer.renderString(RenderableString(f'\\11{int(self.coolDown / 20)}'), at.x + (s.get_width() >> 1), at.y + (s.get_height() >> 1), 0xffffffff, Location.CENTER)
			return ret
		elif chosen:
			renderSkill(3, 0.2, at - self.player.updatePosition(), 0x554499ee if self.coolDown <= 0 else 0x55ee4444, withLine=False)
	
	def onUse(self, mouseAtMap: Vector) -> None:
		if self.coolDown > 0:
			return
		direction = (mouseAtMap - (pos := self.player.updatePosition())).normalize().multiply(3)
		from block.block import Block
		block: Block = game.getWorld().getBlockAt((tar := pos + direction).getBlockVector())
		if block is not None and block.canPass(self.player):
			self.shouldSetPosition = tar
		else:
			res = game.getWorld().rayTraceBlock(tar, direction.reverse(), direction.length())
			if res is None:
				return
			for b, v in res:
				b: Block | BlockVector
				v: Vector
				if isinstance(b, BlockVector):
					continue
				if b.canPass(self.player):
					self.shouldSetPosition = tar + v
					break
		self.coolDown = self.maxCoolDown


class ActiveAdrenalin(Active):
	def __init__(self):
		super().__init__(102, SkillDescription(self, [RenderableString('\\10\\#ffaa0000肾上腺素'), RenderableString('    \\#ffaa4499短时间内不受伤害'), RenderableString(f'    \\#ffaa0000持续0.00秒')]))
		self.timeCount = 0
		self.maxCoolDown = 1200
	
	def init(self, player) -> None:
		super().init(player)
		self.player.preTick.append(self.onTick)
		self.player.preDamage.append(self.onDamage)
	
	def getName(self=None) -> RenderableString:
		if self is None or self._level == 0:
			return RenderableString('\\10\\#ffaa0000肾上腺素')
		else:
			return RenderableString('\\10\\#ffaa0000肾上腺素' + (toRomanNumeral(self._level) if self._level < 5 else "(MAX)"))
	
	def getMaxLevel(self) -> int:
		return 5
	
	def upgrade(self) -> bool:
		if self._level < 5 and super().upgrade():
			self.description.d[0] = self.getName()
			self.description.d[2] = RenderableString(f'    \\#ffaa0000持续{(60 + self._level * 8) / 20:.2f}秒')
			self.maxCoolDown = 900 - self._level * 60
			return True
		return False
	
	def render(self, delta: float, at: Vector | BlockVector, chosen: bool = False, isRenderIcon: bool = False) -> int | None:
		if isRenderIcon:
			ret = super().render(delta, at)
			if self.coolDown > 0:
				s = Surface(self.texture.getUiScaledSurface().get_size())
				s.set_alpha(0xaa)
				renderer.getCanvas().blit(s, at.getTuple())
				renderer.renderString(RenderableString(f'\\11{int(self.coolDown / 20)}'), at.x + (s.get_width() >> 1), at.y + (s.get_height() >> 1), 0xffffffff, Location.CENTER)
			return ret
		elif chosen:
			renderSkillRange(2, 0x554499ee if self.coolDown <= 0 else 0x55ee4444, withLine=False)
	
	def onTick(self) -> None:
		if self.coolDown > 0:
			self.coolDown -= 1
		if self.timeCount > 0:
			self.timeCount -= 1
	
	def onUse(self, mouseAtMap: Vector) -> None:
		if self.coolDown > 0:
			return
		self.timeCount = 60 + self._level * 8
		self.coolDown = self.maxCoolDown
	
	def onDamage(self, damage: float, entity) -> float:
		if self.timeCount > 0 and entity is not self.player and not isinstance(entity, str):
			return 0
		else:
			return damage


class ActiveAttack(Active):
	def __init__(self):
		super().__init__(103, SkillDescription(self, [RenderableString('\\10\\#ffeeee00猛啄'), RenderableString('    \\#ffaa4499向狐狸发起进攻！'), RenderableString(f'    \\#ffaa4499攻击范围 1.5L 2W'), RenderableString(f'    \\#ffeeee00对范围内狐狸造成0点伤害')]))
	
	def init(self, player) -> None:
		super().init(player)
		self.player.preTick.append(self.onTick)
	
	def getName(self=None) -> RenderableString:
		if self is None or self._level == 0:
			return RenderableString('\\10\\#ffeeee00猛啄')
		else:
			return RenderableString('\\10\\#ffeeee00猛啄' + (toRomanNumeral(self._level) if self._level < 10 else "(MAX)"))
	
	def upgrade(self) -> bool:
		if self._level < 10 and super().upgrade():
			self.description.d[0] = self.getName()
			self.description.d[3] = RenderableString(f'    \\#ffeeee00对范围内狐狸造成{10 + self._level}点伤害')
			return True
		return False
	
	def render(self, delta: float, mouseAtMap: Vector | BlockVector, chosen: bool = False, isRenderIcon: bool = False) -> int | None:
		if isRenderIcon:
			ret = super().render(delta, mouseAtMap)
			return ret
		elif chosen:
			renderSkill(1.5, 1, mouseAtMap - self.player.updatePosition(), 0x55eeee00 if self.coolDown <= 0 else 0x55ee4444, withLine=False)
	
	def onUse(self, mouseAtMap: Vector) -> None:
		if self.coolDown > 0:
			return
		pos = self.player.updatePosition()
		direction = mouseAtMap - pos
		direction.normalize()
		from entity.entity import Damageable
		from entity.entity import Entity
		for e in game.getWorld().getEntities():
			if not isinstance(e, Damageable):
				continue
			assert isinstance(e, Entity) and isinstance(e, Damageable)
			pe = e.updatePosition()
			rel = pe - pos
			if rel.lengthManhattan() > 2.2:
				continue
			cross = abs(rel.x * direction.y - rel.y * direction.x)
			if cross > 1:
				continue
			if rel.dot(direction) > 1.5:
				continue
			e.damage(10 + self._level, self.player)


class ActiveSwift(Active):
	def __init__(self):
		super().__init__(104, SkillDescription(self, [RenderableString('\\10\\#ff0088cc疾跑'), RenderableString('    \\#ffaa4499快，快，快……我不行了')]))
		self.timeCount = 0
		self.maxCoolDown = 800
	
	def init(self, player) -> None:
		super().init(player)
		self.player.preTick.append(self.onTick)
	
	def onTick(self) -> None:
		if self.coolDown > 0:
			self.coolDown -= 1
		if self.timeCount > 0:
			self.timeCount -= 1
			if self.timeCount == 0:
				self.player.modifiedMaxSpeed -= 0.1
	
	def getName(self=None) -> RenderableString:
		if self is None or self._level == 0:
			return RenderableString('\\10\\#ff0088cc疾跑')
		else:
			return RenderableString('\\10\\#ff0088cc疾跑' + (toRomanNumeral(self._level) if self._level < 10 else "(MAX)"))
	
	def onUse(self, mouseAtMap: Vector) -> None:
		if self.coolDown > 0:
			return
		self.timeCount = 60 + self._level * 10
		self.coolDown = self.maxCoolDown
		self.player.modifiedMaxSpeed += 0.1
	
	def upgrade(self) -> bool:
		if self._level < 10 and super().upgrade():
			self.description.d[0] = self.getName()
			return True
		return False
	
	def render(self, delta: float, mouseAtMap: Vector | BlockVector, chosen: bool = False, isRenderIcon: bool = False) -> int | None:
		if isRenderIcon:
			ret = super().render(delta, mouseAtMap)
			if self.coolDown > 0:
				s = Surface(self.texture.getUiScaledSurface().get_size())
				s.set_alpha(0xaa)
				renderer.getCanvas().blit(s, mouseAtMap.getTuple())
				renderer.renderString(RenderableString(f'\\11{int(self.coolDown / 20)}'), mouseAtMap.x + (s.get_width() >> 1), mouseAtMap.y + (s.get_height() >> 1), 0xffffffff, Location.CENTER)
			return ret
		elif chosen:
			renderSkillRange(1.5, 0x550088cc if self.coolDown <= 0 else 0x550088cc, withLine=False)


class ActiveBreak(Active):
	def __init__(self):
		super().__init__(105, SkillDescription(self, [RenderableString('\\10\\#ffaa0000头槌'), RenderableString(f'    \\#ffaa4499对范围内狐狸造成0点伤害'), RenderableString(f"    \\#ffaa4499吃得越饱，伤害越高"), RenderableString(f'    \\#ffee0000会消耗已有的40%的成长值')]))
		self.maxCoolDown = 100
		self.shouldResetMoveable = False
	
	def init(self, player) -> None:
		super().init(player)
		self.player.preTick.append(self.onTick)
	
	def getName(self=None) -> RenderableString:
		if self is None or self._level == 0:
			return RenderableString('\\10\\#ffaa0000头槌')
		else:
			return RenderableString('\\10\\#ffaa0000头槌' + (toRomanNumeral(self._level) if self._level < 10 else "(MAX)"))
	
	def upgrade(self) -> bool:
		if self._level < 10 and super().upgrade():
			self.description.d[0] = self.getName()
			self.description.d[1] = RenderableString(f'    \\#ffaa4499对范围内狐狸造成{7 + self.player.growth_value * 0.01 * (self._level + 10):.2f}点伤害')
			return True
		return False
	
	def onUse(self, mouseAtMap: Vector) -> None:
		if self.coolDown <= 0:
			self.coolDown = self.maxCoolDown
			self.player.moveable -= 1
			self.shouldResetMoveable = True
			self.player.setPosition(self.__matchPosition())
			from entity.enemy import Enemy
			for e in game.getWorld().getEntities():
				if isinstance(e, Enemy):
					e.damage(7 + self.player.growth_value * 0.01 * (self._level + 10), self.player)
			self.player.growth_value *= 0.6
	
	def onTick(self) -> None:
		super().onTick()
		if self.shouldResetMoveable:
			self.player.moveable += 1
			self.shouldResetMoveable = False
	
	def render(self, delta: float, mouseAtMap: Vector | BlockVector, chosen: bool = False, isRenderIcon: bool = False) -> int | None:
		if isRenderIcon:
			ret = super().render(delta, mouseAtMap)
			if self.coolDown > 0:
				s = Surface(self.texture.getUiScaledSurface().get_size())
				s.set_alpha(0xaa)
				renderer.getCanvas().blit(s, mouseAtMap.getTuple())
				renderer.renderString(RenderableString(f'\\11{int(self.coolDown / 20)}'), mouseAtMap.x + (s.get_width() >> 1), mouseAtMap.y + (s.get_height() >> 1), 0xffffffff, Location.CENTER)
			return ret
		elif chosen:
			renderSkillRange((3.5 + self._level * 0.2), 0x440088cc if self.coolDown <= 0 else 0x440088cc)
			renderSkillRange(1.5, 0x44eeee00 if self.coolDown <= 0 else 0x44ee4444, position := self.__matchPosition(), withLine=False)
			position = position.multiply(renderer.getMapScale()).getBlockVector().add(renderer.getMapBasis())
			pygame.draw.line(renderer.getCanvas(), (0xee, 0xee, 0, 0x88), (position.x - renderer.getMapScale(), position.y), (position.x + renderer.getMapScale(), position.y), max(1, int(renderer.getMapScale() / 24)))
			pygame.draw.line(renderer.getCanvas(), (0xee, 0xee, 0, 0x88), (position.x, position.y - renderer.getMapScale()), (position.x, position.y + renderer.getMapScale()), max(1, int(renderer.getMapScale() / 24)))

	def __matchPosition(self) -> Vector:
		relative = game.mouseAtMap.clone().subtract(self.player.updatePosition())
		if relative.length() > (3.5 + self._level * 0.2):
			relative.normalize().multiply((3.5 + self._level * 0.2))
		position = relative + self.player.updatePosition()
		targetBlock = game.getWorld().getBlockAt(position.getBlockVector())
		if targetBlock is None or not targetBlock.canPass(self.player):
			results = game.getWorld().rayTraceBlock(position, relative.reverse(), (3.5 + self._level * 0.2))
			for r in results:
				if isinstance(r[0], BlockVector):
					continue
				if r[0].canPass(self.player):
					position = position + r[1]
					break
			else:
				position = self.player.updatePosition()
		return position


class ActiveRegeneration(Active):
	def __init__(self):
		super().__init__(106, SkillDescription(self, [RenderableString('\\10\\#ff00ff00回复'), RenderableString(f'    \\#ff00ff00立即治疗自身0生命值')]))
		self.maxCoolDown = 300
		self.shouldResetMoveable = False
	
	def init(self, player) -> None:
		super().init(player)
		self.player.preTick.append(self.onTick)
	
	def upgrade(self) -> bool:
		if self._level < 10 and super().upgrade():
			self.description.d[0] = self.getName()
			self.description.d[1] = RenderableString(f'    \\#ff00ff00立即治疗自身{self._level * 5 + 30:.2f}生命值')
			return True
		return False
	
	def getName(self=None) -> RenderableString:
		if self is None or self._level == 0:
			return RenderableString('\\10\\#ff00ff00回复')
		else:
			return RenderableString('\\10\\#ff00ff00回复' + (toRomanNumeral(self._level) if self._level < 10 else "(MAX)"))
	
	def onTick(self) -> None:
		super().onTick()
	
	def onUse(self, mouseAtMap: Vector) -> None:
		if self.coolDown > 0:
			return
		player = game.getWorld().getPlayer()
		if player:
			self.coolDown = self.maxCoolDown
			player.heal(self._level * 5 + 30)
	
	def render(self, delta: float, mouseAtMap: Vector | BlockVector, chosen: bool = False, isRenderIcon: bool = False) -> int | None:
		if isRenderIcon:
			ret = super().render(delta, mouseAtMap)
			if self.coolDown > 0:
				s = Surface(self.texture.getUiScaledSurface().get_size())
				s.set_alpha(0xaa)
				renderer.getCanvas().blit(s, mouseAtMap.getTuple())
				renderer.renderString(RenderableString(f'\\11{int(self.coolDown / 20)}'), mouseAtMap.x + (s.get_width() >> 1), mouseAtMap.y + (s.get_height() >> 1), 0xffffffff, Location.CENTER)
			return ret
		else:
			if chosen:
				renderSkillRange(1.5, 0x44eeee00 if self.coolDown <= 0 else 0x44ee4444, position := self.player.updatePosition(), withLine=False)

skillManager.register(101, ActiveFlash)
skillManager.register(102, ActiveAdrenalin)
skillManager.register(103, ActiveAttack)
skillManager.register(104, ActiveSwift)
skillManager.register(105, ActiveBreak)
skillManager.register(106, ActiveRegeneration)
