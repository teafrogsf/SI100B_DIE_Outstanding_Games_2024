from typing import TYPE_CHECKING, Union

from pygame import Surface

from entity.manager import skillManager
from render.renderer import renderer, Location
from render.resource import resourceManager
from utils.game import game
from utils.text import SkillDescription, RenderableString, toRomanNumeral
from utils.vector import BlockVector

if TYPE_CHECKING:
	from entity.entity import Entity


class Skill:
	def __init__(self, skillID: int, description: SkillDescription):
		self._level: int = 0
		self._id: int = skillID
		self.player = None
		self.description: SkillDescription = description
		self.texture = resourceManager.getOrNew(f'skill/{self._id}')
		self.texture.uiScaleOffset = 0.025
		self.texture.systemScaleOffset = 0.1
		self.texture.adaptsSystem()
		self.texture.adaptsUI()
		self.texture.adaptsMap(False)
		self.coolDown: int = 0
		self.maxCoolDown: int = 0
		if game.getWorld() is not None:
			self.init(game.getWorld().getPlayer())
	
	def init(self, player) -> None:
		"""加载时，技能和玩家同时加载，所以技能拿不到game.getWorld().getPlayer()。独立出来以方便处理。"""
		self.player = player
	
	def getID(self) -> int:
		"""获取技能ID"""
		return self._id
	
	def getCoolDown(self) -> int:
		"""
		当前剩余的技能冷却时间，为0则已就绪
		"""
		return self.coolDown
	
	def getMaxCoolDown(self) -> int:
		"""
		技能冷却总时间，为0则不需要冷却
		"""
		return self.maxCoolDown
	
	def getLevel(self) -> int:
		if self._level == -1:
			self._level = 0
			return -1
		return self._level
	
	def getMaxLevel(self) -> int:
		return 10
	
	def upgradeCost(self) -> int:
		return 1
	
	def getName(self=None) -> RenderableString:
		return RenderableString('\\00空白技能')
	
	def render(self, delta: float, at: BlockVector, chosen: bool = None, isRenderIcon: bool = None) -> int:
		"""
		若为非主动技能，后两个参数忽略
		:return: 宽度
		"""
		self.texture.renderAtInterface(at)
		return self.texture.getUiScaledSurface().get_width()
	
	def upgrade(self) -> bool:
		"""
		升级这个技能
		:return: True - 成功，False - 失败
		"""
		self._level += 1
		return True
	
	def save(self) -> dict:
		return {
			'id': self._id,
			'level': self._level,
			'coolDown': self.coolDown
		}
	
	@classmethod
	def load(cls, d: dict) -> 'Skill':
		skill = skillManager.get(d['id'])()
		skill._level = d['level'] - 1
		skill.coolDown = d['coolDown']
		return skill


class SkillEasySatisfaction(Skill):
	def __init__(self):
		super().__init__(1, SkillDescription(self, [RenderableString('\\10\\#ffeeee00爱米'), RenderableString('\\#ffee55dd    可以从米粒中获得额外成长')]))
	
	def init(self, player) -> None:
		super().init(player)
		self.player.preGrow.append(self.onGrow)
	
	def getName(self=None) -> RenderableString:
		if self is None or self._level == 0:
			return RenderableString('\\10\\#ffeeee00爱米')
		else:
			return RenderableString('\\10\\#ffeeee00爱米' + (toRomanNumeral(self._level) if self._level < 20 else '(MAX)'))
	
	def getMaxLevel(self) -> int:
		return 20
	
	def upgrade(self) -> bool:
		if self._level < 20 and super().upgrade():
			self.description.d[0] = self.getName()
			self.description.d[1] = RenderableString(f'\\#ffee55dd    从米粒中获得额外{self._level / 10:.1f}点成长')
			return True
		return False
	
	def onGrow(self, amount: int, src: Union['Entity', str]) -> int:
		from entity.entity import Rice
		if isinstance(src, Rice):
			amount += self._level / 10
		return amount


class SkillResistance(Skill):
	def __init__(self):
		super().__init__(2, SkillDescription(self, [RenderableString('\\10\\#ffeeee00坚毅'), RenderableString(f'\\#ffee55dd    减少受到的0.00%伤害')]))
	
	def init(self, player) -> None:
		super().init(player)
		self.player.preDamage.append(self.onDamage)
	
	def getName(self=None) -> RenderableString:
		if self is None or self._level == 0:
			return RenderableString('\\10\\#ffeeeedd坚毅')
		else:
			return RenderableString('\\10\\#ffeeeedd坚毅' + (toRomanNumeral(self._level) if self._level < 100 else '(MAX)'))
	
	def getMaxLevel(self) -> int:
		return 100
	
	def upgrade(self) -> bool:
		if self._level < 100 and super().upgrade():
			self.description.d[0] = self.getName()
			self.description.d[1] = RenderableString(f'\\#ffee55dd    减少受到的{float(self._level * 100 / (10 + self._level)):.2f}%伤害')
			return True
		return False
	
	def upgradeCost(self) -> int:
		return 1
	
	def onDamage(self, amount: float, src: 'Entity') -> float:
		return amount * 10 / (10 + self._level)


