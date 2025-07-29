import discord
from discord.ext import commands
from discord import app_commands
from utils import music_utils
import yt_dlp
from discord.utils import get
import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()
gcp_api_key = os.getenv("GCP_API_KEY")

def is_owner():
    """Custom check for owner-only commands"""
    async def predicate(interaction: discord.Interaction):
        owner_id = int(os.getenv("OWNER_ID"))
        return interaction.user.id == owner_id
    return app_commands.check(predicate)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.youtube = None
        
    async def cog_load(self):
        if gcp_api_key:
            self.youtube = build("youtube", "v3", developerKey=gcp_api_key)
    
    @app_commands.command(name="join", description="Join a voice channel")
    async def join(self, interaction: discord.Interaction):
        if interaction.user.voice is None:
            await interaction.response.send_message("You are not in a voice channel.")
            return
        channel = interaction.user.voice.channel
        await channel.connect()
        await interaction.response.send_message(f"Joined {channel.name}")
    
    @app_commands.command(name="leave", description="Leave the voice channel")
    async def leave(self, interaction: discord.Interaction):
        if interaction.guild.voice_client is None:
            await interaction.response.send_message("I am not in a voice channel.")
            return
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("Left the voice channel")
    
    @app_commands.command(name="disable_youtube", description="Disable YouTube search")
    @is_owner()
    async def disable_youtube(self, interaction: discord.Interaction):
        self.youtube = None
        await interaction.response.send_message("Youtube search disabled.")
    
    @app_commands.command(name="enable_youtube", description="Enable YouTube search")
    @is_owner()
    async def enable_youtube(self, interaction: discord.Interaction):
        self.youtube = build("youtube", "v3", developerKey=gcp_api_key)
        await interaction.response.send_message("Youtube search enabled.")
    
    @app_commands.command(name="search", description="Search for YouTube videos")
    async def search(self, interaction: discord.Interaction, search_query: str):
        if self.youtube is None:
            await interaction.response.send_message("YouTube search is currently disabled. Please enable it first with /enable_youtube command.")
            return
        
        response = music_utils.search_youtube(self.youtube, search_query, interaction.user.id)
        
        if not response or "items" not in response:
            await interaction.response.send_message("No results found or an error occurred.")
            return
        
        message = "Top 5 results found:\n"
        for i, item in enumerate(response.get("items", [])[:5], start=1):
            title = item["snippet"]["title"]
            video_id = item["id"]["videoId"]
            url = f"<https://www.youtube.com/watch?v={video_id}>"
            message += f"{i}. {title}\n{url}\n\n"
        
        message += "To play a video, use the /play command with the number of the video (e.g., /play 1) or the full URL."
        await interaction.response.send_message(message)
    
    @app_commands.command(name="play", description="Play a YouTube video or add it to the playlist")
    @app_commands.describe(query="Enter a search query, video number from search results, or YouTube URL")
    async def play(self, interaction: discord.Interaction, query: str):
        if interaction.user.voice is None:
            await interaction.response.send_message("You need to be in a voice channel to use this command.")
            return
        
        await interaction.response.defer()
        
        voice_client = interaction.guild.voice_client
        if not voice_client:
            voice_channel = interaction.user.voice.channel
            voice_client = await voice_channel.connect()
        
        if query.isdigit() and 1 <= int(query) <= 5:
            last_search = music_utils.get_last_search(interaction.user.id)
            if not last_search:
                await interaction.followup.send("Please use the /search command first.")
                return
            video_url = last_search[int(query) - 1]
        elif query.startswith("https://"):
            video_url = query
        else:
            if self.youtube is None:
                await interaction.followup.send("YouTube search is currently disabled. Please enable it first with /enable_youtube command.")
                return
            
            search_response = music_utils.search_youtube(self.youtube, query, interaction.user.id)
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
            
            music_utils.add_to_playlist(interaction.guild.id, video_url, title, interaction.user.name)
            
            if not voice_client.is_playing():
                await music_utils.play_next(self.bot, interaction.guild.id, interaction.channel)
                await interaction.followup.send(f"Now playing: {title}\nAdded to server playlist by {interaction.user.name}")
            else:
                await interaction.followup.send(f"Added to playlist: {title} (added by {interaction.user.name})")
        except Exception as e:
            await interaction.followup.send(f"An error occurred while trying to play/add the video: {str(e)}")
    
    @app_commands.command(name="pause", description="Pause the currently playing audio")
    async def pause(self, interaction: discord.Interaction):
        voice_client = get(self.bot.voice_clients, guild=interaction.guild)
        if voice_client and voice_client.is_playing():
            voice_client.pause()
            await interaction.response.send_message("Paused the audio.")
        else:
            await interaction.response.send_message("No audio is currently playing.")
    
    @app_commands.command(name="resume", description="Resume paused audio")
    async def resume(self, interaction: discord.Interaction):
        voice_client = get(self.bot.voice_clients, guild=interaction.guild)
        if voice_client and voice_client.is_paused():
            voice_client.resume()
            await interaction.response.send_message("Resumed the audio.")
        else:
            await interaction.response.send_message("No audio is paused.")
    
    @app_commands.command(name="skip", description="Skip the current song")
    async def skip(self, interaction: discord.Interaction):
        voice_client = interaction.guild.voice_client
        if voice_client and voice_client.is_playing():
            await interaction.response.defer()
            voice_client.stop()
            # Note: play_next will be called automatically by the after callback
            await interaction.followup.send("Skipped the current song.")
        else:
            await interaction.response.send_message("No song is currently playing.")
    
    @app_commands.command(name="view_playlist", description="View the server's playlist")
    async def view_playlist(self, interaction: discord.Interaction):
        current = music_utils.get_currently_playing(interaction.guild.id)
        playlist = music_utils.get_playlist(interaction.guild.id)
        
        if not current and not playlist:
            await interaction.response.send_message("The server playlist is empty.")
            return
        
        message = ""
        
        # Show currently playing song
        if current:
            _, title, added_by = current
            message += f"**Currently Playing:**\n{title} (added by {added_by})\n\n"
        
        # Show upcoming songs
        if playlist:
            message += "**Up Next:**\n"
            for i, (url, title, added_by) in enumerate(playlist, start=1):
                message += f"{i}. {title} (added by {added_by})\n<{url}>\n\n"
        else:
            message += "*No songs in queue*\n"
        
        # Show loop status
        if music_utils.is_looping(interaction.guild.id):
            message += "\n🔁 **Loop mode is ON**"
        
        await interaction.response.send_message(message)
    
    @app_commands.command(name="shuffle_playlist", description="Shuffle the server's playlist")
    async def shuffle_playlist(self, interaction: discord.Interaction):
        music_utils.shuffle_playlist(interaction.guild.id)
        await interaction.response.send_message("The server playlist has been shuffled.")
        playlist = music_utils.get_playlist(interaction.guild.id)
        if playlist:
            message = "Server playlist:\n"
            for i, (url, title, added_by) in enumerate(playlist, start=1):
                message += f"{i}. {title} (added by {added_by})\n<{url}>\n\n"
            await interaction.channel.send(message)
    
    @app_commands.command(name="remove_from_playlist", description="Remove a song from the server's playlist")
    @app_commands.describe(index="The number of the song to remove")
    async def remove_from_playlist(self, interaction: discord.Interaction, index: int):
        removed = music_utils.remove_from_playlist(interaction.guild.id, index - 1)
        if removed:
            await interaction.response.send_message(f"Removed '{removed[1]}' from the server playlist.")
        else:
            await interaction.response.send_message("Invalid index or the server playlist is empty.")
    
    @app_commands.command(name="clear_playlist", description="Clear the server's playlist")
    async def clear_playlist(self, interaction: discord.Interaction):
        utils.clear_playlist(interaction.guild.id)
        await interaction.response.send_message("The server playlist has been cleared.")
    
    @app_commands.command(name="loop", description="Toggle looping of the current playlist")
    async def loop(self, interaction: discord.Interaction):
        is_looping = music_utils.toggle_loop(interaction.guild.id)
        if is_looping:
            await interaction.response.send_message("Playlist looping is now ON.")
        else:
            await interaction.response.send_message("Playlist looping is now OFF.")
    
    @app_commands.command(name="now_playing", description="Show the currently playing song")
    async def now_playing(self, interaction: discord.Interaction):
        current = music_utils.get_currently_playing(interaction.guild.id)
        if current:
            url, title, added_by = current
            voice_client = interaction.guild.voice_client
            status = "⏸️ Paused" if voice_client and voice_client.is_paused() else "▶️ Playing"
            
            embed = discord.Embed(
                title="Now Playing",
                description=f"{status}\n\n**{title}**\n\nAdded by: {added_by}\n[Link]({url})",
                color=discord.Color.blue()
            )
            
            if music_utils.is_looping(interaction.guild.id):
                embed.set_footer(text="🔁 Loop mode is ON")
            
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No song is currently playing.")
    
    @app_commands.command(name="stop", description="Stop playing audio and disconnect")
    async def stop(self, interaction: discord.Interaction):
        voice_client = get(self.bot.voice_clients, guild=interaction.guild)
        if voice_client and voice_client.is_connected():
            # Stop playback
            if voice_client.is_playing():
                voice_client.stop()
            
            # Clear playlist and state
            music_utils.clear_playlist(interaction.guild.id)
            
            # Disconnect
            await voice_client.disconnect()
            await interaction.response.send_message("Disconnected from voice channel and stopped playing.")
        else:
            await interaction.response.send_message("I'm not connected to a voice channel.")

async def setup(bot):
    await bot.add_cog(Music(bot))