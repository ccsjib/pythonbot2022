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



#intents = discord.Intents.default()
#intents.message_content = True
#intents.reactions = True

bot = commands.Bot(command_prefix=".", intents=discord.Intents.default())


print(datetime.today().strftime('%Y-%m-%d'))


#nasapicture = urllib.request.urlretrieve(url = apod["hdurl"] , filename = os.path.join(image_dir,title))

#apod = nasa.picture_of_the_day(date=d, hd=True)

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)


@bot.command()
async def on_ready(ctx):
    print(f'We have logged in as {bot.user}')

@bot.event
async def nasa(ctx):
    channel = ctx.get_channel("775355712271941647")
    if ctx.content.startswith('.nasa'):
        if "date" in ctx.content:
            date = ctx.content.split("date ", 1)[1]
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
                await ctx.channel.send(ctx.author.mention + apodtitle)
                await ctx.channel.send(file=discord.File(data, 'nasaapodimage.jpg'))
                pickmsg = 'Pick 📅 for the image date or 📖 for more info!'
                msg = await ctx.channel.send(pickmsg)
                await msg.add_reaction("📅")
                await msg.add_reaction("📖")
                    #await client.wait_for("reaction_add")   
                    #await reaction.message.channel.send(apodinfo)
                #await message.channel.send(apodinfo)
                #await message.author.send(file=discord.File('nasa-logo.png'))
                #await message.author.send(apodinfo)
                #await message.channel.send("Image Date: " + apoddate)
    if ctx.author == bot.user:
        return

    if ctx.content.startswith('hello'):
        await ctx.channel.send(apod)

    if ctx.content.startswith('inspire'):
        quote = get_quote()
        await ctx.channel.send(quote)
                
@bot.event
async def on_raw_reaction_add(payload):
    channel = cotx.get_channel("775355712271941647")
    pickmsg = 'Pick 📅 for the image date or 📖 for more info!'
    print(payload.reaction.message.content)
    if pickmsg in payload.message.content and payload.emoji == '📅':
        await channel.message.send(apoddate)
    else:
        if pickmsg in reaction.message.content and reaction.emoji == '📖':
            await channel.message.send(apodinfo)               
    
    
bot.run(TOKEN)
    