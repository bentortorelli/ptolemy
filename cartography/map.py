from PIL import Image, ImageDraw, ImageFont
from cartography.hex import Hex
from cartography.token import Token
from specktre import tilings
import math
	
class Map:
	def __init__(self, width, height, edge_length):
		self.edge_length = edge_length
		self.short_diagnol = int(math.sqrt(3)*edge_length)
		self.long_diagnol = 2*edge_length

		dif = int((self.long_diagnol - edge_length)/2)
		self.image_width = self.long_diagnol + int((self.long_diagnol-dif)*(width-1))
		self.image_height = (self.short_diagnol+1)*height

		self.map_color = "white" #error check map color
		self.hexes = dict()
		self.last_move = None
		self.tokens = dict()

		coordinates = tilings.generate_hexagons(self.image_width, self.image_height, self.edge_length)

		hex_list = list()
		for coords in coordinates:
			for x,y in coords:
				valid = True
				if x < 0 or y < 0 or x > self.image_width or y > self.image_height:
					valid = False
					break
			if valid:
				new_hex = Hex(self, coords)
				hex_list.append(new_hex)
				
		hex_list.sort()
		hex_x = 0
		hex_y = 0
		prev_y = self.image_height
		for hex in hex_list:
			if(hex.center[1] >= prev_y):
				hex_x += 1
				hex_y = 0
			hex.position = (hex_x, hex_y)
			hex_y += 1
			prev_y = hex.center[1]
			self.hexes[hex.position] = hex

	def drawMap(self, file_path, draw_move=False):
		# Create a blank 500x500 pixel image
		im = Image.new("RGB", (self.image_width, self.image_height), color = 'white')

		# Draw
		for pos, hex in self.hexes.items():
			hex.draw(im)

		if draw_move:
			line_coords = (self.last_move[0].center[0], self.last_move[0].center[1], self.last_move[1].center[0], self.last_move[1].center[1])
			ImageDraw.Draw(im).line(line_coords, width=10, fill = "red")

		# Save the image to disk
		im.save(file_path)

	def getHex(self, pos):
		try:
			return self.hexes[pos]
		except KeyError:
			return None

	def paintHex(self, position, hex_color, text_color):
		hex = self.getHex(position)
		hex.hex_color = hex_color
		hex.text_color = text_color


	def addToken(self, name, position, image, image_url):
		if name not in self.tokens:
			t = Token(name, position, image, image_url)
			self.tokens[name.lower()] = t
		else:
			raise ValueError("Token name already exists on this map.")

	def deleteToken(self, name):
		if name in self.tokens:
			t = self.tokens.pop(name.lower())
			if isinstance(t.position, Hex):
				t.position.contents.remove(t)
		else:
			raise ValueError(f"Token '{name}' not found on this map.")

	def clearTokens(self):
		t_list = list(self.tokens.items())
		for k, v in t_list:
			self.deleteToken(k)

	def stepToken(self, token_name, direction, distance):
		if token_name.lower() in self.tokens:
			token = self.tokens[token_name.lower()]
			old_location = token.position
			new_location = token.step(direction, distance)
			if old_location is not new_location:
				self.last_move = (old_location, new_location)
		else:
			raise ValueError(f"Token '{name}' not found on this map.")

	def moveToken(self, token_name, position):
		if token_name.lower() in self.tokens:
			token = self.tokens[token_name.lower()]
			old_location = token.position
			new_location = position
			token.setPosition(position)
			if old_location is not new_location:
				self.last_move = (old_location, new_location)
		else:
			raise ValueError(f"Token '{name}' not found on this map.")