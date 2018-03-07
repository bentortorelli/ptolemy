from PIL import Image, ImageDraw, ImageFont, ImageColor
from cartography.direction import Direction
import math

class Hex:
	def __init__(self, map, coords, x=-1, y=-1, hex_color = "white", text_color = "red"):
		point_one = coords[0]
		point_two = coords[1]
		point_four = coords[3]
		
		self.map = map
		self.coords = coords
		self.center = [int((point_one[0]+point_four[0])/2), int((point_one[1]+point_four[1])/2)]
		self.edge_length = int(math.sqrt(math.pow(point_two[0] - point_one[0], 2) + math.pow(point_two[1] - point_one[1], 2)))
		self.positon = (x,y)
		self._hex_color = hex_color
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
		font_size = 1
		center_top_pos = (self.coords[0][0]+int(self.edge_length/2), self.coords[0][1])
		self.font = ImageFont.truetype("arial.ttf", font_size)
		while self.font.getsize(self.text)[0] <= self.edge_length/2:
			font_size += 1
			self.font = ImageFont.truetype("arial.ttf", font_size)
			self.text_position = (center_top_pos[0] - int(self.font.getsize(self.text)[0]/2), center_top_pos[1])

	@property
	def hex_color(self):
		return self._hex_color

	@hex_color.setter
	def hex_color(self, color):
		ImageColor.getrgb(color)
		self._hex_color = color

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

	def getAdjacent(self, direction):
		if direction == Direction.SOUTH_WEST:
			if self._x % 2 == 0:
				return self.map.getHex((self._x-1, self._y))
			else:
				return self.map.getHex((self._x-1, self._y-1))
		elif direction == Direction.SOUTH:
			return self.map.getHex((self._x, self._y-1))
		elif direction == Direction.SOUTH_EAST:
			if self._x % 2 == 0:
				return self.map.getHex((self._x+1, self._y))
			else:
				return self.map.getHex((self._x+1, self._y-1))
		elif direction == Direction.WEST:
			return None
		elif direction == Direction.CENTER:
			return self
		elif direction == Direction.EAST:
			return None
		elif direction == Direction.NORTH_WEST:
			if self._x % 2 == 0:
				return self.map.getHex((self._x-1, self._y+1))
			else:
				return self.map.getHex((self._x-1, self._y))
		elif direction == Direction.NORTH:
			return self.map.getHex((self._x, self._y+1))
		elif direction == Direction.NORTH_EAST:
			if self._x % 2 == 0:
				return self.map.getHex((self._x+1, self._y+1))
			else:
				return self.map.getHex((self._x+1, self._y))
		else:
			return None
			
	def draw(self, image):
		ImageDraw.Draw(image).polygon(self.coords, outline = "black", fill = self.hex_color)
		ImageDraw.Draw(image).text(self.text_position, self.text, font = self.font, fill = self.text_color)

		token_positions = list()
		token_size = (self.edge_length, self.edge_length)

		if len(self.contents) <= 1:
			token_positions = [
				(self.center[0] - int(self.edge_length/2), self.center[1] - int(self.edge_length/2))]
		elif len(self.contents) == 2:
			token_positions = [
				(self.center[0] - int(self.edge_length/2), self.center[1] - int(self.edge_length/4)),
				(self.center[0], self.center[1] - int(self.edge_length/4))]
			token_size = (int(self.edge_length/2), int(self.edge_length/2))
		else:
			token_positions = [
				(self.center[0] - int(self.edge_length/2), self.center[1] - int(self.edge_length/2)),
				(self.center[0], self.center[1] - int(self.edge_length/2)),
				(self.center[0] - int(self.edge_length/2), self.center[1]),
				(self.center[0], self.center[1])]	
			token_size = (int(self.edge_length/2), int(self.edge_length/2))

		for token in self.contents:
			if token_positions:
				position = token_positions.pop(0)
				token.draw(image, position, token_size)
			else:
				break

		if len(self.contents) > 4:
			overflow_text = "..."
			dot_position = (self.center[0] - self.font.getsize(overflow_text)[0]/2, self.center[1] + int(self.edge_length)/4)
			ImageDraw.Draw(image).text(dot_position, overflow_text, font = self.font, fill = self.text_color)