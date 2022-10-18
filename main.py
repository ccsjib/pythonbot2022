from fileinput import filename
import discord
import os
from discord.ext import commands
import requests
import json
import nasapy
import pandas as pd
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

print(datetime.today().strftime('%Y-%m-%d'))


#nasapicture = urllib.request.urlretrieve(url = apod["hdurl"] , filename = os.path.join(image_dir,title))

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
        if "date" in message.content:
            date = message.content.split("date ", 1)[1]
        else:    
            date = datetime.today().strftime('%Y-%m-%d')  
        
        k = "DEMO_KEY"
        nasa = nasapy.Nasa(key = k)

        

        #apod = nasa.picture_of_the_day(date='2019-01-01', hd=True)
        apod = nasa.picture_of_the_day(date=date, hd=True)


        apodpython = json.dumps(apod) #turns the apod data from a json string into one with correct quotes

        #print(apodpython)

        apoddict = json.loads(apodpython)

        apodurl = apoddict['url']
        apodtitle = apoddict['title']
        apodinfo = apoddict['explanation']
        apoddate = apoddict['date']
        async with aiohttp.ClientSession() as session: # creates session
            async with session.get(apodurl) as resp: # gets image from url
                filename = "nasaapodimage.jpg" #changes filename so discord can find it
                if resp.status != 200:
                    return await channel.send('Could not download file...')
                data = io.BytesIO(await resp.read())
                await message.channel.send(message.author.mention + apodtitle)
                await message.channel.send(file=discord.File(data, 'nasaapodimage.jpg'))
                await message.channel.send("Check DMs for picture info!")
                await message.author.send(file='nasa-logo.png'))
                await message.author.send(apodinfo)
                await message.channel.send("Image Date: " + apoddate)
                
    if message.author == client.user:
        return

    if message.content.startswith('hello'):
        await message.channel.send(apod)

    if message.content.startswith('inspire'):
        quote = get_quote()
        await message.channel.send(quote)
    
client.run(TOKEN)
    