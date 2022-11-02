from fileinput import filename
import discord #discord.py 
import os
from discord.ext import commands
import requests
import nasapy #to access NASA API
import json #to read JSON from NASA API
import pandas as pd #needed for nasapy
import io 
import aiohttp #needed to download file from URL
from datetime import datetime #to get current date and time



#keeps token safe inside .env file
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TOKEN")


intents = discord.Intents.all()
intents.message_content = True
intents.reactions = True

#I am using the client method because it is much more readable for beginners. I hope to switch to bot.Command in the future, but I am not sure if it has all the capabilites I need. 
client = discord.Client(intents=intents)

#uses datetime library to get today's date
print(datetime.today().strftime('%Y-%m-%d'))

#From tutorial. Gets random quote from Zenquotes API in JSON and converts to a string 
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)


#global variables required for NASA information to be shared to reaction detector
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
channel = '' 

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    global hasDateRanYet
    global hasInfoRanYet
    
    #current channel ID (this one is #free-for-all)
    global channel
    #channel = client.get_channel(775355712271941647)
    channel = message.channel.id
    
    
    #if the msg says nasa, reset the reaction counter from any previous posts.
    if message.content.startswith('nasa'):
        hasDateRanYet = False
        hasInfoRanYet = False
        #checks length of msg and saves to var
        nasaMsgLen = len(message.content)
        #Next, if date is in the msg, save it to a var. If not, use today's date.
        if "date" in message.content:
            date = message.content.split("date ", 1)[1]
            print(nasaMsgLen)
        else:    
            date = datetime.today().strftime('%Y-%m-%d') 
            print(nasaMsgLen)
        
        #API key for NASA API (I used the demo so I didn't have to sign up)
        k = "DEMO_KEY"
        nasa = nasapy.Nasa(key = k)
        
        #Check msg length var. If it's 20 or 4, continue code. Else, send invalid input error.
        if nasaMsgLen == 20 or nasaMsgLen == 4:
            
            #get JSON data from NASA API
            apod = nasa.picture_of_the_day(date=date, hd=True)
            
         #There is a quote error in the NASA JSON, and somehow this command reparses it correctly. It is meant to parse a string into JSON, but it works for this too. 
            apodpython = json.dumps(apod)
            
            #This turns the JSON into a string and saves it in a var.
            apoddict = json.loads(apodpython)
            
            #saves the various parts of apoddict into their own vars.
            apodurl = apoddict['url']
            apodtitle = apoddict['title']
            #accesses the global variable so that the reaction command can still access this data.
            global apodinfo
            apodinfo = apoddict['explanation']
            global apoddate
            apoddate = apoddict['date']
            global apodtest
            apodtest = 55
            #print(apodtest)
            
            
            async with aiohttp.ClientSession() as session: # creates session
                async with session.get(apodurl) as resp: # gets image from url
                    print(apodurl)
                    filename = "nasaapodimage.jpg" #changes filename so discord can find it
                    if resp.status != 200: #if aiohttp can't get the file...
                        return await channel.send('Could not download file...')
                    data = io.BytesIO(await resp.read())
                    #mention the user and send the title + picture of the NASA astronomy pic of the day
                    if "youtube" in apodurl:
                        apodyoutube = apodurl.split("embed/", 1)[1]
                        print(apodyoutube)
                        apodytlink = "https://youtu.be/" + apodyoutube
                        await message.channel.send(apodytlink)
                    await message.channel.send(message.author.mention + apodtitle)
                    if "nasa" in apodurl:
                        await message.channel.send(file=discord.File(data, 'nasaapodimage.jpg'))
                    #explains how to get more data with reactions, and reacts to itself for easy access to these emojis
                    pickmsg = 'Pick 📅 for the image date or 📖 for more info!'
                    msg = await message.channel.send(pickmsg)
                    await msg.add_reaction("📅")
                    await msg.add_reaction("📖")
                    #await message.author.send(file=discord.File('nasa-logo.png'))
                    #await message.author.send(apodinfo)
                    #await message.channel.send("Image Date: " + apoddate)
        #as mentioned at the top of the if statement, this sends and error if msg length is not either 20 or 4
        else:
            await message.channel.send("invalid input :( try again!")
    #stops the bot from detecting its own msgs/reactions for any code below this.
    if message.author == client.user:
        return
    #respond to hello with hello :D
    if message.content.startswith('hello'):
        await message.channel.send('hello :D')

    #respond to inspire by getting the quote from the API above.
    if message.content.startswith('inspire'):
        quote = get_quote()
        await message.channel.send(quote)
              
@client.event
#checks for a reaction added by a user
async def on_reaction_add(reaction, user):
    #checks if the reactions have been ran already for the current instance of nasa msg (saying nasa resets these)
    global hasDateRanYet
    global hasInfoRanYet
    #free-for-all channel ID
    #channel = client.get_channel(775355712271941647)
    global channel
    #checks if the msg reacted on matches pickmsg var.
    pickmsg = 'Pick 📅 for the image date or 📖 for more info!'
    #if the reaction is the bot's own, don't do anything 
    if user == client.user:
        return
    #if user reacts calendar, send date and tell var that reaction has been run
    if pickmsg in reaction.message.content and reaction.emoji == '📅' and hasDateRanYet == False:
        print('calendar emoji')
        await channel.send(apoddate)
        hasDateRanYet = True
    else:
        #same as calendar but with book reaction
        if pickmsg in reaction.message.content and reaction.emoji == '📖' and hasInfoRanYet == False:
                print('book emoji')
                await channel.send(apodinfo)
                hasInfoRanYet = True  
    
    
client.run(TOKEN)
    