class SkillFastGrow(Skill):
	def __init__(self):
		super().__init__(3, SkillDescription(self, [RenderableString('\\10\\#ffee8844揠苗'), RenderableString('\\#ffee55dd  每秒获得0.00点成长'), RenderableString('\\#ffee0000    但是每秒受到0.00点伤害！'), RenderableString('\\#ff888888    当然如果已经完全成长就不会受到伤害')]))
	
	def init(self, player) -> None:
		super().init(player)
		self.player.preTick.append(self.onTick)
	
	def getName(self=None) -> RenderableString:
		if self is None or self._level == 0:
			return RenderableString('\\10\\#ffee8844揠苗')
		else:
			return RenderableString('\\10\\#ffee8844揠苗' + (toRomanNumeral(self._level) if self._level < 100 else '(MAX)'))
	
	def getMaxLevel(self) -> int:
		return 100
	
	def upgrade(self) -> bool:
		if self._level < 100 and super().upgrade():
			self.description.d[0] = self.getName()
			self.description.d[1] = RenderableString(f'\\#ffee55dd    每秒获得{self._level / 50:.2f}点成长')
			self.description.d[2] = RenderableString(f'\\#ffee0000    但是每秒受到{self._level * 20 / (200 + self._level << 1):.2f}点伤害！')
			return True
		return False
	
	def onTick(self):
		if self.player.grow(self._level / 1000, 'SkillFastGrow') != 0:
			self.player.damage(self._level / (200 + self._level << 1), self.player)


class SkillRevive(Skill):
	def __init__(self):
		super().__init__(4, SkillDescription(self, [RenderableString('\\10\\#ffffff66屹立不倒'), RenderableString('\\#ffee55dd    死亡时可以立刻复活'), RenderableString('\\#ffee5555    体力回复 0.00%')]))
	
	def init(self, player) -> None:
		super().init(player)
		self.player.preTick.append(self.onTick)
		self.player.preDeath.append(self.onDeath)
	
	def render(self, delta: float, at: BlockVector, chosen: bool = None, isRenderIcon: bool = None) -> int:
		ret = super().render(delta, at)
		if self.coolDown > 0:
			s = Surface(self.texture.getMapScaledSurface().get_size())
			s.set_alpha(0xaa)
			renderer.getCanvas().blit(s, at.getTuple())
			renderer.renderString(RenderableString(f'\\11{int(self.coolDown / 20)}'), at.x + (s.get_width() >> 1), at.y + (s.get_height() >> 1), 0xffffffff, Location.CENTER)
		return ret
	
	def getName(self=None) -> RenderableString:
		if self is None or self._level == 0:
			return RenderableString('\\10\\#ffffff66屹立不倒')
		else:
			return RenderableString('\\10\\#ffffff66屹立不倒' + (toRomanNumeral(self._level) if self._level < 10 else "(MAX)"))
	
	def upgrade(self) -> bool:
		if self._level < 20 and super().upgrade():
			self.maxCoolDown = 2500 - self._level * 100
			self.description.d[0] = self.getName()
			self.description.d[2] = RenderableString(f'\\#ffee5555    体力回复 {20 + 3 * self._level:.2f}%')
			return True
		return False
	
	def onDeath(self):
		if self.coolDown <= 0:
			self.player.setHealth((20 + 3 * self._level) / 100 * self.player.getMaxHealth())
			self.coolDown = self.maxCoolDown
			game.hud.sendMessage(RenderableString('\\.ccff0000\\#ffeeeeee                 复生！                '))
			return True
		return False
	
	def onTick(self):
		if self.coolDown > 0:
			self.coolDown -= 1


class SkillSwift(Skill):
	def __init__(self):
		self.modifier = 0
		super().__init__(5, SkillDescription(self, [RenderableString('\\10\\#ff96F8F5迅捷'), RenderableString('\\#ffee55dd    快，快，快')]))
	
	def getName(self=None) -> RenderableString:
		if self is None or self._level == 0:
			return RenderableString('\\10\\#ff96F8F5迅捷')
		else:
			return RenderableString('\\10\\#ff96F8F5迅捷' + (toRomanNumeral(self._level) if self._level < 10 else "(MAX)"))
	
	def upgrade(self) -> bool:
		if self._level < 10 and super().upgrade():
			self.player.modifiedMaxSpeed -= self.modifier
			self.modifier = 0.005 * self._level
			self.player.modifiedMaxSpeed += self.modifier
			self.description.d[0] = self.getName()
			return True
		return False


skillManager.register(0, Skill)
skillManager.register(1, SkillEasySatisfaction)
skillManager.register(2, SkillResistance)
skillManager.register(3, SkillFastGrow)
skillManager.register(4, SkillRevive)
skillManager.register(5, SkillSwift)
