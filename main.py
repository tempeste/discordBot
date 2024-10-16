import discord
from discord import app_commands
import os
import subprocess
import utils
import bot_tasks
from discord.ext import commands
from dotenv import load_dotenv
from googleapiclient.discovery import build
import asyncio
import yt_dlp
from discord.utils import get

# Load environment variables
load_dotenv()
bot_token = os.getenv("BOT_TOKEN")
gcp_api_key = os.getenv("GCP_API_KEY")
owner_id = os.getenv("OWNER_ID")

# Init client
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(intents=intents, command_prefix='!')

# Init youtube service instance
youtube = None

# Custom check for owner-only commands 
def is_owner():
    async def predicate(interaction: discord.Interaction):
        return interaction.user.id == int(owner_id)
    return app_commands.check(predicate)

@client.event
async def on_ready():
    print('Bot is ready.')
    print(f"Logged in as: {client.user.name}\n")
    await client.tree.sync()
    bot_tasks.start_update_task(client)

@client.tree.command(name="ping", description="Check if the bot is responsive")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message('Pong!')

@client.tree.command(name="join", description="Join a voice channel")
async def join(interaction: discord.Interaction):
    if interaction.user.voice is None:
        await interaction.response.send_message("You are not in a voice channel.")
        return
    channel = interaction.user.voice.channel
    await channel.connect()
    await interaction.response.send_message(f"Joined {channel.name}")

@client.tree.command(name="leave", description="Leave the voice channel")
async def leave(interaction: discord.Interaction):
    if interaction.guild.voice_client is None:
        await interaction.response.send_message("I am not in a voice channel.")
        return
    await interaction.guild.voice_client.disconnect()
    await interaction.response.send_message("Left the voice channel")

@client.tree.command(name="disable_youtube", description="Disable YouTube search")
@is_owner()
async def disable_youtube(interaction: discord.Interaction):
    global youtube
    youtube = None
    await interaction.response.send_message("Youtube search disabled.")

@client.tree.command(name="enable_youtube", description="Enable YouTube search")
@is_owner()
async def enable_youtube(interaction: discord.Interaction):
    global youtube
    youtube = build("youtube", "v3", developerKey=gcp_api_key)
    await interaction.response.send_message("Youtube search enabled.")

@client.tree.command(name="search", description="Search for YouTube videos")
async def search(interaction: discord.Interaction, search_query: str):
    global youtube  # Make sure we're using the global youtube object

    if youtube is None:
        await interaction.response.send_message("YouTube search is currently disabled. Please enable it first with /enable_youtube command.")
        return

    response = utils.search_youtube(youtube, search_query, interaction.user.id)

    if not response or "items" not in response:
        await interaction.response.send_message("No results found or an error occurred.")
        return

    message = "Top 5 results found:\n"
    for i, item in enumerate(response.get("items", [])[:5], start=1):
        title = item["snippet"]["title"]
        video_id = item["id"]["videoId"]
        url = f"<https://www.youtube.com/watch?v={video_id}>"  # Use < > to prevent embedding
        message += f"{i}. {title}\n{url}\n\n"
    
    message += "To play a video, use the /play command with the number of the video (e.g., /play 1) or the full URL."
    await interaction.response.send_message(message)


