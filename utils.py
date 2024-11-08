import subprocess
import re
import asyncio
import random
import discord
import yt_dlp

last_searches = {}
playlists = {}
loop_status = {}

async def check_palworld_server():
    try:
        command = "/home/pwserver/pwserver details"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        status_output = result.stdout

        # If the command failed but we got output in stderr
        if result.returncode != 0:
            return (
                "Error", 
                "N/A", 
                "N/A", 
                "STOPPED" if "not running" in result.stderr.lower() else "ERROR"
            )

        # Remove ANSI escape codes for more reliable regex matching
        ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
        cleaned_output = ansi_escape.sub('', status_output)

        # Extracting the sections
        internet_ip = re.search(r"Internet IP:\s*(.+)", cleaned_output)
        cpu_usage = re.search(r"CPU Used:\s*(.+?)%", cleaned_output)
        mem_usage = re.search(r"Mem Used:\s*(.+)%", cleaned_output)
        server_status_search = re.search(r"Status:\s*(\w+)", cleaned_output)

        internet_ip = internet_ip.group(1) if internet_ip else "Not Found"
        cpu_usage = f"CPU Used: {cpu_usage.group(1)}%" if cpu_usage else "Not Found"
        mem_usage = f"Mem Used: {mem_usage.group(1)}%" if mem_usage else "Not Found"
        server_status = server_status_search.group(1) if server_status_search else "Not Found"

        return internet_ip, cpu_usage, mem_usage, server_status

    except Exception as e:
        return f"Error: {str(e)}", "N/A", "N/A", "ERROR"

async def restart_palworld_server():
    command = "/home/pwserver/pwserver restart"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    try:
        stdout, stderr = await asyncio.wait_for(asyncio.to_thread(process.communicate), timeout=120)  # Timeout in seconds
        return process.returncode, stdout, stderr
    except asyncio.TimeoutError:
        return None, None, "Timeout"
    
async def start_palworld_server():
    command = "/home/pwserver/pwserver start"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    try:
        stdout, stderr = await asyncio.wait_for(asyncio.to_thread(process.communicate), timeout=120)  # Timeout in seconds
        return process.returncode, stdout, stderr
    except asyncio.TimeoutError:
        return None, None, "Timeout"
    
async def stop_palworld_server():
    command = "/home/pwserver/pwserver stop"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    try:
        stdout, stderr = await asyncio.wait_for(asyncio.to_thread(process.communicate), timeout=120)  # Timeout in seconds
        return process.returncode, stdout, stderr
    except asyncio.TimeoutError:
        return None, None, "Timeout"

def search_youtube(youtube, search_query, user_id):
    request = youtube.search().list(
        part="snippet",
        q=search_query,
        maxResults=5,
        type="video"
    )
    response = request.execute()
    
    if "items" in response:
        video_urls = [f"https://www.youtube.com/watch?v={item['id']['videoId']}" for item in response['items']]
        last_searches[user_id] = video_urls
    
    return response

def get_last_search(user_id):
    return last_searches.get(user_id, [])

def add_to_playlist(server_id, song_url, song_title, added_by):
    if server_id not in playlists:
        playlists[server_id] = []
    playlists[server_id].append((song_url, song_title, added_by))

def remove_from_playlist(server_id, index):
    if server_id in playlists and 0 <= index < len(playlists[server_id]):
        return playlists[server_id].pop(index)
    return None

def get_playlist(server_id):
    return playlists.get(server_id, [])

def shuffle_playlist(server_id):
    if server_id in playlists:
        random.shuffle(playlists[server_id])

def clear_playlist(server_id):
    if server_id in playlists:
        playlists[server_id].clear()
        
def toggle_loop(guild_id):
    loop_status[guild_id] = not loop_status.get(guild_id, False)
    return loop_status[guild_id]

def is_looping(guild_id):
    return loop_status.get(guild_id, False)
        
async def play_next(client, guild_id, text_channel):
    playlist = get_playlist(guild_id)
    if playlist or is_looping(guild_id):
        if is_looping(guild_id) and len(playlist) > 0:
            # If looping, move the last played song to the end of the playlist
            last_song = playlist[0]
            playlist.append(last_song)
        
        next_song = playlist.pop(0) if playlist else None
        
        if next_song is None and is_looping(guild_id):
            # If the playlist is empty but looping is on, play the last song again
            next_song = playlist[-1]
        
        if next_song:
            url, title, added_by = next_song
            
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
                    info = ydl.extract_info(url, download=False)
                    url2 = info['url']
                    source = await discord.FFmpegOpusAudio.from_probe(url2, **{'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'})
                
                voice_client = discord.utils.get(client.voice_clients, guild__id=guild_id)
                if voice_client:
                    def after_playing(error):
                        asyncio.run_coroutine_threadsafe(play_next(client, guild_id, text_channel), client.loop)

                    voice_client.play(source, after=after_playing)
                    await text_channel.send(f"Now playing: {title} (added by {added_by})")
                else:
                    await text_channel.send("Not connected to a voice channel.")
            except Exception as e:
                await text_channel.send(f"An error occurred while trying to play the next song: {str(e)}")
        else:
            voice_client = discord.utils.get(client.voice_clients, guild__id=guild_id)
            if voice_client:
                await voice_client.disconnect()
            await text_channel.send("Playlist is empty and looping is off. Disconnected from voice channel.")
    else:
        voice_client = discord.utils.get(client.voice_clients, guild__id=guild_id)
        if voice_client:
            await voice_client.disconnect()
        await text_channel.send("Playlist is empty and looping is off. Disconnected from voice channel.")