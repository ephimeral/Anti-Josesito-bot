from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import discord
from discord.ext import commands
import random

class MyBot(commands.Bot):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        imagenes = None

    async def setup_hook(self):
        self.imagenes = await scrape()

    async def on_ready(self):
        print(f"Logging in as: {self.user}")



client = MyBot(command_prefix=commands.when_mentioned_or("jj"),intents=discord.Intents.all(),
                      case_insensitive=True, activity=discord.Game(name="con los pezones de Jhon Llama"))
client.remove_command('help')

@client.event
async def on_message(message):
	user = message.author

	await user.send(client.imagenes[random.randint(0,len(client.imagenes) - 1)])

async def scrape():
	# Configurar firefox sin interfaz
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	chrome_options.add_argument("--log-level=3")
	driver = webdriver.Chrome(options=chrome_options)

	driver.get("https://rule34.xxx/index.php?page=post&s=list&tags=lt._john_llama")

	# Esperar a el tag 'image-list'
	wait = WebDriverWait(driver, 2)
	element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'image-list')))

	soup = BeautifulSoup(driver.page_source, 'html.parser')

	image_links = []

	# Hacer una lista con el link de los posts de las imagenes
	for element in soup.find(class_='image-list').find_all('a'):
	    image_link = element.get('href')
	    url = f"https://rule34.xxx{image_link}"
	    image_links.append(url)

	imagenes = []
	# Iterar en cada link y sacar el link de la imagen
	for url in image_links:
	    driver.get(url)
	    image_soup = BeautifulSoup(driver.page_source, 'html.parser')
	    imagen = image_soup.find(class_='flexi').find('img')

	    if imagen:
	        imagenes.append(imagen.get('src'))

	driver.quit()
	return imagenes


client.run("MTEyMzM5NTE1MzgzOTc5MjI0MA.Gmfst-.DqF93vqKNMb9Y9N_IR6q1wj5w2-SRs-NqBv7rI")