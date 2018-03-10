from PIL import Image, ImageDraw, ImageFont
import math

class Token:
	def __init__(self, name, position, image, image_url):
			self.name = name
			self.position = None
			self.set_position(position)
			self.image = image #Image.open('test.png')
			self.image_url = image_url

	def set_position(self, position):
		#if isinstance(position, Hex):
		if self.position is not None:
			self.position.contents.remove(self)
		self.position = position #weakref.ref(position)
		self.position.contents.append(self)

	def step(self, direction, distance):
		if distance <= 0:
			raise ValueError("Distance cannot be zero.")
		for i in range(0, distance):
			if self.position.get_adjacent(direction) is None:
				break
			else:
				self.set_position(self.position.get_adjacent(direction))
		return self.position

	def draw(self, background_image, position, size):
		adjusted_image = self.image.resize(size, Image.LANCZOS)
		background_image.paste(adjusted_image, position, adjusted_image)
