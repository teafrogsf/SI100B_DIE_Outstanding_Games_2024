from collections import deque

import pygame.draw
from pygame import Surface

from render.renderable import Renderable
from render.renderer import renderer, Location
from utils.game import game
from utils.text import RenderableString
from utils.vector import BlockVector


class Hud(Renderable):
	def __init__(self):
		super().__init__(None)
		self.displayHealth: float = 1.0
		self.lastDisplayHealth: float = 0.0
		self.displayHunger: float = 1.0
		self.lastDisplayHunger: float = 0.0
		self.defaultLength: float = 0.25
		self.messages: deque[tuple[int, RenderableString]] = deque()
	
	def sendMessage(self, message: RenderableString) -> None:
		self.messages.append((game.tickCount, message))
		while len(self.messages) > 6:
			self.messages.popleft()
	
	def render(self, delta: float) -> None:
		if game.getWorld() is None:
			return
		player = game.getWorld().getPlayer()
		if player is None:
			return
		self.displayHealth = player.getHealth() / player.getMaxHealth()
		self.displayHunger = player.growth_value / 100
		
		w, h = renderer.getSize().getTuple()
		margin = h >> 6
		from render import font
		barLeft = font.allFonts[11].get(False, False, False, False).size(player.name)[0] + margin + margin  # 加玩家名显示
		barLength = int(w * self.defaultLength)
		sw, sh = (barLength + barLeft, margin * 3)
		barHeight = margin
		surface: Surface = Surface((sw, sh))
		surface.set_colorkey((0, 0, 0))
		surface.set_alpha(0xcc)
		pygame.draw.polygon(surface, (0xff, 0xff, 0xff), [(0, 0), (sw, 0), (sw - (sh >> 1), sh), (0, sh)])
		barBackgroundX = (barHeight - 1)
		up = sw - barBackgroundX - (barHeight >> 1)
		down = sw - barBackgroundX - barHeight
		pygame.draw.polygon(surface, (1, 1, 1), [(barLeft - 1, barBackgroundX), (up, barBackgroundX), (down, subBarY := (sh - barBackgroundX)), (barLeft - 1, subBarY)])  # 背景黑条
		renderer.getCanvas().blit(surface, (margin, margin))
		surface.fill((0, 0, 0))
		surface.set_alpha(0xff)
		up -= 1 + barLeft
		down -= 1 + barLeft
		
		upNow = barLeft + up * self.displayHealth
		downNow = barLeft + down * self.displayHealth
		if self.displayHealth != 0:
			pygame.draw.polygon(surface, (0x70, 0xb0, 0x10), [
				(barLeft, barHeight),
				(upNow, barHeight),
				(downNow, barHeight << 1),
				(barLeft, barHeight << 1)
			])
		valueDelta = self.lastDisplayHealth - self.displayHealth
		if valueDelta < 0:  # 有回血
			valueDelta = -valueDelta
			pygame.draw.polygon(surface, (0x33, 0x88, 0xff), [
				(upNow, barHeight),
				(barLeft + up * self.lastDisplayHealth, barHeight),
				(barLeft + down * self.lastDisplayHealth, barHeight << 1),
				(downNow, barHeight << 1)
			])
			if valueDelta <= 0.002:
				self.lastDisplayHealth = self.displayHealth
			else:
				self.lastDisplayHealth += 0.002 + valueDelta * 0.01
		elif valueDelta > 0:  # 有扣血
			pygame.draw.polygon(surface, (0xff, 0x33, 0x33), [
				(upNow, barHeight),
				(barLeft + up * self.lastDisplayHealth, barHeight),
				(barLeft + down * self.lastDisplayHealth, barHeight << 1),
				(downNow, barHeight << 1)
			])
			if valueDelta <= 0.002:
				self.lastDisplayHealth = self.displayHealth
			else:
				self.lastDisplayHealth -= 0.002 + valueDelta * 0.01
		
		upStart = barLeft + (up >> 1) - (barHeight >> 2)
		upEnd = barLeft + up - (barHeight >> 2)
		downStart = barLeft + (down >> 1)
		upNow = upStart + (up - (barHeight >> 2) + 1 >> 1) * self.displayHunger
		downNow = downStart + (down + 1 >> 1) * self.displayHunger
		subBarY = margin + (barHeight >> 1)
		pygame.draw.polygon(surface, (1, 1, 1), [
			(upEnd + 1, subBarY - 1),
			(upStart - 1, subBarY - 1),
			(downStart - 1, barHeight << 1),
			(barLeft + down + 1, barHeight << 1)
		])
		if self.displayHunger != 0:
			pygame.draw.polygon(surface, (0xc0, 0xb0, 0x10), [
				(upNow, subBarY),
				(upStart, subBarY),
				(downStart, barHeight << 1),
				(downNow, barHeight << 1)
			])
		valueDelta = self.lastDisplayHunger - self.displayHunger
		if valueDelta < 0:  # 有回血
			valueDelta = -valueDelta
			pygame.draw.polygon(surface, (0xf0, 0xf0, 0x60), [
				(upNow, subBarY),
				(upStart + (up - (barHeight >> 2) + 1 >> 1) * self.lastDisplayHunger, subBarY),
				(downStart + (down + 1 >> 1) * self.lastDisplayHunger, barHeight << 1),
				(downNow, barHeight << 1)
			])
			if valueDelta <= 0.002:
				self.lastDisplayHunger = self.displayHunger
			else:
				self.lastDisplayHunger += 0.002 + valueDelta * 0.01
		elif valueDelta > 0:  # 有扣血
			pygame.draw.polygon(surface, (0xee, 0, 0), [
				(upNow, subBarY),
				(upStart + (up - (barHeight >> 2) + 1 >> 1) * self.lastDisplayHunger, subBarY),
				(downStart + (down + 1 >> 1) * self.lastDisplayHunger, barHeight << 1),
				(downNow, barHeight << 1)
			])
			if valueDelta <= 0.002:
				self.lastDisplayHunger = self.displayHunger
			else:
				self.lastDisplayHunger -= 0.002 + valueDelta * 0.01
		renderer.getCanvas().blit(surface, (margin, margin))
		
		renderer.renderString(RenderableString('\\11' + player.name), margin << 1, margin + (sh >> 1), 0xff000000, Location.LEFT)
		
		pos: BlockVector = BlockVector(margin, margin << 2)
		for s in player.skills.values():
			pos.x += s.render(delta, pos)
		pos.x = margin
		pos.y += renderer.getSystemScale() * 0.4
		for s in player.activeSkills:
			pos.x += s.render(delta, pos, player.skillSelecting, True)
		
		while len(self.messages) != 0 and game.tickCount - self.messages[0][0] > 120:
			self.messages.popleft()
		yMessage = h >> 3
		xCenter = w >> 1
		for tick, message in self.messages.copy():
			renderer.renderString(message, xCenter, yMessage, 0xff000000, Location.TOP, 0xccffffff, -1)
			yMessage += font.realHalfHeight
