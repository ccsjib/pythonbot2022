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



#keeps token safe inside .env file but loads it to be accessible
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TOKEN")

#discord default Intents - required to run bot
intents = discord.Intents.all()
intents.message_content = True
intents.reactions = True

#I am using the client method because it is much more readable for beginners. I want to switch to bot.Command in the future, but it has some limited capabilites.
#Mainly that bot.Command requires a command prefix.
client = discord.Client(intents=intents)

#uses datetime library to get today's date
print(datetime.today().strftime('%Y-%m-%d'))

#From tutorial. Gets random quote from Zenquotes API in JSON and converts to a string 
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)


#global variables required for NASA and channel information to be shared to reaction detector
channelsave = ''
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
hasAlienRanYet = False 


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')



@client.event
async def on_message(message):
     #API key for NASA API (I used the demo so I didn't have to sign up)
    k = "DEMO_KEY"
    nasa = nasapy.Nasa(key = k)
        
    #making the reaction repeat checker accessible locally.
    global hasDateRanYet
    global hasInfoRanYet
    global hasAlienRanYet
    
    #channel ID that the msg came from is saved into a global var. Then it is saved in channel locally. 
    #I originally made channel global, but that caused the reaction functionality to break. Instead, I made another var for global use.
    global channelsave
    channelsave = message.channel.id
    channel = channelsave
    
    #if the msg says "nasa":
    if message.content.startswith('nasa'):
        
        #Reset the reaction repeat checker.
        hasDateRanYet = False
        hasInfoRanYet = False
        hasAlienRanYet = False
        #print(hasAlienRanYet)
    
        #Next, if "date" is in the msg, save it to a var. If not, use today's date.
        if "date" in message.content:
            date = message.content.split("date ", 1)[1]
        else:    
            date = datetime.today().strftime('%Y-%m-%d') 
        
        #checks length of msg and saves to var
        nasaMsgLen = len(message.content)
        
        #Check msg length var. If it's 20 or 4, continue code. Else, send invalid input error.
        if nasaMsgLen == 20 or nasaMsgLen == 4:
            
            #get JSON data from NASA API
            apod = nasa.picture_of_the_day(date=date, hd=True)
            
         #There is a quote error in the NASA JSON, and somehow this command reparses it correctly. It is meant to parse a string into JSON, but it works for this too. 
            apodpython = json.dumps(apod)
            
            #This turns the JSON into a string and saves it in a var.
            apoddict = json.loads(apodpython)
            
            #accesses the global var so that reaction command can still access this data.
            global apodinfo
            global apoddate
            
            #saves the various parts of apoddict into their own vars.
            apodurl = apoddict['url']
            apodtitle = apoddict['title']
            apodinfo = apoddict['explanation']
            apoddate = apoddict['date']
                
            #mention the user and send the title + picture of the NASA astronomy pic of the day
            await message.channel.send(message.author.mention + apodtitle)
            
            #Since I recently found out that the APOD is sometimes a video:
            #if the link is to youtube, it is an embed link. 
            if "youtube" in apodurl:
                
                #This splits the link, takes the ID, and attaches it to a normal YT share link since Discord doesn't recognize the embed type link.
                #Discord has its own type of embed which ironically only works with non-embed YT links (lol)
                apodytid = apodurl.split("embed/", 1)[1]
                apodytlink = "https://youtu.be/" + apodytid
                
                #Sends link in chat, triggering Discord to embed it
                await message.channel.send(apodytlink)
                
            #If "nasa" in URL, it'a picture. Get the file using aiohttp
            if "nasa" in apodurl:
                            
                #aiohttp allows downloading an image from URL
                # creates session
                async with aiohttp.ClientSession() as session: 
                    
                    # gets image from url
                    async with session.get(apodurl) as resp: 
                        print(apodurl)
                        
                        #changes filename so discord can find it
                        filename = "nasaapodimage.jpg"
                        
                        #in the case that aiohttp can't get the file...
                        if resp.status != 200: 
                            return await channel.send('Could not download file...')
                        data = io.BytesIO(await resp.read())
    
                        #Sends image in chat.
                        await message.channel.send(file=discord.File(data, 'nasaapodimage.jpg'))
                        
            #explains how to get more data with reactions, and reacts to itself for easy access to these emojis
            pickmsg = 'Pick 📅 for the image date or 📖 for more info!'
            msg = await message.channel.send(pickmsg)
            await msg.add_reaction("📅")
            await msg.add_reaction("📖")
            
        #as mentioned at the top of the if statement, this sends and error if msg length is not either 20 or 4
        else:
            await message.channel.send("invalid input :( \n -**If including a date, make sure to type \"nasa date yyyy-mm-dd\". \n-Otherwise, type \"nasa\"!**\n-Also, try out other commands like \"hello\" and \"inspire\" :)")
            
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
    global hasAlienRanYet
    #gets channel ID from global var and saves it locally in channel var
    global channelsave
    print(channelsave)
    channel = client.get_channel(channelsave)
    
    #if the reaction is the bot's own, don't do anything 
    if user == client.user:
        return
    print(hasAlienRanYet)
    #checks if the msg reacted on matches pickmsg var.
    pickmsg = 'Pick 📅 for the image date or 📖 for more info!'
    if pickmsg in reaction.message.content:
        
        #if user reacts calendar, send date and tell var that reaction has been run
        if reaction.emoji == '📅' and hasDateRanYet == False:
            print('calendar emoji')
            await channel.send(apoddate)
            hasDateRanYet = True
            
        #same as calendar but with book reaction
        elif reaction.emoji == '📖' and hasInfoRanYet == False:
            print('book emoji')
            await channel.send(apodinfo)
            hasInfoRanYet = True  
                
        #same as above, but easter egg that deletes msgs and shows nasa logo       
        elif reaction.emoji == '👾' and hasAlienRanYet == False:
            print('alien:)')
            await reaction.message.delete()
            await channel.send('SECRET easter egg :)')
            await channel.send(file=discord.File('nasa-logo.png'))
            hasAlienRanYet = True
    
#runs bot using token
client.run(TOKEN)
    