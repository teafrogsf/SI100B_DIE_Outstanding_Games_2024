import math
from typing import Union

from utils.util import utils
from utils.error import InvalidOperationException


class Matrix:
	def __init__(self, M2x2: Union[list[float], list[list[float]], tuple[tuple[float, float], tuple[float, float]]]):
		"""
		创建变换矩阵
		:param M2x2: 可以是((a1, a2), (b1, b2))或[[a1, a2], [b1, b2]]或[a1, a2, b1, b2]的形式
		"""
		if isinstance(M2x2, list) and len(M2x2) >= 4 and isinstance(M2x2[0], float):
			self._a1: float = float(M2x2[0])
			self._a2: float = float(M2x2[1])
			self._b1: float = float(M2x2[2])
			self._b2: float = float(M2x2[3])
		else:
			self._a1: float = M2x2[0][0]
			self._a2: float = M2x2[0][1]
			self._b1: float = M2x2[1][0]
			self._b2: float = M2x2[1][1]
	
	def add(self, other: Union['Matrix', int, float]) -> 'Matrix':
		if isinstance(other, Matrix):
			self._a1 += other._a1
			self._a2 += other._a2
			self._b1 += other._b1
			self._b2 += other._b2
		else:
			self._a1 += other
			self._a2 += other
			self._b1 += other
			self._b2 += other
		return self
	
	def subtract(self, other: Union['Matrix', int, float]) -> 'Matrix':
		if isinstance(other, Matrix):
			self._a1 -= other._a1
			self._a2 -= other._a2
			self._b1 -= other._b1
			self._b2 -= other._b2
		else:
			self._a1 -= other
			self._a2 -= other
			self._b1 -= other
			self._b2 -= other
		return self
	
	def multiply(self, other: Union['Matrix', 'Vector', 'BlockVector', int, float]) -> Union['Matrix', 'Vector']:
		if isinstance(other, Matrix):
			self._a1, self._a2, self._b1, self._b2 = other._a1 * self._a1 + other._a2 * self._b1, other._a1 * self._a2 + other._a2 * self._b2, other._b1 * self._a1 + other._b2 * self._b1, other._b1 * self._a2 + other._b2 * self._b2
			return self
		elif isinstance(other, Vector) or isinstance(other, BlockVector):
			return Vector(self._a1 * other.x + self._a2 * other.y, self._b1 * other.x + self._b2 * other.y)
		else:
			self._a1 *= other
			self._a2 *= other
			self._b1 *= other
			self._b2 *= other
			return self
	
	def __eq__(self, other: 'Matrix') -> bool:
		return self._a1 == other._a1 and self._a2 == other._a2 and self._b1 == other._b1 and self._b2 == other._b2
	
	def __add__(self, other: Union['Matrix', int, float]) -> 'Matrix':
		if isinstance(other, Matrix):
			return Matrix([[self._a1 + other._a1, self._a2 + other._a2], [self._b1 + other._b1, self._b2 + other._b2]])
		else:
			return Matrix([[self._a1 + other, self._a2 + other], [self._b1 + other, self._b2 + other]])
	
	def __sub__(self, other: Union['Matrix', int, float]) -> 'Matrix':
		if isinstance(other, Matrix):
			return Matrix([[self._a1 - other._a1, self._a2 - other._a2], [self._b1 - other._b1, self._b2 - other._b2]])
		else:
			return Matrix([[self._a1 - other, self._a2 - other], [self._b1 - other, self._b2 - other]])
	
	def __mul__(self, other: float | int) -> 'Matrix':
		return Matrix([[self._a1 * other, self._a2 * other], [self._b1 * other, self._b2 * other]])
	
	def __rmul__(self, other: float | int) -> 'Matrix':
		return Matrix([[self._a1 * other, self._a2 * other], [self._b1 * other, self._b2 * other]])
	
	def __matmul__(self, other: Union['Matrix', 'Vector', 'BlockVector']) -> Union['Matrix', 'Vector']:
		if isinstance(other, Matrix):
			return Matrix([[self._a1 * other._a1 + self._a2 * other._b1, self._a1 * other._a2 + self._a2 * other._b2], [self._b1 * other._a1 + self._b2 * other._b1, self._b1 * other._a2 + self._b2 * other._b2]])
		else:
			return Vector(self._a1 * other.x + self._a2 * other.y, self._b1 * other.x + self._b2 * other.y)


