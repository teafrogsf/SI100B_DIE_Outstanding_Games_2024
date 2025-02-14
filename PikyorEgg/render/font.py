import pygame.font
from pygame import Surface

from utils.util import utils, times

fontHeight: int = 30


class Font:
	def __init__(self, file: str, yOffset: int = 0, halfSize: bool = False):
		self._half: bool = halfSize
		self._addr: str = file
		self._yOffset: float = yOffset
		try:
			self._file = open(file, 'rb')
			if self._half:
				self._font = pygame.font.Font(self._file, fontHeight >> 1)
			else:
				self._font = pygame.font.Font(self._file, fontHeight)
		except Exception as e:
			utils.printException(e)
		if self._half:
			self._scaledOffset: int = int(yOffset * self._font.get_height() * 0.005)
		else:
			self._scaledOffset: int = int(yOffset * self._font.get_height() * 0.01)
	
	def close(self) -> None:
		self._file.close()
	
	def get(self, bold: bool, italic: bool, underline: bool, strikeThrough: bool) -> pygame.font.Font:
		self._font.set_bold(bold)
		self._font.set_italic(italic)
		self._font.set_underline(underline)
		self._font.set_strikethrough(strikeThrough)
		return self._font
	
	def draw(self, screen: Surface, string: str, x: int, y: int, color: int, bold: bool, italic: bool, underline: bool, strikeThrough: bool, background: int) -> int:
		if string is None:
			return 0
		if (color & 0xffffff) != (background & 0xffffff):
			bg = ((background >> 16) & 0xff, (background >> 8) & 0xff, background & 0xff)
			surface: Surface = self.get(bold, italic, underline, strikeThrough).render(string, True, ((color >> 16) & 0xff, (color >> 8) & 0xff, color & 0xff), bg)
			surface.set_colorkey(bg)
			surface.set_alpha(color >> 24)
			if background & 0xff000000 != 0:
				bgs = Surface(surface.get_size())
				bgs.fill(bg)
				bgs.set_alpha(background >> 24)
				screen.blit(bgs, (x, y - self._scaledOffset))
		else:
			bg1 = ((background >> 16) & 0xff, (background >> 8) & 0xff, background & 0xff)
			bg = [(background >> 16) & 0xff, (background >> 8) & 0xff, background & 0xff]
			if bg[0] < 128:
				bg[0] += 60
			else:
				bg[0] -= 60
			if bg[1] < 128:
				bg[1] += 60
			else:
				bg[1] -= 60
			if bg[2] < 128:
				bg[2] += 60
			else:
				bg[2] -= 60
			bg = (bg[0], bg[1], bg[2])
			surface: Surface = self.get(bold, italic, underline, strikeThrough).render(string, True, ((color >> 16) & 0xff, (color >> 8) & 0xff, color & 0xff), bg)
			surface.set_colorkey(bg)
			surface.set_alpha(color >> 24)
			if background & 0xff000000 != 0:
				bgs = Surface(surface.get_size())
				bgs.fill(bg1)
				bgs.set_alpha(background >> 24)
				screen.blit(bgs, (x, y - self._scaledOffset))
		screen.blit(surface, (x, y - self._scaledOffset))
		return surface.get_width()
	
	def setHeight(self, h: int) -> None:
		self._file.close()
		self._file = open(self._addr, 'rb')
		if self._half:
			self._font = pygame.font.Font(self._file, h >> 1)
			self._scaledOffset = int(self._yOffset * h * 0.005)
		else:
			self._font = pygame.font.Font(self._file, h)
			self._scaledOffset = int(self._yOffset * h * 0.01)


allFonts: dict[int, Font] = {}
realFontHeight: int = 0
realHalfHeight: int = 0


def setScale(scale: float) -> None:
	global fontHeight, realFontHeight, realHalfHeight
	fontHeight = int(scale)
	for i, f in allFonts.items():
		f.setHeight(fontHeight)
	realFontHeight = allFonts[0].get(False, False, False, False).get_height()
	realHalfHeight = allFonts[10].get(False, False, False, False).get_height()


def initializeFont() -> None:
	global realFontHeight
	global realHalfHeight
	allFonts[0] = Font('./assets/font/stsong.ttf', 5)
	allFonts[1] = Font('./assets/font/sword_art_online.ttf', -13)
	allFonts[2] = Font('./assets/font/yumindb.ttf', 2)
	allFonts[10] = Font('./assets/font/stsong.ttf', 5, True)
	allFonts[11] = Font('./assets/font/sword_art_online.ttf', -13, True)
	allFonts[12] = Font('./assets/font/yumindb.ttf', 2, True)
	realFontHeight = allFonts[0].get(False, False, False, False).get_height()
	realHalfHeight = allFonts[10].get(False, False, False, False).get_height()


def finalize() -> None:
	for f in allFonts.values():
		f.close()
