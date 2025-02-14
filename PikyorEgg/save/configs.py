"""/
这个文件主要用于导出和导入设置。
"""
import json
import os
import types
from typing import Callable

from utils.util import utils


def readConfig() -> dict[str, any]:
	"""
	读取配置文件。！！！由于文件位置问题，只能在main.py中调用！！！
	"""
	if not os.path.exists("user"):
		os.makedirs("user")
	try:
		f = open("user/config.json", "r")
	except FileNotFoundError:
		f2 = open("user/config.json", "x")
		f2.write("{}")
		f2.close()
		return {}
	file: str = f.read()
	f.close()
	try:
		return json.loads(file)
	except Exception as e:
		utils.printException(e)
		return {}


def writeConfig(d: dict[str, any]) -> None:
	"""
	写入配置文件。！！！由于文件位置问题，只能在main.py中调用！！！
	"""
	with open("user/config.json", "w") as f:
		f.write(json.dumps(d))
		f.close()


def readElseDefault(dic: dict[str, any], key: str, else_: any, result_or_judgement: dict[any, any] | Callable[[any], any] | None, warningMessage: str | None = None) -> any:
	"""
	:param dic: config字典
	:param key: 要检查的key
	:param result_or_judgement: 可以是期待的result的字典；可以是函数，接受设置中的值，返回实际设置值，用于调整超限或不合法值；也可以是None
	:param else_: 如果dic中不存在key，或者dic[key]不存在于result字典中，返回else_。相当于默认值
	:param warningMessage: dic[key]不存在于result字典中时输出的消息。内部可以包含一个花括号，用于.format(设置中的值)
	:return: 实际设置值
	"""
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
