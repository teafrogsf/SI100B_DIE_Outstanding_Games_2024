from utils.error import InvalidOperationException


class Status:
	def __init__(self, name: str):
		"""
		:param name: 监视状态的名称
		"""
		self.name = name
		self.isPressed: bool = False
		self.wasPressed: int = 0
		self._shouldDeal = False
	
	def set(self, status: bool) -> None:
		"""
		设置状态。应当仅在main.py的mainThread中调用。用于激活事件
		:param status: 设置为的值
		"""
		if status:
			self._shouldDeal = True
			self.wasPressed += 1
		self.isPressed = status
	
	def shouldDeal(self) -> bool:
		return self._shouldDeal
	
	def peek(self) -> int:
		"""
		需要处理时调用。
		:returns 如果需要处理，则返回True，但是不重置状态
		"""
		return self.isPressed
	
	def deals(self) -> bool:
		"""
		需要处理时调用。
		:returns 如果需要处理，则返回True，并且重置状态
		"""
		if self._shouldDeal:
			self._shouldDeal = False
			self.wasPressed = 0
			return self.isPressed
		else:
			return False
	
	def dealPressTimes(self) -> int:
		ret = self.wasPressed
		self.wasPressed = 0
		return ret
	
	def __str__(self) -> str:
		return f'{self.name}: {self.wasPressed}'


class ScrollStatus(Status):
	def __init__(self):
		super().__init__('MouseScroll')
		self._shouldDeal = 0
	
	def scroll(self, scr: int) -> None:
		"""
		向下为正
		"""
		self._shouldDeal += scr
	
	def peekScroll(self) -> int:
		"""
		需要处理时调用。
		:returns 如果需要处理，则返回True，但是不重置状态
		"""
		return self._shouldDeal
	
	def resetScroll(self) -> None:
		"""
		重置滚动量
		"""
		self._shouldDeal = 0
	
	def dealScroll(self) -> int:
		if self._shouldDeal != 0:
			ret = self._shouldDeal
			self._shouldDeal = 0
			return ret
		else:
			return 0
	
	def dealPressTimes(self) -> bool:
		raise InvalidOperationException('ScrollStatus.deal() should not be called')
	
	def peek(self) -> bool:
		raise InvalidOperationException('ScrollStatus.peek() should not be called')
	
	def set(self, status: bool) -> None:
		raise InvalidOperationException('ScrollStatus.set() should not be called')
	
	def __str__(self) -> str:
		return f'{self.name}: {self._shouldDeal}'