@client.tree.command(name="play", description="Play a YouTube video or add it to the playlist")
@app_commands.describe(query="Enter a search query, video number from search results, or YouTube URL")
async def play(interaction: discord.Interaction, query: str):
    global youtube  # Make sure we're using the global youtube object

    if interaction.user.voice is None:
        await interaction.response.send_message("You need to be in a voice channel to use this command.")
        return

    await interaction.response.defer()

    voice_client = interaction.guild.voice_client
    if not voice_client:
        voice_channel = interaction.user.voice.channel
        voice_client = await voice_channel.connect()

    # Check if query is a number (referring to search results)
    if query.isdigit() and 1 <= int(query) <= 5:
        last_search = utils.get_last_search(interaction.user.id)
        if not last_search:
            await interaction.followup.send("Please use the /search command first.")
            return
        video_url = last_search[int(query) - 1]
    elif query.startswith("https://"):
        video_url = query
    else:
        # Treat as a new search query
        if youtube is None:
            await interaction.followup.send("YouTube search is currently disabled. Please enable it first with /enable_youtube command.")
            return
        
        search_response = utils.search_youtube(youtube, query, interaction.user.id)
        if not search_response or "items" not in search_response:
            await interaction.followup.send("No results found or an error occurred.")
            return
        video_url = f"https://www.youtube.com/watch?v={search_response['items'][0]['id']['videoId']}"

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            title = info['title']
        
        utils.add_to_playlist(interaction.guild.id, video_url, title, interaction.user.name)
        
        if not voice_client.is_playing():
            await utils.play_next(client, interaction.guild.id, interaction.channel)
            await interaction.followup.send(f"Now playing: {title}\nAdded to server playlist by {interaction.user.name}")
        else:
            await interaction.followup.send(f"Added to playlist: {title} (added by {interaction.user.name})")
    except Exception as e:
        await interaction.followup.send(f"An error occurred while trying to play/add the video: {str(e)}")
        
@client.tree.command(name="pause", description="Pause the currently playing audio")
async def pause(interaction: discord.Interaction):
    voice_client = get(client.voice_clients, guild=interaction.guild)
    if voice_client and voice_client.is_playing():
        voice_client.pause()
        await interaction.response.send_message("Paused the audio.")
    else:
        await interaction.response.send_message("No audio is currently playing.")

@client.tree.command(name="resume", description="Resume paused audio")
async def resume(interaction: discord.Interaction):
    voice_client = get(client.voice_clients, guild=interaction.guild)
    if voice_client and voice_client.is_paused():
        voice_client.resume()
        await interaction.response.send_message("Resumed the audio.")
    else:
        await interaction.response.send_message("No audio is paused.")

