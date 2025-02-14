import pygame

from interact.status import Status, ScrollStatus
from utils.util import utils
from utils.vector import BlockVector


class Interact:
	def __init__(self):
		self.KEY_COUNT = 256
		self.mouse: BlockVector = BlockVector(0, 0)
		self.left: Status = Status('MouseLeft')
		self.middle: Status = Status('MouseMiddle')
		self.right: Status = Status('MouseRight')
		self.scroll: ScrollStatus = ScrollStatus()
		self.keys: list[Status | None] = [Status('ERROR_KEY')] * self.KEY_COUNT
		self.specialKeys: list[Status | None] = [self.keys[0]] * self.KEY_COUNT
		self.KEY_COUNT -= 1
		for i in pygame.__dict__:
			if not i.startswith('K_'):
				continue
			j = getattr(pygame, i)
			if j <= self.KEY_COUNT:
				self.keys[j] = Status(i[2:])
			else:
				self.specialKeys[j & self.KEY_COUNT] = Status(i[2:])
		del i, j
	
	def onKey(self, event) -> None:
		if event.type == pygame.KEYDOWN:
			if event.key <= self.KEY_COUNT:
				self.keys[event.key].set(True)
			else:
				self.specialKeys[event.key & self.KEY_COUNT].set(True)
		elif event.type == pygame.KEYUP:
			if event.key <= self.KEY_COUNT:
				self.keys[event.key].set(False)
			else:
				self.specialKeys[event.key & self.KEY_COUNT].set(False)
	
	def onMouse(self, event) -> None:
		if event.type == pygame.MOUSEMOTION:
			self.mouse.set(event.pos)
			# 此处交给main.py来修正鼠标位置不对的问题，根据renderer.getOffset()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				self.left.set(True)
			elif event.button == 2:
				self.middle.set(True)
			elif event.button == 3:
				self.right.set(True)
			elif event.button == 4:
				self.scroll.scroll(-1)
			elif event.button == 5:
				self.scroll.scroll(1)
			else:
				utils.warn(f'onMouse: unknown button {event.button}')
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:
				self.left.set(False)
			elif event.button == 2:
				self.middle.set(False)
			elif event.button == 3:
				self.right.set(False)
			elif event.button == 4:
				self.scroll.scroll(-1)
			elif event.button == 5:
				self.scroll.scroll(1)
			else:
				utils.warn(f'onMouse: unknown button {event.button}')


interact: Interact = Interact()
