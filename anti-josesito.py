import discord
from discord.ext import commands
import asyncio
import random
from requests_html import AsyncHTMLSession
import asyncio
import itertools

class MyBot(commands.Bot):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.imagenes = []

	async def setup_hook(self):
		await self.scraper()

	async def on_ready(self):
		print(f"Logging in as: {self.user}")

	async def get_post_link(self, pid):
		r = await self.asession.get(f'https://rule34.xxx/index.php?page=post&s=list&tags=lt._john_llama&pid={pid}')
		link_images = [link.attrs['href'] for link in r.html.find('.image-list a')]
		return link_images

	async def get_image_link(self, url):
		url = f"https://rule34.xxx{url}"

		r = await self.asession.get(url)
		imagen = r.html.find('.flexi img')
		if imagen:
			imagen = imagen[0].attrs['src']
			self.imagenes.append(imagen)

	async def scraper(self):
		self.asession = AsyncHTMLSession()
		pids = [0, 42, 84, 126, 168]  
		tasks = [self.get_post_link(pid) for pid in pids]  
		post_links_nested = await asyncio.gather(*tasks) 
		post_links = list(itertools.chain.from_iterable(post_links_nested)) 
		tasks = [self.get_image_link(url) for url in post_links]
		await asyncio.gather(*tasks)




client = MyBot(command_prefix=commands.when_mentioned_or("jj"),intents=discord.Intents.all(),
                      case_insensitive=True, activity=discord.Game(name="con los pezones de Jhon Llama"))
client.remove_command('help')



@client.event
async def on_message(message):
	user = message.author
	if user.bot:
		return

	if user.id == 180858106761314305:
		await user.send(client.imagenes[random.randint(0,len(client.imagenes) - 1)])

client.run(TOKEN)
