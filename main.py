# Hide warnings about depreciation
import warnings
warnings.filterwarnings("ignore")

# Import discord.py. Allows access to Discord's API.
import discord
import os
import sys
import time
import datetime
from discord.ext import commands
from dotenv import load_dotenv

#Selenium Imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging']) #Hides unhelpful messages in terminal
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(executable_path="C:/Users/alexe/AppData/Local/Programs/Python/Python39/Scripts/chromedriver.exe", options=chrome_options)

ISLAND 			= 	0,
VALGUERO 		= 	0,
RANGAROK 		= 	0,
GENESIS1 		= 	0,
GENESIS2 		= 	0,
SCORCHEDEARTH 	= 	0,
ABERRATION 		= 	0,
CRYSTALISLES 	= 	0,
CENTER 			= 	0,
EXTINCTION 		= 	0

# Loads the .env file that resides on the same level as the script.
load_dotenv()
# Grab the API token from the .env file.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Creates a new Bot object with a specified prefix. It can be whatever you want it to be.
bot = commands.Bot(command_prefix="!")

print("Bot has started! Press ctrl+c to stop.")

watch_list = []
alerts = []

@bot.event
async def on_message(message):
	# if message.content == "island":
	if message.content.startswith("island") or message.content.startswith("!isl"):

	        server_output = ''
	        # Open the battlemetrics page for the map
	        driver.get(f'https://www.battlemetrics.com/servers/ark/7811424')
	        for table in driver.find_elements_by_xpath('//*[@id="serverPage"]/div[4]/div[1]/table'):
	            server_data = [item.text for item in table.find_elements_by_xpath(".//*[self::td or self::th]")]

	            #Get server population
	            population = int(len(server_data)/3 - 1)
				
	            server_output += "--- The Island [" + str(population) + " online] " + datetime.datetime.now().strftime("[%m/%d/%Y, %I:%M:%S %p]") + " ---\n"
				
	            i = 0
	            #Only look at active members
	            for x in range(2, len(server_data)):
	                if(i == 1):
	                    if(server_data[x] in watch_list):
	                        server_output += server_data[x] + " [" + server_data[x+1] + "] - " + alerts + "\n"
	                    else:
	                        server_output += server_data[x] + " [" + server_data[x+1] + "]\n"
	                i += 1
	                if(i == 3):
	                    i = 0
	        await message.channel.send(server_output)

	# Includes the commands for the bot. Without this line, you cannot trigger your commands.
	await bot.process_commands(message)

# Command !ping. Invokes only when the message "!ping" is send in the Discord server.
# Alternatively @bot.command(name="ping") can be used if another function name is desired.
@bot.command(
	# Adds this value to the !help ping message.
	help="Uses come crazy logic to determine if pong is actually the correct value or not.",
	# Adds this value to the !help message.
	brief="Prints pong back to the channel."
)

async def reset_all_timers(ctx):
    await ctx.channel.send("Resetting all map timers")

async def status(ctx):
	# Sends a message to the channel using the Context object.
	await ctx.channel.send("Status Update")

# Command !print. This takes an in a list of arguments from the user and simply prints the values back to the channel.
@bot.command(
	# Adds this value to the !help print message.
	help="Looks like you need some help.",
	# Adds this value to the !help message.
	brief="Prints the list of values back to the channel."
)

async def timer(ctx, args):
    time.sleep(int(args))
    await ctx.channel.send(f'The bot has waited for {args} second(s)!')

async def print(ctx, *args):
	response = ""

	# Loops through the list of arguments that the user inputs.
	for arg in args:
            response = response + " " + arg
            if(arg == 'valg'):
                await ctx.channel.send('Resetting orp for valguero')
	# Sends a message to the channel using the Context object.
	await ctx.channel.send(response)

# Executes the bot with the specified token. Token has been removed and used just as an example.
bot.run(DISCORD_TOKEN)