from random import Random

import pygame
from pygame import Surface

from render.renderer import renderer
from render.resource import resourceManager

base = resourceManager.getOrNew("egg/base")
base.adaptsMap(False)
butterfly = resourceManager.getOrNew("egg/butter")
butterfly.adaptsMap(False)
cc = resourceManager.getOrNew("egg/CC")
cc.adaptsMap(False)
first = resourceManager.getOrNew("egg/first")
first.adaptsMap(False)
flower = resourceManager.getOrNew("egg/flower")
flower.adaptsMap(False)
heart = resourceManager.getOrNew("egg/heart")
heart.adaptsMap(False)
leaves = resourceManager.getOrNew("egg/leaves'")
leaves.adaptsMap(False)
music = [
	resourceManager.getOrNew("egg/music"),
	resourceManager.getOrNew("egg/music2")
]
for t in music:
	t.adaptsMap(False)
runes = [
	resourceManager.getOrNew("egg/o1"),
	resourceManager.getOrNew("egg/o2"),
	resourceManager.getOrNew("egg/o3"),
	resourceManager.getOrNew("egg/o4"),
	resourceManager.getOrNew("egg/o5"),
	resourceManager.getOrNew("egg/o6"),
	resourceManager.getOrNew("egg/o7"),
	resourceManager.getOrNew("egg/o8"),
]
for t in runes:
	t.adaptsMap(False)
python = resourceManager.getOrNew("egg/python")
python.adaptsMap(False)
python.getSurface().set_colorkey((0, 0, 0))
rabbit = resourceManager.getOrNew("egg/rabbit")
rabbit.adaptsMap(False)
second = resourceManager.getOrNew("egg/second")
second.adaptsMap(False)
styles = [
	base,  # 0.0      0
	butterfly,  # 3.3 1
	cc,  # 1.6        2
	first,  # 1.2     3
	flower,  # 2.1    4
	heart,  # 1.5     5
	leaves,  # 3.2    6
	music,  # 2.2     7
	runes,  # 1.4     8
	python,  # 1.3    9
	rabbit,  # 3.1    10
	second,  # 1.1    11
]
base = 0
butterfly = 1
cc = 2
first = 3
flower = 4
heart = 5
leaves = 6
music = 7
runes = 8
python = 9
rabbit = 10
second = 11
del t


def copySurface(src: Surface, color: int):
	sfc = Surface(src.get_size(), flags=pygame.SRCALPHA)
	cr, cg, cb = (color >> 16) & 0xff, (color >> 8) & 0xff, color & 0xff
	for i in range(sfc.get_width()):
		for j in range(sfc.get_height()):
			r, g, b, a = src.get_at((i, j))
			sfc.set_at((i, j), (cr, cg, cb, r))
	return sfc


def __check(lst: list[int], i: int, d: int) -> bool:
	for j in lst:
		if abs(i - j) < d:
			return True
	return False


eggGenerated: Surface | None = None


def generateEgg(style: list[int], colors: list[int], egg: int, random: Random):
	sfc: Surface = copySurface(styles[base].getSurface(), egg)
	lst = []
	if runes in style:
		for i in random.sample(styles[runes], random.randint(4, 8)):
			y = random.randint(12, 43)
			x = random.randint(30 - abs(y - 27), abs(y - 27) + 30)
			sfc.blit(copySurface(i.getSurface(), colors[style.index(runes)]), (x, y))
	if second in style:
		y = random.randint(15, 40)
		while __check(lst, y, 2):
			y = random.randint(15, 40)
		lst.append(y)
		sub = copySurface(styles[second].getSurface(), colors[style.index(second)])
		sfc.blit(sub, (28, y))
	if first in style:
		y = random.randint(15, 40)
		while __check(lst, y, 2):
			y = random.randint(15, 40)
		lst.append(y)
		sub = copySurface(styles[first].getSurface(), colors[style.index(first)])
		sfc.blit(sub, (28, y))
	if python in style:
		y = random.randint(15, 40)
		while __check(lst, y, 3):
			y = random.randint(15, 40)
		lst.append(y)
		sfc.blit(styles[python].getSurface(), (28, y))
	if heart in style:
		y = random.randint(15, 40)
		while __check(lst, y, 3):
			y = random.randint(15, 40)
		lst.append(y)
		sfc.blit(copySurface(styles[heart].getSurface(), colors[style.index(heart)]), (random.randint(28 - abs(y - 27), 28 + abs(y - 27)), y))
	if cc in style:
		y = random.randint(15, 40)
		while __check(lst, y, 3):
			y = random.randint(15, 40)
		lst.append(y)
		sfc.blit(copySurface(styles[cc].getSurface(), colors[style.index(cc)]), (random.randint(29 - abs(y - 27), 29 + abs(y - 27)), y))
	if flower in style:
		y = random.randint(15, 40)
		x = random.randint(-abs(y - 27), abs(y - 27)) + 28
		sfc.blit(copySurface(styles[flower].getSurface(), colors[style.index(flower)]), (x, y))
	if music in style:
		for i in random.sample(styles[music], 1 if random.random() < 0.5 else 2):
			y = random.randint(10, 40)
			x = random.randint(10, 40)
			sfc.blit(copySurface(i.getSurface(), colors[style.index(music)]), (x, y))
	if rabbit in style:
		y = random.randint(15, 40)
		while __check(lst, y, 3):
			y = random.randint(25, 35)
		lst.append(y)
		sfc.blit(copySurface(styles[rabbit].getSurface(), colors[style.index(rabbit)]), (26, y))
	if leaves in style:
		sfc.blit(copySurface(styles[leaves].getSurface(), colors[style.index(leaves)]), (27, 0))
	if butterfly in style:
		y = random.randint(15, 40)
		while __check(lst, y, 3):
			y = random.randint(15, 40)
		lst.append(y)
		sfc.blit(copySurface(styles[butterfly].getSurface(), colors[style.index(butterfly)]), (27, y))
	global eggGenerated
	eggGenerated = sfc
