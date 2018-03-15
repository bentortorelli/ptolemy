from PIL import Image, ImageDraw, ImageFont, ImageColor
from cartography.gridspace import GridSpace
from cartography.direction import Direction
import math

class Hex(GridSpace):
	def __init__(self, map, coords, x=-1, y=-1, color = "white", text_color = "red"):
		super().__init__(map, coords, x, y, color, text_color)
		point_one = coords[0]
		point_two = coords[1]
		point_four = coords[3]
		
		self.center = [int((point_one[0]+point_four[0])/2), int((point_one[1]+point_four[1])/2)]
		self.edge_length = int(math.sqrt(math.pow(point_two[0] - point_one[0], 2) + math.pow(point_two[1] - point_one[1], 2)))

	def calculate_font_size(self, text):
		font_size = 1
		center_top_pos = (self.coords[0][0]+int(self.edge_length/2), self.coords[0][1])
		self.font = ImageFont.truetype("arial.ttf", font_size)
		while self.font.getsize(self.text)[0] <= self.edge_length/2:
			font_size += 1
			self.font = ImageFont.truetype("arial.ttf", font_size)
			self.text_position = (center_top_pos[0] - int(self.font.getsize(self.text)[0]/2), center_top_pos[1])

	def get_adjacent(self, direction):
		if direction == Direction.SOUTH_WEST:
			if self._x % 2 == 0:
				return self.map.get_space((self._x-1, self._y))
			else:
				return self.map.get_space((self._x-1, self._y-1))
		elif direction == Direction.SOUTH:
			return self.map.get_space((self._x, self._y-1))
		elif direction == Direction.SOUTH_EAST:
			if self._x % 2 == 0:
				return self.map.get_space((self._x+1, self._y))
			else:
				return self.map.get_space((self._x+1, self._y-1))
		elif direction == Direction.WEST:
			return None
		elif direction == Direction.CENTER:
			return self
		elif direction == Direction.EAST:
			return None
		elif direction == Direction.NORTH_WEST:
			if self._x % 2 == 0:
				return self.map.get_space((self._x-1, self._y+1))
			else:
				return self.map.get_space((self._x-1, self._y))
		elif direction == Direction.NORTH:
			return self.map.get_space((self._x, self._y+1))
		elif direction == Direction.NORTH_EAST:
			if self._x % 2 == 0:
				return self.map.get_space((self._x+1, self._y+1))
			else:
				return self.map.get_space((self._x+1, self._y))
		else:
			return None
			
	def draw(self, image):
		super().draw(image)
		
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