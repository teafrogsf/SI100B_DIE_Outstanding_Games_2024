from random import Random
from typing import List, Dict

import LLA.chat_with_ai as ai
from render.egg_generate import generateEgg
from utils.util import utils
from window.input import asyncTasks


def asyncEgg(keywords: list[str], random: Random):
	asyncTasks.create_task(getProperties(keywords, random))


async def getProperties(keywords: List[str], random: Random):
	msg = [
		{
			"role": "user",
			"content":
				f"You have the styles with its serial number: "
				f"1: butterfly bow, 2: C, 3: first placem or champion, 4: flower, 5: heart, 6: leaves, 7: music; 8 rune, 9: pythonic, 10: rabbit, 11: second place or runner-up"
				f"and you have the keywords: "
				f"{keywords}. "
				f"Decide what styles match the keywords. "
				f"You can choose more than one styles. "
				f"Only reply me the serial numbers, divide them with a single space, in the first line. "
				f"Only reply me the color you think is proper for the styles, one-to-one correspondent with the first line, in t he form of #RRGGBB, divide them with a single space, in the second line."
				f"And finally, reply me the color you think is proper for the egg itself, in the form of #RRGGBB, in the third line."
		}
	]
	new = None
	new2 = None
	egg = None
	while True:
		response = ai.client.chat.completions.create(
			model="llama3.2",
			messages=msg  # a list of dictionary contains all chat dictionary
		)
		content = response.choices[0].message.content
		lst = content.split('\n')
		if len(lst) < 3:
			continue
		lst, clr, egg = lst[0].split(' '), lst[1].split(' '), lst[2].strip()
		try:
			egg = int(egg[1:], 16)
		except Exception as e:
			utils.printException(e)
			continue
		new = []
		new2 = []
		for i in lst:
			try:
				j = i.strip()
				if len(j) == 0:
					continue
				j = int(j)
				new.append(j)
				assert 0 < j < 12
			except Exception as e:
				utils.printException(e)
				break
		else:
			for i in clr:
				try:
					j = i.strip()
					if len(j) < 2:
						continue
					new2.append(int(j[1:], 16))
				except Exception as e:
					utils.printException(e)
					break
			else:
				if len(new) == len(new2):
					break
	properties = new, new2, egg
	utils.info(properties)
	generateEgg(new, new2, egg, random)
