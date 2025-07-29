import asyncio
import random
import discord
import yt_dlp

last_searches = {}
playlists = {}
loop_status = {}
currently_playing = {}
original_playlists = {}


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
    if server_id in original_playlists:
        original_playlists[server_id].clear()
    if server_id in currently_playing:
        del currently_playing[server_id]
        
def toggle_loop(guild_id):
    loop_status[guild_id] = not loop_status.get(guild_id, False)
    if loop_status[guild_id]:
        # When enabling loop, save current playlist state
        current_playlist = playlists.get(guild_id, []).copy()
        # If there's a currently playing song, include it at the beginning
        if guild_id in currently_playing:
            current_playlist.insert(0, currently_playing[guild_id])
        original_playlists[guild_id] = current_playlist
    elif not loop_status[guild_id] and guild_id in original_playlists:
        del original_playlists[guild_id]
    return loop_status[guild_id]

def is_looping(guild_id):
    return loop_status.get(guild_id, False)

def get_currently_playing(guild_id):
    return currently_playing.get(guild_id, None)

async def play_next(client, guild_id, text_channel):
    playlist = get_playlist(guild_id)
    
    # Check if playlist is empty
    if not playlist:
        # If looping is enabled and we have an original playlist, restore it
        if is_looping(guild_id) and guild_id in original_playlists and original_playlists[guild_id]:
            playlists[guild_id] = original_playlists[guild_id].copy()
            playlist = get_playlist(guild_id)
        else:
            # No songs to play, disconnect
            voice_client = None
            for vc in client.voice_clients:
                if vc.guild.id == guild_id:
                    voice_client = vc
                    break
            
            if voice_client:
                await voice_client.disconnect()
            
            # Clean up state
            if guild_id in currently_playing:
                del currently_playing[guild_id]
            
            await text_channel.send("Playlist is empty. Disconnected from voice channel.")
            return
    
    # Get the next song from the playlist
    next_song = playlist.pop(0)
    url, title, added_by = next_song
    
    # Store currently playing song
    currently_playing[guild_id] = next_song
    
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
        
        voice_client = None
        for vc in client.voice_clients:
            if vc.guild.id == guild_id:
                voice_client = vc
                break
        
        if voice_client:
            def after_playing(error):
                if error:
                    asyncio.run_coroutine_threadsafe(
                        text_channel.send(f"An error occurred: {str(error)}"), 
                        client.loop
                    )
                asyncio.run_coroutine_threadsafe(play_next(client, guild_id, text_channel), client.loop)

            voice_client.play(source, after=after_playing)
            await text_channel.send(f"Now playing: {title} (added by {added_by})")
        else:
            await text_channel.send("Not connected to a voice channel.")
            # Clean up state
            if guild_id in currently_playing:
                del currently_playing[guild_id]
    except Exception as e:
        await text_channel.send(f"An error occurred while trying to play the next song: {str(e)}")
        # Try to play the next song in case of error
        asyncio.create_task(play_next(client, guild_id, text_channel))