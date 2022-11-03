Welcome to jib's NASA bot :)

This bot connects to the NASA Astronomy Picture of the Day (APOD) API to pull the picture along with all relevant information. It can send different pieces of info based on a user's reaction to the message, keeping chat from clogging up. 

Commands:

"nasa" - Pings the user + sends title along with APOD. Displays a message with reactions that can be used as buttons to obtain an image description and date. 
"nasa date yyyy-mm-dd" - A version of the "nasa" command which allows finding the Nasa APOD for a specific day.
"hello" - Replies with hello :D
"inspire" - Replies with an inspirational quote!


My code started out with this template: https://www.freecodecamp.org/news/create-a-discord-bot-with-python/ (thank you Liam!).

I started with this discord.py base code, but many of its functions did not work (like dotenv). I tried many versions of the dotenv code I found on different forums and websites until I got it working (I had to install python-dotenv and reference my .env file). The ZenQuote API code was included in the tutorial code for testing purposes, and I ended up leaving it in as the "inspire" command on my bot. From there, I looked around for some cool APIs and found Nasa's OpenAPIs along with Nasapy, a Python library for the API. I made my goal to parse the data received from the API into an interactive sequence of Discord messages. I ran into an enormous amount of issues, each requiring lots of Googling errors, learning new code, and writing nested if-else logic for message detection. Throughout this experience, I was able to gain a much deeper understanding, and I can now clearly explain what each piece of my code does.  

At the beginning of this project, I used discord.js. I understood the code until the tutorial became extremely hazy after the command handling section. This is when I switched to Python. Command handling is one thing that I do miss about discord.js, and I hope to find a way to implement it discord.py. The concept of command handling is to create a modular system that eliminates endless nested if-else statements routing commands. The main bot file can reference a command handler file while passing on the bot's trigger. The handler file is responsible for conditional statements, iterating through until it finds the correct command. This reference is to a dedicated command file which houses the command's actions. The best part about this system is that the command files can be put into a folder and the handler can be told to automatically look through all the files. This module approach means that a new command can be added simply by creating a new command file with the same format as the others. 

Command handling divides the bot's process into 3 distinct pieces: the command files are responsible for the command's actions, the handler is responsible for selecting the correct command based on the user's input, and the main bot file is responsible for running the Discord bot itself and routing the user's commands to the handler. This makes the code much less cluttered and much easier to read. I think this can be recreated in Python by learning how to import variables and libraries across files. I have a general how this is done, and I hope that, with some troubleshooting, this will be the next thing I accomplish with my bot.

