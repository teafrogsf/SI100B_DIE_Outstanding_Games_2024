import time
import traceback
import types
from sys import stdout, stderr
from threading import Lock
from typing import Callable


class Utils:
	def __init__(self):
		self._lock = Lock()
		if self._lock.locked():
			self._lock.release()
		self.logLevel = 4
	
	@staticmethod
	def __copyFromConfigs(dic: dict[str, any], key: str, else_: any, result_or_judgement: dict[any, any] | Callable[[any], any] | None, warningMessage: str | None = None) -> any:
		"""此处代码应当抄写configs.py中的readElseDefault"""
		if key in dic:
			res = dic[key]
			if isinstance(result_or_judgement, dict):
				if res in result_or_judgement:
					return result_or_judgement[res]
				else:
					if warningMessage:
						utils.warn(warningMessage.format(res))
					return else_
			elif isinstance(result_or_judgement, types.FunctionType):
				return result_or_judgement(res)
			else:
				return else_
		else:
			return else_
	
	def readConfig(self, config: dict) -> None:
		self.logLevel = self.__copyFromConfigs(config, 'logLevel', 4, {'trace': 0, 'debug': 1, 'info': 2, 'warn': 3, 'error': 4}, 'Invalid log level: {}')
	
	def writeConfig(self) -> dict:
		match self.logLevel:
			case 0:
				return {'logLevel': 'trace'}
			case 1:
				return {'logLevel': 'debug'}
			case 2:
				return {'logLevel': 'info'}
			case 3:
				return {'logLevel': 'warn'}
			case _:
				return {'logLevel': 'error'}
	
	def _output(self, head: str, *args, sep=' ', end='\n', file=stdout):
		self._lock.acquire()
		print(head, sep='', end='', file=file)
		print(*args, sep=sep, end=end, file=file)
		self._lock.release()
	
	def trace(self, *args, sep=' ', end='\n') -> None:
		if self.logLevel > 0:
			return
		self._output('[IKUN] [TRACE] ', *args, sep=sep, end=end)
	
	def debug(self, *args, sep=' ', end='\n') -> None:
		if self.logLevel > 1:
			return
		self._output('[IKUN] [DEBUG] ', *args, sep=sep, end=end)
	
	def info(self, *args, sep=' ', end='\n') -> None:
		if self.logLevel > 2:
			return
		self._output('[IKUN] [INFO]  ', *args, sep=sep, end=end)
	
	def warn(self, *args, sep=' ', end='\n') -> None:
		if self.logLevel > 3:
			return
		self._output('[IKUN] [WARN]  ', *args, sep=sep, end=end, file=stderr)
	
	def error(self, *args, sep=' ', end='\n') -> None:
		if self.logLevel > 4:
			return
		self._output('[IKUN] [ERROR] ', *args, sep=sep, end=end, file=stderr)
	
	def traceStack(self, e: Exception, msg: str | None = None) -> None:
		"""
		建议改为调用printException()
		:param e: 被抛出的错误
		:param msg: 其他要输出的错误
		"""
		result = []
		last_file = None
		last_line = None
		last_name = None
		count = 0
		traces = traceback.extract_tb(e.__traceback__)
		result.append(f'  {traces[-1].line}\n')
		for frame in traces:
			if last_file is None or last_file != frame.filename or last_line is None or last_line != frame.lineno or last_name is None or last_name != frame.name:
				if count > 3:
					count -= 3
					result.append(f'  [Previous line repeated {count} more time{"s" if count > 1 else ""}]\n')
				last_file = frame.filename
				last_line = frame.lineno
				last_name = frame.name
				count = 0
			count += 1
			if count > 3:
				continue
			row = [f'  @ {frame.name} @ File "{frame.filename}", line {frame.lineno}']
			if frame.locals:
				for name, value in sorted(frame.locals.items()):
					row.append(f'    {name} = {value}')
			row.append('\n')
			result.append(''.join(row))
		if count > 3:
			count -= 3
			result.append(f'  [Previous line repeated {count} more time{"s" if count > 1 else ""}]\n')
		self._lock.acquire()
		if msg is not None:
			print(f'[IKUN] [ERROR] {msg}', file=stderr)
		else:
			print('[IKUN] [WARN]  Stack trace:', file=stderr)
		for line in result:
			print(line, file=stderr, end='')
		self._lock.release()
	
	def printException(self, e: Exception) -> None:
		"""
		抛出错误时调用
		:param e: 被抛出的错误
		"""
		self.traceStack(e, f'[{type(e).__name__}] {str(e)}!! when running code:')
	
	@staticmethod
	def fequal(a: float, b: float) -> bool:
		return abs(a - b) < 1e-9
	
	@staticmethod
	def fless(a: float, b: float) -> bool:
		return a < b and not Utils.fequal(a, b)
	
	@staticmethod
	def fgreater(a: float, b: float) -> bool:
		return a > b and not Utils.fequal(a, b)
	
	@staticmethod
	def flesseq(a: float, b: float) -> bool:
		return not Utils.fgreater(a, b)
	
	@staticmethod
	def fgreatereq(a: float, b: float) -> bool:
		return not Utils.fless(a, b)
	
	def frange(self, value: float, start: float, end: float) -> float:
		if self.flesseq(value, start):
			return start
		elif self.fgreatereq(value, end):
			return end
		else:
			return value


utils: Utils = Utils()


def prints(func):
	def wrapper(*args, **kwargs):
		s = f'args: {args}, kwargs: {kwargs}'
		ret = func(*args, **kwargs)
		utils.trace(s + f', ret = {ret}')
		return ret
	
	return wrapper


def times(func):
	def wrapper(*args, **kwargs):
		ns = time.perf_counter_ns()
		ret = func(*args, **kwargs)
		utils.trace(f'{type(args[0]).__name__}.{func.__name__} takes {(time.perf_counter_ns() - ns) / 1e6} ms')
		return ret
	return wrapper
