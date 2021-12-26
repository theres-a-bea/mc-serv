# bot.py
from discord.ext import commands
from dotenv import load_dotenv
import os
import threading
import mcstatus
import rcon
import time

server = mcstatus.MinecraftServer('localhost',25565)

def mcstart():
    print('Minecraft Server Starting')
    os.chdir('server')
    command = "java -Xmx1024M -Xms1024M -jar server.jar nogui"
    os.system(command)    

def serverStatus():
    while True:
        try:
            stats = server.status()
            players = stats.players.online
        except:
            break

        if players > 0:
            timeLastOnline = round(time.time())
        
        difference = round(time.time()) - timeLastOnline

        if difference > 900:
            with rcon.Client('localhost', 25575, passwd='nipslip') as client:
                response = client.run('stop')
            print(response)
            break


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

@bot.command(name='mcstart', help='starts up minecraft server')
async def startmc(ctx):
    print('Recieved start command, rev yer fukin engines')
    await ctx.send('Command recieved, standby')

    try:
        server.status()
        await ctx.send('Server was already running, ding dong :(')
    except:
        newThread = threading.Thread(target=mcstart, daemon=True)
        newThread.start()

    await ctx.send('Server starting... please wait')

    running = False

    while running == False:
        try:
            server.status()
            running = True
        except:
            running = False
        
    newThread = threading.Thread(target=serverStatus, daemon=True)
    newThread.start()    
    
    await ctx.send('Server is up. Reminder: if server is dormant for 15+ mins, will automatically shutdown. Enjoy!')

@bot.command(name='mcstop', help='stops the minecraft server')
async def stopmc(ctx):
    print('Aaaaand sleepy time')
    await ctx.send('Recieved stop command, standby')
    status = False

    try:
        server.status()
        status = True
    except:
        status = False
    
    if status == True:
        with rcon.Client('localhost', 25575, passwd='nipslip') as client:
            response = client.run('stop')
            print(response)
            await ctx.send('Server shutdown, thanks for playing')
    else:
        await ctx.send('Server already shutdown, knob')

@bot.command(name='mcstatus', help='pulls the mcStatus data')
async def stats(ctx):
    running = False
    try:
        server.status()
        running = True
    except:
        running = False

    if running == True:
        stats = server.status()
        players = stats.players.online
        message = "Server is currently online with " + str(players) + " players."
    if running == False:
        message = "Server currently offline."
    
    await ctx.send(message)

bot.run(TOKEN)