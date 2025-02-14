from copy import deepcopy
from queue import Queue
from typing import TypeVar, Deque, Generic

_SyncT = TypeVar('_SyncT')


class SynchronizedStorage(Generic[_SyncT]):
	"""
	用于多线程异步设置值。在set线程期望的时候设置值，在use线程期望的时候应用新值
	"""
	
	def __init__(self, value: _SyncT):
		self._value: _SyncT = value
		self._newValue: _SyncT = deepcopy(value)
	
	def get(self) -> _SyncT:
		return self._value
	
	def getNew(self) -> _SyncT:
		return self._newValue
	
	def set(self, value: _SyncT) -> None:
		self._newValue = value
	
	def apply(self, value: _SyncT) -> None:
		self._value = self._newValue
		self._newValue = value


class SynchronizedModifier(Generic[_SyncT]):
	"""
	用于多线程异步设置值。在set线程期望的时候设置值，在use线程期望的时候应用变化
	"""
	
	def __init__(self, value: _SyncT):
		self._value: list = value
		self._queue: Deque[callable] = Deque[callable]()
	
	def modify(self, modifier: callable) -> None:
		self._queue.append(modifier)
	
	def apply(self) -> None:
		q = self._queue
		self._queue = Queue[callable]
		for modifier in q:
			modifier(self._value)


class Boolean:
	def __init__(self, value: bool):
		self._value: bool = value
	
	def set(self, value: bool) -> None:
		self._value = value
	
	def toggle(self) -> None:
		self._value = not self._value
	
	def get(self) -> bool:
		return self._value
	
	def __bool__(self) -> bool:
		return self._value
	
	def __eq__(self, other: bool) -> bool:
		return self._value == other
	
	def __ne__(self, other: bool) -> bool:
		return self._value != other
	
	def __str__(self) -> str:
		return 'true' if self._value else 'false'
	
	def __repr__(self) -> str:
		return f'Boolean({self._value})'
