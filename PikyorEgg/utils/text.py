from typing import TYPE_CHECKING, Union

from pygame import Surface

from render import font
from utils.util import utils

if TYPE_CHECKING:
	from block.block import Block
	from entity.entity import Entity
	from entity.skill import Skill


class Description:
	"""
	元素描述。如果重写，可以实现按时间不同变化的文字
	"""
	
	def __init__(self, d: list['RenderableString'] | None = None):
		self.d = [] if d is None else d
	
	def generate(self) -> list['RenderableString']:
		return self.d


class BlockDescription(Description):
	def __init__(self, block: 'Block', d: Union[list['RenderableString'], None] = None):
		super().__init__(d)
		self._block = block
	
	def generate(self) -> list['RenderableString']:
		return [RenderableString('\\#ffaa4499' + self._block.getBlockPosition().getTuple().__str__())] + self.d


class EntityDescription(Description):
	def __init__(self, entity: 'Entity', d: Union[list['RenderableString'], None] = None):
		super().__init__(d)
		self._entity = entity
	
	def generate(self) -> list['RenderableString']:
		from entity.entity import Damageable
		if isinstance(self._entity, Damageable):
			from entity.entity import Entity
			assert isinstance(self._entity, Entity) and isinstance(self._entity, Damageable)
			return [RenderableString('\\#ffaa4499' + self._entity.getPosition().toString() + (f'\\#ffee0000 UUID -1' if self._entity.uuid == -1 else f'\\#ffeeee00 UUID {self._entity.uuid}')), RenderableString(f'\\#ffee4444HP {self._entity.getHealth():.2f}/{self._entity.getMaxHealth():.2f}')] + self.d
		else:
			return [RenderableString('\\#ffaa4499' + self._entity.getPosition().toString() + (f'\\#ffee0000 UUID -1' if self._entity.uuid == -1 else f'\\#ffeeee00 UUID {self._entity.uuid}'))] + self.d


class SkillDescription(Description):
	def __init__(self, skill: 'Skill', d: Union[list['RenderableString'], None] = None):
		self._skill = skill
		super().__init__(d)
	
	def generate(self) -> list['RenderableString']:
		from entity.active_skill import Active
		if isinstance(self._skill, Active):
			return [RenderableString(f'\\#ffaa4499主动技能 {"就绪" if self._skill.getCoolDown() == 0 else (self._skill.getCoolDown() / 20)}/{int(self._skill.getMaxCoolDown() / 20)}秒')] + self.d
		else:
			return [RenderableString(f'\\#ffaa4499被动技能 {"就绪" if self._skill.getCoolDown() == 0 else int(self._skill.getCoolDown() / 20) + 1}/{int(self._skill.getMaxCoolDown() / 20)}秒' if self._skill.getMaxCoolDown() != 0 else '\\#ffaa4499被动技能')] + self.d


