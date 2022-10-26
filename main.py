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


intents = discord.Intents.all()
intents.message_content = True
intents.reactions = True

client = discord.Client(intents=intents)

print(datetime.today().strftime('%Y-%m-%d'))


#nasapicture = urllib.request.urlretrieve(url = apod["hdurl"] , filename = os.path.join(image_dir,title))

#apod = nasa.picture_of_the_day(date=d, hd=True)

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

apod = ''
apodpython = ''
apoddict = ''
apodurl = ''
apodtitle = ''
apodinfo = ''
apoddate = ''
apodtest = ''
hasDateRanYet = False                
hasInfoRanYet = False  

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    global hasDateRanYet
    global hasInfoRanYet
    
    channel = client.get_channel("775355712271941647")
    #message.channel.send("say nasa to get the pic of the day ")
    if message.content.startswith('nasa'):
        hasDateRanYet = False
        hasInfoRanYet = False
        nasaMsgLen = len(message.content)
        if "date" in message.content:
            date = message.content.split("date ", 1)[1]
            print(nasaMsgLen)
        else:    
            date = datetime.today().strftime('%Y-%m-%d') 
            print(nasaMsgLen)
        
        k = "DEMO_KEY"
        nasa = nasapy.Nasa(key = k)
        if nasaMsgLen == 20 or nasaMsgLen == 4:
            #apod = nasa.picture_of_the_day(date='2019-01-01', hd=True)
            apod = nasa.picture_of_the_day(date=date, hd=True)
            

            apodpython = json.dumps(apod) #turns the apod data from a json string into one with correct quotes

            #print(apodpython)

            apoddict = json.loads(apodpython)

            apodurl = apoddict['url']
            apodtitle = apoddict['title']
            global apodinfo
            apodinfo = apoddict['explanation']
            global apoddate
            apoddate = apoddict['date']
            global apodtest
            apodtest = 55
            print(apodtest)
            
            async with aiohttp.ClientSession() as session: # creates session
                async with session.get(apodurl) as resp: # gets image from url
                    filename = "nasaapodimage.jpg" #changes filename so discord can find it
                    if resp.status != 200:
                        return await channel.send('Could not download file...')
                    data = io.BytesIO(await resp.read())
                    await message.channel.send(message.author.mention + apodtitle)
                    await message.channel.send(file=discord.File(data, 'nasaapodimage.jpg'))
                    pickmsg = 'Pick 📅 for the image date or 📖 for more info!'
                    msg = await message.channel.send(pickmsg)
                    await msg.add_reaction("📅")
                    await msg.add_reaction("📖")
                    #await message.author.send(file=discord.File('nasa-logo.png'))
                    #await message.author.send(apodinfo)
                    #await message.channel.send("Image Date: " + apoddate)
        else:
            await message.channel.send("something went wrong :(")
    if message.author == client.user:
        return

    if message.content.startswith('hello'):
        await message.channel.send(apod)

    if message.content.startswith('inspire'):
        quote = get_quote()
        await message.channel.send(quote)
              
@client.event
async def on_reaction_add(reaction, user):
    #apoddate = 'testing1q243'
    global hasDateRanYet
    global hasInfoRanYet
    channel = client.get_channel(775355712271941647)
    #print(channel)
    #if reaction.message.channel.id != channel.id:
        #return
    pickmsg = 'Pick 📅 for the image date or 📖 for more info!'
    print(reaction.message)
    if user == client.user:
        return
    if pickmsg in reaction.message.content and reaction.emoji == '📅' and hasDateRanYet == False:
        print('calendar emoiji')
        await channel.send(apoddate)
        hasDateRanYet = True
    else:
        if pickmsg in reaction.message.content and reaction.emoji == '📖' and hasInfoRanYet == False:
                await channel.send(apodinfo)
                hasInfoRanYet = True  
    
    
client.run(TOKEN)
    