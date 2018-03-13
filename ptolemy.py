from discord.ext import commands
import discord
import asyncio
import configparser

import discord
import logging



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
	logger = logging.getLogger('discord')
	logger.setLevel(logging.INFO)
	handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
	handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
	logger.addHandler(handler)

	p = Ptolemy()