import discord
import os
import subprocess
import re
import asyncio
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
youtube = None

@client.command()
async def disable_youtube(ctx):
    global youtube
    youtube = None
    await ctx.send("Youtube search disabled.")
    
@client.command()
async def enable_youtube(ctx):
    global youtube
    youtube = build("youtube", "v3", developerKey=gcp_api_key)
    await ctx.send("Youtube search enabled.")

@client.command()
async def search(ctx, *, search_query):
    if youtube is None:
        await ctx.send("YouTube search is currently disabled. Please enable it first.")
        return

    response = utils.search_youtube(youtube, search_query)

    if not response or "items" not in response:
        await ctx.send("No results found or an error occurred.")
        return

    message = "Top 10 results found:\n"
    for item in response.get("items", []):
        title = item["snippet"]["title"]
        video_id = item["id"]["videoId"]
        url = f"https://www.youtube.com/watch?v={video_id}"
        message += f"{title}\n{url}\n\n"
    
    await ctx.send(message)

@client.command()
async def check_server(ctx):
    try:
        internet_ip, resource_usage, server_status = await utils.check_palworld_server()

        # Set embed color based on server status
        color = 0x2ecc71 if server_status == "STARTED" else 0xe74c3c

        embed = discord.Embed(title="🌐 Palworld Server Status", color=color)
        embed.add_field(name="🔗 Internet IP", value=internet_ip, inline=True)

        # Formatting resource usage for better presentation
        cpu_usage, mem_usage = resource_usage.split("Mem Used:", 1)
        embed.add_field(name="🖥️ CPU Usage", value=cpu_usage, inline=True)
        embed.add_field(name="💾 Memory Usage", value=f"Mem Used: {mem_usage}", inline=True)

        embed.set_footer(text=f"Server Status: {server_status}")
        embed.set_thumbnail(url="https://cdn.vox-cdn.com/uploads/chorus_image/image/73067966/ss_8ef8a16df5e357df5341efdb814192835814107f.0.jpg") 
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)
    except subprocess.CalledProcessError as e:
        await ctx.send(f"Failed to get Palworld Server status: {e}")

@client.command()
@commands.is_owner()
async def restart_server(ctx):
    try:
        returncode, stdout, stderr = await utils.restart_palworld_server()

        if returncode is None:
            await ctx.send("Timeout occurred while restarting the LGSM server.")
            return

        if returncode == 0:
            await ctx.send(f"LGSM server restarted successfully.\n```{stdout}```")
        else:
            await ctx.send(f"Failed to restart LGSM server.\nError:```{stderr}```")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

if __name__ == "__main__":
    client.run(bot_token)