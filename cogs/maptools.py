from discord.ext import commands
from cartography import Map, Token, Direction
from urllib.request import urlopen
from PIL import Image
import discord

class Maptools:
	def __init__(self, bot):
		self.maps = dict()
		self.bot = bot
	@commands.command(pass_context=True)
	async def create(self, ctx, width, height, type = "square", edge_length=50):
		"""Creates a new map for the server.
		Only one map can exist for a server at a time. Map dimensions are 'width' x 'height' grid spaces. 
		Valid map types are 'square' and 'hex'. 'edge_length' specifies the length of each edge of a space in pixels.
		"""
		server_id = ctx.message.server.id
		if server_id in self.maps:
			await self.bot.say("A map for this server already exists. Use the 'delete' command before creating new self.maps.")
		else:
			try:
				self.maps[server_id] = Map(int(width), int(height), int(edge_length), type)
			except ValueError as e:
				return await self.bot.say(str(e))
			#draw map
			await self.bot.say("Map created.")

	@commands.command(pass_context=True)
	async def delete(self, ctx):
		"""Deletes the current server map."""
		server_id = ctx.message.server.id
		if server_id in self.maps:
			m = self.maps.pop(server_id)
			m.clear_tokens()
			await self.bot.say("Map deleted.")
		else:
			await self.bot.say("There is no map for this server.")

	@commands.command(pass_context=True, aliases=["highnoon"])
	async def draw(self, ctx):
		"""Displays the current map to the channel.
		Generates an image of the map's current state and uploads it to the channel along with a map key of current tokens.
		"""
		server_id = ctx.message.server.id
		if server_id in self.maps:
			server_map = self.maps[server_id]
			server_map.draw_map("maps/"+server_id+".png")
			await self.bot.upload("maps/"+server_id+".png")

			if len(server_map.tokens) >= 1:
				embed=discord.Embed(title="Map Tokens")
				for k,v in server_map.tokens.items():
					embed.add_field(name=v.name, value=v.position.text, inline=True)
				await self.bot.say(embed=embed)
		else:
			await self.bot.say("No map for this server. Use the 'create' command to create a map.")

	@commands.command(pass_context=True)
	async def addtoken(self, ctx, name, x, y, image_url):
		"""Adds a token to the current map.
		The token is added to the map with ID 'name' at position ('x','y') using the image at 'image_url'
		"""
		server_id = ctx.message.server.id
		if server_id in self.maps:
			server_map = self.maps[server_id]
			try:
				token_image = Image.open(urlopen(image_url))
				hex = server_map.get_space((int(x),int(y)))
				if hex is None:
					return await self.bot.say(f"Map position ({x},{y}) is invalid.")
				server_map.add_token(name, hex, token_image, image_url)
				await self.bot.say("Token added.")
			except ValueError as e:
				await self.bot.say(str(e))
			except OSError as e:
				await self.bot.say("Image URL is inaccessible.")
		else:
			await self.bot.say("There is no map for this server.")

	@commands.command(pass_context=True)
	async def deletetoken(self, ctx, name):
		"""Deletes a token from the current map.
		The token with with ID 'name' is removed from the map.
		"""
		server_id = ctx.message.server.id
		if server_id in self.maps:
			server_map = self.maps[server_id]
			try:
				server_map.delete_token(name)
				await self.bot.say(f"Token {name} deleted.")
			except ValueError as e:
				await self.bot.say(str(e))
		else:
			await self.bot.say("There is no map for this server.")

	@commands.command(pass_context=True)
	async def step(self, ctx, name, direction, distance):
		"""Steps a token in a compass direction.
		The token with ID 'name' is moved 'distance' spaces in a compass direction. 
		Valid directions are: north, south, east, west, northeast, northwest, southeast, southwest, n, s, e, w, ne, nw, se, sw.
		Some directions may not be valid on all map types  (e.g. east and west on hex grid maps)
		"""
		server_id = ctx.message.server.id
		if server_id in self.maps:
			denum = None
			if direction.lower() in ["north", "n"]:
				denum = Direction.NORTH
			elif direction.lower() in ["south", "s"]:
				denum = Direction.SOUTH
			elif direction.lower() in ["east", "e"]:
				denum = Direction.EAST
			elif direction.lower() in ["west", "w"]:
				denum = Direction.WEST
			elif direction.lower() in ["northeast", "ne"]:
				denum = Direction.NORTH_EAST
			elif direction.lower() in ["northwest", "nw"]:
				denum = Direction.NORTH_WEST
			elif direction.lower() in ["southeast", "se"]:
				denum = Direction.SOUTH_EAST
			elif direction.lower() in ["southwest", "sw"]:
				denum = Direction.SOUTH_WEST
			else:
				return await self.bot.say("Invalid direction. See 'help step' for valid directions.")
			server_map = self.maps[server_id]
			try:
				server_map.step_token(name, denum, int(distance))
				server_map.draw_map("maps/"+server_id+".png", True)
				await self.bot.upload("maps/"+server_id+".png")
			except ValueError as e:
				await self.bot.say(str(e))
		else:
			await self.bot.say("There is no map for this server.")

	@commands.command(pass_context=True)
	async def move(self, ctx, name, x, y):
		"""Moves a token to a space directly.
		The token with ID 'name' is moved directly to map position ('x','y')
		"""
		server_id = ctx.message.server.id
		if server_id in self.maps:
			server_map = self.maps[server_id]
			try:
				hex = server_map.get_space((int(x),int(y)))
				if hex is None:
					return await self.bot.say(f"Map position ({x},{y}) is invalid.")
				server_map.move_token(name, hex)
				server_map.draw_map("maps/"+server_id+".png", True)
				await self.bot.upload("maps/"+server_id+".png")
			except ValueError as e:
				await self.bot.say(str(e))

		else:
			await self.bot.say("There is no map for this server.")

def setup(bot):
	bot.add_cog(Maptools(bot))