class InnerStringConfig:
	"""
	这是内部类，外部不应直接使用
	"""
	
	def __init__(self):
		self.string: str | None = None
		self.color: int = 0x1_ffff_ffff  # 多打一个一是为了后面的“默认颜色”用的
		self.background: int = 0x1_ffff_ffff  # 同上
		self.font: int = 0
		self.italic: bool = False
		self.bold: bool = False
		self.delete: bool = False
		self.underline: bool = False
	
	def renderAt(self, screen: Surface, x: int, y: int, defaultColor: int, defaultBackground: int = 0) -> int:
		dx = font.allFonts[self.font].draw(screen, self.string, x, y, defaultColor if self.color == 0x1_ffff_ffff else self.color, self.bold, self.italic, self.underline, self.delete, defaultBackground if self.background == 0x1_ffff_ffff else self.background)
		return x + dx
	
	def renderSmall(self, screen: Surface, x: int, y: int, defaultColor: int, defaultBackground: int = 0) -> int:
		smallFont = self.font if self.font >= 10 else self.font + 10
		dx = font.allFonts[smallFont].draw(screen, self.string, x, y, defaultColor if self.color == 0x1_ffff_ffff else self.color, self.bold, self.italic, self.underline, self.delete, defaultBackground if self.background == 0x1_ffff_ffff else self.background)
		return x + dx

	def renderGiant(self, screen: Surface, x: int, y: int, defaultColor: int, defaultBackground: int = 0) -> int:
		smallFont = self.font if self.font < 10 else self.font - 10
		dx = font.allFonts[smallFont].draw(screen, self.string, x, y, defaultColor if self.color == 0x1_ffff_ffff else self.color, self.bold, self.italic, self.underline, self.delete, defaultBackground if self.background == 0x1_ffff_ffff else self.background)
		return x + dx
	
	def clone(self) -> 'InnerStringConfig':
		ret: 'InnerStringConfig' = InnerStringConfig()
		ret.color = self.color
		ret.background = self.background
		ret.font = self.font
		ret.italic = self.italic
		ret.bold = self.bold
		ret.delete = self.delete
		ret.underline = self.underline
		return ret
	
	def cloneWithText(self) -> 'InnerStringConfig':
		ret = self.clone()
		ret.string = self.string
		return ret
	
	def appendString(self, string: str) -> None:
		if self.string is None:
			self.string = string
		else:
			self.string += string
	
	def length(self) -> int:
		if self.string is None:
			return 0
		return font.allFonts[self.font].get(self.bold, self.italic, self.underline, self.delete).size(self.string)[0]
	
	def lengthSmall(self) -> int:
		if self.string is None:
			return 0
		smallFont = self.font if self.font >= 10 else self.font + 10
		return font.allFonts[smallFont].get(self.bold, self.italic, self.underline, self.delete).size(self.string)[0]

	def lengthGiant(self) -> int:
		if self.string is None:
			return 0
		smallFont = self.font if self.font < 10 else self.font - 10
		return font.allFonts[smallFont].get(self.bold, self.italic, self.underline, self.delete).size(self.string)[0]
	
	def __str__(self) -> str:
		return \
			f'#{hex(self.color)[2:]}.{hex(self.background)[2:]}"' \
			f'"F?{"/" if self.italic else " "}' \
			f'{"=" if self.bold else " "}' \
			f'{"-" if self.delete else " "}' \
			f'{"_" if self.underline else " "}\n  ' \
			f'{self.string}'


