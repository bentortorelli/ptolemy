from discord.ext import commands
import discord
import asyncio
import configparser

#test

class Ptolemy(commands.Bot):
	def __init__(self):
		config = configparser.ConfigParser()
		config.read('options.cfg')
		BOT_TOKEN = config.get('credentials', 'token')
		super().__init__(commands.when_mentioned)
		
		self.add_command(self.test)
		self.load_extension("cogs.maptools")
		self.run(BOT_TOKEN)

	async def on_ready(self):
		print('Logged in as')
		print(self.user.name)
		print(self.user.id)
		print('------')

	@commands.command(pass_context=True)
	async def test(self, ctx):
		print(ctx)
		await self.say("hello")

if __name__ == "__main__":
	p = Ptolemy()
	#new_map = Map(10, 30, 50)
	#new_map.drawMap('rectangle.png')
