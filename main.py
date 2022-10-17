import discord
import os
import requests
import json
#import nasapy
import io
import aiohttp
from datetime import datetime
#import urllib.request

from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TOKEN")


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

k = "demo_key"
#nasa = nasapy.Nasa(key = k)


#nasapicture = urllib.request.urlretrieve(url = apod["hdurl"] , filename = os.path.join(image_dir,title))

d = datetime.today().strftime('%Y-%m-%d')
#apod = nasa.picture_of_the_day(date=d, hd=True)

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    channel = client.get_channel("775355712271941647")
    if message.content.startswith('nasa'):
        async with aiohttp.ClientSession() as session: # creates session
            async with session.get("https://apod.nasa.gov/apod/image/2209/WR140_WebbSchmidt_960.jpg") as resp: # gets image from url
                if resp.status != 200:
                    return await channel.send('Could not download file...')
                data = io.BytesIO(await resp.read())
                await message.channel.send(file=discord.File(data, 'WR140_WebbSchmidt_960.jpg'))
    if message.author == client.user:
        return

    if message.content.startswith('hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('inspire'):
        quote = get_quote()
        await message.channel.send(quote)
    
client.run(TOKEN)
    