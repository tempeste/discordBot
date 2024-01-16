import discord
import os
from discord.ext import commands
from discord import FFmpegPCMAudio
from dotenv import load_dotenv

load_dotenv()
bot_token = os.getenv("BOT_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(intents=intents, command_prefix = '!')

@client.event
async def on_ready():
    print('Bot is ready.')
    print("Logged in as: " + client.user.name + "\n")
    
@client.command()
async def ping(ctx):
    await ctx.send('Pong!')

@client.command()
async def hello(ctx):
    await ctx.send('Hello!')
    
@client.command(pass_context=True)
async def join(ctx):
    if (ctx.message.author.voice == None):
        await ctx.send("You are not in a voice channel.")
        return
    channel = ctx.message.author.voice.channel
    await channel.connect()

@client.command(pass_context=True)
async def leave(ctx):
    if (ctx.voice_client == None):
        await ctx.send("I am not in a voice channel.")
        return
    await ctx.voice_client.disconnect()

client.run(bot_token)