@client.tree.command(name="skip", description="Skip the current song")
async def skip(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if voice_client and voice_client.is_playing():
        voice_client.stop()
        await interaction.response.send_message("Skipped the current song.")
        await utils.play_next(client, interaction.guild.id, interaction.channel)
    else:
        await interaction.response.send_message("No song is currently playing.")

@client.tree.command(name="view_playlist", description="View the server's playlist")
async def view_playlist(interaction: discord.Interaction):
    playlist = utils.get_playlist(interaction.guild.id)
    if not playlist:
        await interaction.response.send_message("The server playlist is empty.")
        return

    message = "Server playlist:\n"
    for i, (url, title, added_by) in enumerate(playlist, start=1):
        message += f"{i}. {title} (added by {added_by})\n<{url}>\n\n"
    
    await interaction.response.send_message(message)

@client.tree.command(name="shuffle_playlist", description="Shuffle the server's playlist")
async def shuffle_playlist(interaction: discord.Interaction):
    utils.shuffle_playlist(interaction.guild.id)
    await interaction.response.send_message("The server playlist has been shuffled.")
    await view_playlist(interaction)

@client.tree.command(name="remove_from_playlist", description="Remove a song from the server's playlist")
@app_commands.describe(index="The number of the song to remove")
async def remove_from_playlist(interaction: discord.Interaction, index: int):
    removed = utils.remove_from_playlist(interaction.guild.id, index - 1)
    if removed:
        await interaction.response.send_message(f"Removed '{removed[1]}' from the server playlist.")
    else:
        await interaction.response.send_message("Invalid index or the server playlist is empty.")

@client.tree.command(name="clear_playlist", description="Clear the server's playlist")
async def clear_playlist(interaction: discord.Interaction):
    utils.clear_playlist(interaction.guild.id)
    await interaction.response.send_message("The server playlist has been cleared.")

@client.tree.command(name="loop", description="Toggle looping of the current playlist")
async def loop(interaction: discord.Interaction):
    is_looping = utils.toggle_loop(interaction.guild.id)
    if is_looping:
        await interaction.response.send_message("Playlist looping is now ON.")
    else:
        await interaction.response.send_message("Playlist looping is now OFF.")

@client.tree.command(name="stop", description="Stop playing audio and disconnect")
async def stop(interaction: discord.Interaction):
    voice_client = get(client.voice_clients, guild=interaction.guild)
    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()
        await interaction.response.send_message("Disconnected from voice channel and stopped playing.")
    else:
        await interaction.response.send_message("I'm not connected to a voice channel.")

@client.tree.command(name="check_server", description="Check Palworld server status")
async def check_server(interaction: discord.Interaction):
    try:
        internet_ip, cpu_usage, mem_usage, server_status = await utils.check_palworld_server()

        color = 0x2ecc71 if server_status == "STARTED" else 0xe74c3c
        thumbnail_url = "https://static.wikia.nocookie.net/palworld/images/3/3e/Screen_%281%29.jpg/revision/latest/scale-to-width-down/1200?cb=20210911235311" if server_status == "STARTED" else "https://cdn.vox-cdn.com/uploads/chorus_image/image/73067966/ss_8ef8a16df5e357df5341efdb814192835814107f.0.jpg"

        embed = discord.Embed(title="🌐 Palworld Server Status", color=color)
        embed.add_field(name="🔗 Internet IP", value=internet_ip, inline=True)
        embed.add_field(name="🖥️ CPU Usage", value=cpu_usage, inline=True)
        embed.add_field(name="💾 Memory Usage", value=mem_usage, inline=True)

        embed.set_footer(text=f"Server Status: {server_status}")
        embed.set_thumbnail(url=thumbnail_url)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url if interaction.user.avatar else None)

        await interaction.response.send_message(embed=embed)
    except subprocess.CalledProcessError as e:
        await interaction.response.send_message(f"Failed to get Palworld Server status: {e}")

@client.tree.command(name="restart_server", description="Restart the Palworld server")
@is_owner()
async def restart_server(interaction: discord.Interaction):
    try:
        await interaction.response.defer()
        returncode, stdout, stderr = await utils.restart_palworld_server()

        if returncode is None:
            await interaction.followup.send("Timeout occurred while restarting the LGSM server.")
            return

        if returncode == 0:
            await interaction.followup.send(f"LGSM server restarted successfully.\n```{stdout}```")
        else:
            await interaction.followup.send(f"Failed to restart LGSM server.\nError:```{stderr}```")
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {e}")

@client.tree.command(name="stop_server", description="Stop the Palworld server")
@is_owner()
async def stop_server(interaction: discord.Interaction):
    try:
        await interaction.response.defer()
        returncode, stdout, stderr = await utils.stop_palworld_server()

        if returncode is None:
            await interaction.followup.send("Timeout occurred while stopping the LGSM server.")
            return

        if returncode == 0:
            await interaction.followup.send(f"LGSM server stopped successfully.\n```{stdout}```")
        else:
            await interaction.followup.send(f"Failed to stop LGSM server.\nError:```{stderr}```")
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {e}")

@client.tree.command(name="start_server", description="Start the Palworld server")
async def start_server(interaction: discord.Interaction):
    try:
        await interaction.response.defer()
        returncode, stdout, stderr = await utils.start_palworld_server()

        if returncode is None:
            await interaction.followup.send("Timeout occurred while starting the LGSM server.")
            return

        if returncode == 0:
            await interaction.followup.send(f"LGSM server started successfully.\n```{stdout}```")
        else:
            await interaction.followup.send(f"Failed to start LGSM server.\nError:```{stderr}```")
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {e}")

if __name__ == "__main__":
    client.run(bot_token)