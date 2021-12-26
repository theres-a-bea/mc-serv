# bot.py
import os
from discord.ext import commands
from dotenv import load_dotenv

#Loads details from .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following server:\n'
        f'{guild.name}(id: {guild.id})'
    )
@bot.command(name='mcstart', help='starts up minecraft instance')
async def startmc(ctx):
    print('Recieved start command, rev yer fukin engines')
    await ctx.send('Command recieved, standby')
    #RUN MC SERVER
    

bot.run(TOKEN)