class Matrices:
	yOnly = Matrix([[0, 0], [0, 1]])
	xOnly = Matrix([[1, 0], [0, 0]])


class Vector:
	def __init__(self, x: float = 0, y: float = 0):
		"""
		屏幕上的点，或世界上的点。方块采用整数，其余采用浮点
		:param x: 横坐标，相对左上角。
		:param y: 纵坐标，相对左上角
		"""
		self.x = x
		self.y = y
	
	def set(self, x_or_pos: Union[float, tuple[float, float], 'Vector'], y_or_None: float | None = None) -> None:
		"""
		重设坐标。可以直接传入一个唯一参数set((x, y))元组，也可以传入两个参数set(x, y)
		"""
		if isinstance(x_or_pos, tuple):
			self.x = x_or_pos[0]
			self.y = x_or_pos[1]
		elif isinstance(x_or_pos, Vector):
			self.x = x_or_pos.x
			self.y = x_or_pos.y
		else:
			self.x = x_or_pos
			self.y = y_or_None
	
	def setX(self, x: float) -> 'Vector':
		self.x = x
		return self
	
	def setY(self, y: float) -> 'Vector':
		self.y = y
		return self
	
	def add(self, x: Union[float, tuple[float, float], 'Vector'], y: float | None = None) -> 'Vector':
		if isinstance(x, tuple):
			x, y = x
		elif isinstance(x, Vector) or isinstance(x, BlockVector):
			x, y = x.x, x.y
		self.x += x
		self.y += y
		return self
	
	def subtract(self, x: Union[float, tuple[float, float], 'Vector'], y: float | None = None) -> 'Vector':
		if isinstance(x, tuple):
			x, y = x
		elif isinstance(x, Vector) or isinstance(x, BlockVector):
			x, y = x.x, x.y
		self.x -= x
		self.y -= y
		return self
	
	def multiply(self, mul) -> 'Vector':
		self.x *= mul
		self.y *= mul
		return self
	
	def divide(self, div) -> 'Vector':
		self.x /= div
		self.y /= div
		return self
	
	def dot(self, other: 'Vector') -> float:
		return self.x * other.x + self.y * other.y
	
	def clone(self) -> 'Vector':
		return Vector(self.x, self.y)
	
	def length(self) -> float:
		return float(self.x ** 2 + self.y ** 2) ** 0.5
	
	def lengthManhattan(self) -> float:
		return abs(self.x) + abs(self.y)
	
	def normalize(self) -> 'Vector':
		if self.x == 0 and self.y == 0:
			return self
		selfLength = self.length()
		self.x /= selfLength
		self.y /= selfLength
		return self
	
	def floor(self) -> 'Vector':
		self.x = int(self.x)
		self.y = int(self.y)
		return self
	
	def reverse(self) -> 'Vector':
		self.x = -self.x
		self.y = -self.y
		return self
	
	def distance(self, other: 'Vector') -> float:
		return float((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
	
	def distanceManhattan(self, other: 'Vector') -> float:
		return abs(self.x - other.x) + abs(self.y - other.y)
	
	def getTuple(self) -> tuple[float, float]:
		return self.x, self.y
	
	def getBlockVector(self) -> 'BlockVector':
		return BlockVector(math.floor(self.x), math.floor(self.y))
	
	def getBlockTuple(self) -> tuple[int, int]:
		return math.floor(self.x), math.floor(self.y)
	
	def directionalCloneBlock(self) -> 'BlockVector':
		"""
		查看方向性。对于x和y，如果大于0，修改为1；如果小于0，修改为-1；否则修改为0
		:return:
		"""
		return BlockVector(0 if self.x == 0 else (1 if self.x > 0 else -1), 0 if self.y == 0 else (1 if self.y > 0 else -1))
	
	def directionalClone(self) -> 'Vector':
		"""
		查看方向性。对于x和y，如果大于0，修改为1；如果小于0，修改为-1；否则修改为0
		:return:
		"""
		return Vector(0 if self.x == 0 else (1 if self.x > 0 else -1), 0 if self.y == 0 else (1 if self.y > 0 else -1))
	
	def pointVerticalTo(self, line: 'Vector') -> 'Vector':
		"""
		将本坐标视为坐标点，求该点到直线的垂线向量，包含长度。
		:param line: 目标直线
		:return: 垂线
		"""
		d = line.clone().normalize()
		length = d.x * self.y - d.y * self.x
		if length == 0:
			return Vector(0, 0)
		d.x, d.y = d.y, -d.x
		return d.multiply(length)
	
	def xInteger(self) -> bool:
		return self.x == int(self.x)
	
	def yInteger(self) -> bool:
		return self.y == int(self.y)
	
	def extendX(self, x: float) -> 'Vector':
		"""
		更改x的值，并等比放大向量
		:param x: 目标x
		:return: 自身。如果self.x == 0且x != 0则直接返回自身，不做扩展
		"""
		if utils.fequal(self.x, 0):
			if x != 0:
				utils.warn(f'扩展向量的零值。{self}: {x = }')
			return self
		self.y = self.y / self.x * x
		self.x = x
		return self
	
	def extendY(self, y: float) -> 'Vector':
		"""
		更改y的值，并等比放大向量
		:param y: 目标y
		:return: 自身。如果self.y == 0则直接返回自身，不做扩展
		"""
		if utils.fequal(self.y, 0):
			if y != 0:
				utils.warn(f'扩展向量的零值。{self}: {y = }')
			return self
		self.x = self.x / self.y * y
		self.y = y
		return self
	
	def toString(self) -> str:
		return f'({self.x:.3f}, {self.y:.3f})'
	
	def save(self) -> dict:
		return {
			'x': self.x,
			'y': self.y
		}
	
	@classmethod
	def load(cls, d: dict) -> 'Vector':
		return Vector(d['x'], d['y'])
	
	def __len__(self) -> float:
		return float(self.x ** 2 + self.y ** 2) ** 0.5
	
	def __add__(self, other: 'Vector') -> 'Vector':
		return Vector(self.x + other.x, self.y + other.y)
	
	def __sub__(self, other: 'Vector') -> 'Vector':
		return Vector(self.x - other.x, self.y - other.y)
	
	def __mul__(self, val: float) -> 'Vector':
		return Vector(self.x * val, self.y * val)
	
	def __rmul__(self, val: float) -> 'Vector':
		return Vector(self.x * val, self.y * val)
	
	def __truediv__(self, other: float) -> 'Vector':
		return Vector(self.x / other, self.y / other)
	
	def __eq__(self, other: 'Vector') -> bool:
		return self.x == other.x and self.y == other.y
	
	def __str__(self) -> str:
		return f'Vector({self.x}, {self.y})'
	
	def __repr__(self) -> str:
		return f'Vector({self.x}, {self.y})'


class BlockVector:
	def __init__(self, x: int = 0, y: int = 0):
		"""
		屏幕上的点，或世界上的点。方块采用整数，其余采用浮点
		:param x: 横坐标，相对左上角。
		:param y: 纵坐标，相对左上角
		"""
		if x >= 0x1_0000 or y >= 0x1_0000 or x <= -0xffff or y <= -0xffff:
			raise ValueError('BlockVector out of range')
		self.x = x
		self.y = y
	
	def set(self, x_or_pos: Union[int, tuple[int, int], 'BlockVector'], y_or_None: int | None = None) -> None:
		"""
		重设坐标。可以直接传入一个唯一参数set((x, y))元组，也可以传入两个参数set(x, y)
		"""
		if isinstance(x_or_pos, tuple):
			self.x = int(x_or_pos[0])
			self.y = int(x_or_pos[1])
		elif isinstance(x_or_pos, BlockVector) or isinstance(x_or_pos, Vector):
			self.x = int(x_or_pos.x)
			self.y = int(x_or_pos.y)
		else:
			self.x = int(x_or_pos)
			self.y = int(y_or_None)
	
	def setX(self, x: int) -> 'BlockVector':
		self.x = int(x)
		return self
	
	def setY(self, y: int) -> 'BlockVector':
		self.y = int(y)
		return self
	
	def add(self, x: Union[int, tuple[int, int], 'BlockVector'], y: int | None = None) -> 'BlockVector':
		if isinstance(x, tuple):
			x, y = x
		elif isinstance(x, BlockVector) or isinstance(x, Vector):
			x, y = x.x, x.y
		self.x += x
		self.y += y
		return self
	
	def subtract(self, x: Union[int, tuple[int, int], 'BlockVector'], y: int | None = None) -> 'BlockVector':
		if isinstance(x, tuple):
			x, y = x
		elif isinstance(x, BlockVector) or isinstance(x, Vector):
			x, y = x.x, x.y
		self.x -= x
		self.y -= y
		return self
	
	def multiply(self, mul: int | float) -> 'BlockVector':
		self.x = (self.x * mul)
		self.y = (self.y * mul)
		return self
	
	def dot(self, other: 'BlockVector') -> int:
		return self.x * other.x + self.y * other.y
	
	def clone(self) -> 'BlockVector':
		return BlockVector(self.x, self.y)
	
	def length(self) -> float:
		return float(self.x ** 2 + self.y ** 2) ** 0.5
	
	def lengthManhattan(self) -> int:
		return abs(self.x) + abs(self.y)
	
	def distance(self, other: 'BlockVector') -> float:
		return float((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
	
	def distanceManhattan(self, other: 'BlockVector') -> float:
		return abs(self.x - other.x) + abs(self.y - other.y)
	
	def normalizeClone(self) -> 'Vector':
		if self.x == 0 and self.y == 0:
			return Vector()
		selfLength = self.length()
		return Vector(self.x / selfLength, self.y / selfLength)
	
	def reverse(self) -> 'BlockVector':
		self.x = -self.x
		self.y = -self.y
		return self
	
	def floor(self) -> 'BlockVector':
		self.x = int(self.x)
		self.y = int(self.y)
		return self
	
	def getTuple(self) -> tuple[int, int]:
		return self.x, self.y
	
	def getVector(self) -> Vector:
		return Vector(self.x, self.y)
	
	def directionalCloneBlock(self) -> 'BlockVector':
		"""
		查看方向性。对于x和y，如果大于0，修改为1；如果小于0，修改为-1；否则修改为0
		:return:
		"""
		return BlockVector(0 if self.x == 0 else 1 if self.x > 0 else -1, 0 if self.y == 0 else 1 if self.y > 0 else -1)
	
	def directionalClone(self) -> 'Vector':
		"""
		查看方向性。对于x和y，如果大于0，修改为1；如果小于0，修改为-1；否则修改为0
		:return:
		"""
		return Vector(0 if self.x == 0 else 1 if self.x > 0 else -1, 0 if self.y == 0 else 1 if self.y > 0 else -1)
	
	def pointVerticalTo(self, line: Vector) -> Vector:
		"""
		将本坐标视为坐标点，求该点到直线的垂线向量，包含长度。
		:param line: 目标直线
		:return: 垂线
		"""
		d = line.clone().normalize()
		length = d.x * self.y - d.y * self.x
		if length == 0:
			return Vector(0, 0)
		d.x, d.y = d.y, -d.x
		return d.multiply(length)
	
	def contains(self, point: Vector) -> bool:
		"""
		检查方块是否包含目标点
		:param point: 目标点
		"""
		return self.x <= point.x <= self.x + 1 and self.y <= point.y <= self.y + 1
	
	def covers(self, point: Vector) -> bool:
		"""
		检查目标点是否恰好在方块内部
		"""
		return self.x < point.x < self.x + 1 and self.y < point.y < self.y + 1
	
	def atBorder(self, point: Vector) -> bool:
		"""
		检查目标点是否恰好在方块边界
		"""
		return point.x == self.x or point.y == self.y or point.x == self.x + 1 or point.y == self.y + 1
	
	def getHitPoint(self, startPosition: Vector, direction: Vector) -> Vector | None:
		"""
		获取从start射出的射线direction会碰到方块表面位置，返回start点到该位置的向量
		:param startPosition: 起始点
		:param direction: 方向
		:returns: 如果start不经过direction，返回None
		"""
		if direction.x == 0 and direction.y == 0:
			return None
		start: Vector = startPosition.clone()
		relative: Vector = ((self.getVector() - start).add(0.5, 0.5))  # 起始点->方块中心
		dc: BlockVector = direction.directionalCloneBlock()
		if self.contains(start):
			result1 = result2 = None
			if dc.x != 0:
				result1 = direction.clone().extendX((0.5 if dc.x > 0 else -0.5) - relative.x)
				if -0.5 <= result1.y + relative.y <= 0.5:
					return result1
			if dc.y != 0:
				result2 = direction.clone().extendY((0.5 if dc.y > 0 else -0.5) - relative.y)
				if -0.5 <= result2.x + relative.x <= 0.5:
					return result2
			raise InvalidOperationException(f'不应当运行到此处，请检查代码问题。{self = } {start = }, {direction = }, {relative = }, {dc = }, {result1 = }, {result2 = }')
		else:
			result = direction.clone()
			if dc.y == -1:
				if relative.y > 0.51:
					return None
				result.extendY(relative.y + 0.5)
				rdc = result.directionalCloneBlock()
				if -0.5 <= relative.x - result.x <= 0.5 and (rdc.x == rdc.y == 0 or rdc == dc):
					return result
			elif dc.y == 1:
				if relative.y < -0.51:
					return None
				result.extendY(relative.y - 0.5)
				rdc = result.directionalCloneBlock()
				if -0.5 <= relative.x - result.x <= 0.5 and (rdc.x == rdc.y == 0 or rdc == dc):
					return result
			result = direction.clone()
			if dc.x == -1:
				if relative.x > 0.51:
					return None
				result.extendX(relative.x + 0.5)
				rdc = result.directionalCloneBlock()
				if -0.5 <= relative.y - result.y <= 0.5 and (rdc.x == rdc.y == 0 or rdc == dc):
					return result
			elif dc.x == 1:
				if relative.x < -0.51:
					return None
				result.extendX(relative.x - 0.5)
				rdc = result.directionalCloneBlock()
				if -0.5 <= relative.y - result.y <= 0.5 and (rdc.x == rdc.y == 0 or rdc == dc):
					return result
			return None
	
	def getRelativeBlock(self, position: Vector, direction: Vector) -> Union[list[tuple['BlockVector', Vector]], 'BlockVector', None]:
		"""
		获取方块角落上某一点向某一个方向移动的相关方块位置，主要用于移动撞边判断。如果direction不平行于边界，可能返回两个BlockVector和Vector元组。
		元组中，后者Vector指示如果BlockVector是canPass，折速度向量结果
		:param position: 某个角落
		:param direction: 某个方向
		:return: 相关方块位置。如果目标点不在角落，返回撞边的方向，例如撞右边返回(1, 0)；如果方向无关、不影响移动，返回空列表
		"""
		if utils.fequal(self.x, position.x):
			left = True
			if utils.fequal(self.y, position.y):
				up = True
			elif utils.fequal(self.y + 1, position.y):
				up = False
			else:
				return BlockVector(-1, 0)  # 撞左边
		elif utils.fequal(self.x + 1, position.x):
			left = False
			if utils.fequal(self.y, position.y):
				up = True
			elif utils.fequal(self.y + 1, position.y):
				up = False
			else:
				return BlockVector(1, 0)  # 撞右边
		else:
			if utils.fequal(self.y, position.y):
				return BlockVector(0, -1)  # 撞上边
			elif utils.fequal(self.y + 1, position.y):
				return BlockVector(0, 1)  # 撞下边
			else:
				return None  # 接受触点在方块中间
		dcb = direction.clone().directionalCloneBlock()
		if dcb.x == 0:
			if (dcb.y == -1 and not up) or (dcb.y == 1 and up):
				return [(
					(BlockVector(self.x - 1, self.y) if left else BlockVector(self.x + 1, self.y)),
					direction.clone().setX(0)
				)]
		elif dcb.x == -1:
			if dcb.y == -1:
				if not up and not left:
					return [
						(BlockVector(self.x, self.y + 1), direction.clone().setY(0)),
						(BlockVector(self.x + 1, self.y), direction.clone().setX(0))
					]
			elif dcb.y == 1:
				if up and not left:
					return [(BlockVector(self.x, self.y - 1), direction.clone().setY(0)), (BlockVector(self.x + 1, self.y), direction.clone().setX(0))]
			elif dcb.y == 0:
				return [(BlockVector(self.x, self.y - 1) if up else BlockVector(self.x, self.y + 1), direction.clone().setY(0))]
		elif dcb.x == 1:
			if dcb.y == -1:
				if not up and left:
					return [(BlockVector(self.x - 1, self.y), direction.clone().setX(0)), (BlockVector(self.x, self.y + 1), direction.clone().setY(0))]
			elif dcb.y == 1:
				if up and left:
					return [(BlockVector(self.x - 1, self.y), direction.clone().setX(0)), (BlockVector(self.x, self.y - 1), direction.clone().setY(0))]
			elif dcb.y == 0:
				return [(BlockVector(self.x, self.y - 1) if up else BlockVector(self.x, self.y + 1), direction.clone().setY(0))]
		return []
	
	def save(self) -> dict:
		return {
			'x': self.x,
			'y': self.y
		}
	
	@classmethod
	def load(cls, d: dict) -> 'BlockVector':
		return BlockVector(int(d['x']), int(d['y']))
	
	def __len__(self) -> float:
		return float(self.x ** 2 + self.y ** 2) ** 0.5
	
	def __add__(self, other: 'BlockVector') -> 'BlockVector':
		return BlockVector(self.x + other.x, self.y + other.y)
	
	def __sub__(self, other: 'BlockVector') -> 'BlockVector':
		return BlockVector(self.x - other.x, self.y - other.y)
	
	def __mul__(self, val: int | float) -> 'BlockVector':
		return BlockVector(self.x * val, self.y * val)
	
	def __rmul__(self, val: int | float) -> 'BlockVector':
		return BlockVector(self.x * val, self.y * val)
	
	def __truediv__(self, other: int | float) -> 'BlockVector':
		return BlockVector(int(self.x / other), int(self.y / other))
	
	def __eq__(self, other: 'BlockVector') -> bool:
		return self.x == other.x and self.y == other.y
	
	def __str__(self) -> str:
		return f'Block({self.x}, {self.y})'
	
	def __repr__(self) -> str:
		return f'Block({self.x}, {self.y})'
	
	def __hash__(self) -> int:
		return (self.x << 16) | (self.y if self.y >= 0 else ((self.y - 1) & 0xffff))
