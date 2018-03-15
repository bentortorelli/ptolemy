from PIL import Image, ImageDraw, ImageFont
from cartography.hex import Hex
from cartography.square import Square
from cartography.token import Token
from specktre import tilings
import math
	
class Map:
	def __init__(self, width, height, edge_length, type = "square", background_color = "white", background_image = None):
		self.edge_length = edge_length
		self.map_color = "white" #error check map color
		self.spaces = dict()
		self.last_move = None
		self.tokens = dict()
		self.background_color = background_color
		self.background_image = background_image

		space_list = None
		if type == "square":
			space_list = self.generate_square_map(width, height)
		elif type == "hex":
			space_list = self.generate_hex_map(width, height)
		else:
			raise ValueError(f"Unknown map type '{type}' specified.")

		space_list.sort()
		space_x = 0
		space_y = 0
		prev_y = self.image_height
		for space in space_list:
			if(space.center[1] >= prev_y):
				space_x += 1
				space_y = 0
			space.position = (space_x, space_y)
			space_y += 1
			prev_y = space.center[1]
			self.spaces[space.position] = space
		

	def generate_hex_map(self, width, height):
		short_diagnol = int(math.sqrt(3)*self.edge_length)
		long_diagnol = int(2*self.edge_length)

		dif = int((long_diagnol - self.edge_length)/2)
		self.image_width = long_diagnol + int((long_diagnol-dif)*(width-1))
		self.image_height = (short_diagnol+1)*height

		coordinates= None
		coordinates = tilings.generate_hexagons(self.image_width, self.image_height, self.edge_length)
		space_list = list()
		for coords in coordinates:
			for x,y in coords:
				valid = True
				if x < 0 or y < 0 or x > self.image_width or y > self.image_height:
					valid = False
					break
			if valid:
				new_hex = Hex(self, coords)
				space_list.append(new_hex)
		return space_list

	def generate_square_map(self, width, height):
		self.image_width = self.edge_length * width
		self.image_height = self.edge_length * height

		coordinates= None
		coordinates = tilings.generate_squares(self.image_width, self.image_height, self.edge_length)
		space_list = list()
		for coords in coordinates:
			for x,y in coords:
				valid = True
				if x < 0 or y < 0 or x > self.image_width or y > self.image_height:
					valid = False
					break
			if valid:
				new_hex = Square(self, coords)
				space_list.append(new_hex)
		return space_list
				

	def draw_map(self, file_path, draw_move=False):
		# Create a base map image
		im = None
		if self.background_image is None:
			im = Image.new("RGBA", (self.image_width, self.image_height), color = self.background_color)
		else:
			im = self.background_image.resize((self.image_width, self.image_height), Image.LANCZOS)

		# Draw each space
		for pos, space in self.spaces.items():
			space.draw(im)

		# If draw_move flag is set, draw a red line between the old and new positions
		if draw_move:
			line_coords = (self.last_move[0].center[0], self.last_move[0].center[1], self.last_move[1].center[0], self.last_move[1].center[1])
			ImageDraw.Draw(im).line(line_coords, width=10, fill = "red")

		# Save the image to disk
		im.save(file_path)

	def get_space(self, pos):
		try:
			return self.spaces[pos]
		except KeyError:
			return None

	def paint_space(self, position, color, text_color):
		space = self.get_space(position)
		space.color = color
		space.text_color = text_color


	def add_token(self, name, position, image, image_url):
		if name not in self.tokens:
			t = Token(name, position, image, image_url)
			self.tokens[name.lower()] = t
		else:
			raise ValueError("Token name already exists on this map.")

	def delete_token(self, name):
		if name in self.tokens:
			t = self.tokens.pop(name.lower())
			if t.position is not None:
				t.position.contents.remove(t)
		else:
			raise ValueError(f"Token '{name}' not found on this map.")

	def clear_tokens(self):
		t_list = list(self.tokens.items())
		for k, v in t_list:
			self.delete_token(k)

	def step_token(self, token_name, direction, distance):
		if token_name.lower() in self.tokens:
			token = self.tokens[token_name.lower()]
			old_location = token.position
			new_location = token.step(direction, distance)
			if old_location is not new_location:
				self.last_move = (old_location, new_location)
		else:
			raise ValueError(f"Token '{name}' not found on this map.")

	def move_token(self, token_name, position):
		if token_name.lower() in self.tokens:
			token = self.tokens[token_name.lower()]
			old_location = token.position
			new_location = position
			token.set_position(position)
			if old_location is not new_location:
				self.last_move = (old_location, new_location)
		else:
			raise ValueError(f"Token '{name}' not found on this map.")