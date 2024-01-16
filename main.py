import discord
import os
import utils
from discord.ext import commands
from discord import FFmpegPCMAudio
from dotenv import load_dotenv
from googleapiclient.discovery import build

# Load environment variables
load_dotenv()
bot_token = os.getenv("BOT_TOKEN")
gcp_api_key = os.getenv("GCP_API_KEY")

# Init client
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

# Voice-related commands
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

# Init youtube service instance
youtube = build("youtube", "v3", developerKey=gcp_api_key)

@client.command()
async def search(ctx, *, search_query):
    response = utils.search_youtube(youtube, search_query)

    message = "Top 10 results found:\n"
    for item in response.get("items", []):
        title = item["snippet"]["title"]
        video_id = item["id"]["videoId"]
        url = f"https://www.youtube.com/watch?v={video_id}"
        message += f"{title}\n{url}\n\n"
    
    await ctx.send(message)
    
if __name__ == "__main__":
    client.run(bot_token)   