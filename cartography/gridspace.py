from abc import ABC, abstractmethod
from PIL import Image, ImageDraw, ImageFont, ImageColor
from cartography.direction import Direction
import math

class GridSpace(ABC):
	def __init__(self, map, coords, x=-1, y=-1, color = "white", text_color = "red"):
		self.map = map
		self.coords = coords
		self.center = None
		self.edge_length = None
		self.positon = (x,y)
		self._color = color
		self._text_color = text_color
		self.contents = list()

	@property
	def position(self):
		return (self._x, self._y)

	@position.setter
	def position(self, pos):
		self._x = pos[0]
		self._y = pos[1]
		self.text = (str(self._x) + ", " + str(self._y))
	
	@property
	def text(self):
		return self._text
	
	@text.setter
	def text(self, text):
		self._text = text
		self.calculate_font_size(text)

	@abstractmethod
	def calculate_font_size(self, text):
		pass

	@property
	def color(self):
		return self._color

	@color.setter
	def color(self, color):
		ImageColor.getrgb(color)
		self._color = color

	@property
	def text_color(self):
		return self._text_color

	@text_color.setter
	def text_color(self, color):
		ImageColor.getrgb(color)
		self._text_color = color
	
	def __lt__(self, other):
		if self.center[0] < other.center[0]:
			return True
		elif self.center[0] == other.center[0] and self.center[1] > other.center[1]:
			return True
		else:
			return False

	@abstractmethod
	def get_adjacent(self, direction):
		pass
	
	@abstractmethod	
	def draw(self, image):
		pass