class RenderableString:
	"""
	用于风格化字符串输出。以反斜线开头
	\\#AARRGGBB
	\\.AARRGGBB背景色
	\\xx
	\\-删除线
	\\_下划线
	\\/斜体
	\\=粗体
	\\r重置
	"""
	
	def __init__(self, string: str):
		self.set: list[InnerStringConfig] = []
		self._parseAppend(string)
	
	def _parseAppend(self, string: str) -> None:
		config = InnerStringConfig() if len(self.set) == 0 else self.set[-1].clone()
		subs = string.split('\\')
		if len(subs) == 0:
			return
		if subs[0] != '':
			config.appendString(subs[0])
			self.set.append(config)
			config = config.clone()
		for index in range(1, len(subs)):
			i = subs[index]
			if config.string is not None:
				self.set.append(config)
				config = config.clone()
			if len(i) == 0:
				config.appendString('\\')
				continue
			match i[0]:
				case '#':
					if len(i) < 9:
						continue
					if len(i) > 9:
						config.appendString(i[9:])
					config.color = int(i[1:9], 16)
				case '.':
					if len(i) < 9:
						continue
					if len(i) > 9:
						config.appendString(i[9:])
					config.background = int(i[1:9], 16)
				case 'f':
					if len(i) < 2:
						continue
					if len(i) > 2:
						config.appendString(i[2:])
					config.font = int(i[1])
				case '-' | 's' | 'S':
					config.delete = True
					if len(i) >= 1:
						config.appendString(i[1:])
				case '_' | 'u' | 'U':
					config.underline = True
					if len(i) >= 1:
						config.appendString(i[1:])
				case '/' | 'i' | 'I':
					config.italic = True
					if len(i) >= 1:
						config.appendString(i[1:])
				case '=' | 'b' | 'B':
					config.bold = True
					if len(i) >= 1:
						config.appendString(i[1:])
				case 'r':
					config = InnerStringConfig()
					if len(i) >= 1:
						config.appendString(i[1:])
				case '0':
					config.font = 0
					if len(i) >= 1:
						if ord('0') <= ord(i[1]) <= ord('2'):
							config.font = int(i[1])
					if len(i) >= 2:
						config.appendString(i[2:])
				case '1':
					config.font = 1
					if len(i) >= 1:
						if ord('0') <= ord(i[1]) <= ord('2'):
							config.font = int(i[1]) + 10
					if len(i) >= 2:
						config.appendString(i[2:])
				case _:
					utils.warn(f'无法识别的字符序列：{i}，来自\n{string}')
		if config.string is not None:
			self.set.append(config)
	
	def length(self) -> int:
		s = 0
		for i in self.set:
			s += i.length()
		return s
	
	def lengthSmall(self) -> int:
		s = 0
		for i in self.set:
			s += i.lengthSmall()
		return s
	
	def lengthGiant(self) -> int:
		s = 0
		for i in self.set:
			s += i.lengthGiant()
		return s
	
	def renderAt(self, screen: Surface, x: int, y: int, defaultColor: int, defaultBackground: int = 0) -> int:
		for i in self.set:
			x = i.renderAt(screen, x, y, defaultColor, defaultBackground)
		return x
	
	def renderSmall(self, screen: Surface, x: int, y: int, defaultColor: int, defaultBackground: int = 0) -> int:
		for i in self.set:
			x = i.renderSmall(screen, x, y, defaultColor, defaultBackground)
		return x

	def renderGiant(self, screen: Surface, x: int, y: int, defaultColor: int, defaultBackground: int = 0) -> int:
		for i in self.set:
			x = i.renderGiant(screen, x, y, defaultColor, defaultBackground)
		return x
	
	def clone(self) -> 'RenderableString':
		ret: 'RenderableString' = RenderableString('')
		ret.set = self.set.copy()
		for i in range(len(ret.set)):
			ret.set[i] = ret.set[i].cloneWithText()
		return ret
	
	def append(self, string: str) -> 'RenderableString':
		self._parseAppend(string)
		return self
	
	def __add__(self, other: Union['RenderableString', str]) -> 'RenderableString':
		r = self.clone()
		if isinstance(other, str):
			return r.append(other)
		else:
			r.set += other.set
			return r
	
	def __str__(self):
		return '\n'.join([str(i) for i in self.set])


def toRomanNumeral(value: int) -> str:
	if value == 0:
		return "N"
	if value >= 4000:
		return str(value)
	k = value // 1000
	h = value % 1000 // 100
	t = value % 100 // 10
	a = value % 10
	if k == 0:
		ret = ''
	elif k == 1:
		ret = "M"
	elif k == 2:
		ret = "MM"
	elif k == 3:
		ret = "MMM"
	else:
		return str(value)
	if h != 0:
		if h == 1:
			ret += "C"
		elif h == 2:
			ret += "CC"
		elif h == 3:
			ret += "CCC"
		elif h == 4:
			ret += "CD"
		elif h == 5:
			ret += "D"
		elif h == 6:
			ret += "DC"
		elif h == 7:
			ret += "DCC"
		elif h == 8:
			ret += "DCCC"
		else:
			ret += "CM"
	if t != 0:
		if t == 1:
			ret += "X"
		elif t == 2:
			ret += "XX"
		elif t == 3:
			ret += "XXX"
		elif t == 4:
			ret += "XL"
		elif t == 5:
			ret += "L"
		elif t == 6:
			ret += "LX"
		elif t == 7:
			ret += "LXX"
		elif t == 8:
			ret += "LXXX"
		else:
			ret += "XC"
	if a != 0:
		if a == 1:
			ret += "I"
		elif a == 2:
			ret += "II"
		elif a == 3:
			ret += "III"
		elif a == 4:
			ret += "IV"
		elif a == 5:
			ret += "V"
		elif a == 6:
			ret += "VI"
		elif a == 7:
			ret += "VII"
		elif a == 8:
			ret += "VIII"
		else:
			ret += "IX"
	return ret
