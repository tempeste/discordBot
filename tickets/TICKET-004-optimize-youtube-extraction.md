# TICKET-004: Optimize YouTube Extraction to Avoid Duplicate API Calls

## Description
The bot is currently making duplicate YouTube extraction calls for each video:
1. Once in `music.py` to get the video title
2. Again in `utils.py` when actually playing the video

This results in unnecessary API calls, slower response times, and excessive console output showing multiple JSON downloads for the same video.

## Current Behavior
```
[youtube] fSS96c2u_wU: Downloading tv client config
[youtube] fSS96c2u_wU: Downloading tv player API JSON
[youtube] fSS96c2u_wU: Downloading ios player API JSON
[youtube] fSS96c2u_wU: Downloading m3u8 information
[youtube] Extracting URL: https://www.youtube.com/watch?v=fSS96c2u_wU
[youtube] fSS96c2u_wU: Downloading webpage
[youtube] fSS96c2u_wU: Downloading tv client config
[youtube] fSS96c2u_wU: Downloading player 0b00c3eb-main
[youtube] fSS96c2u_wU: Downloading tv player API JSON
[youtube] fSS96c2u_wU: Downloading ios player API JSON
```

## Acceptance Criteria
- [ ] YouTube info should be extracted only once per video
- [ ] Extracted info should be cached or stored with the playlist entry
- [ ] Reduce API calls and improve response time
- [ ] Clean up console output to show extraction happening only once

## Priority
Medium

## Status
Todo

## Implementation Options

### Option 1: Cache Extracted Info in Playlist
Store the extracted info dict in the playlist instead of just the URL:
```python
# Instead of storing: (url, title, added_by)
# Store: (url, title, added_by, info_dict)
```

### Option 2: Use yt-dlp's Built-in Caching
Configure yt-dlp to use its cache directory:
```python
ydl_opts = {
    'cachedir': '/path/to/cache',
    'format': 'bestaudio/best',
    # ...
}
```

### Option 3: Extract Only When Playing
Remove the extraction from the play command entirely and only extract when actually playing.

### Option 4: Implement Custom Caching Layer
Create a simple in-memory cache with TTL for extracted info.

## Technical Details

### Current Flow
1. User runs `/play <url>`
2. `music.py` extracts info to get title
3. Adds URL to playlist
4. When playing, `utils.py` extracts info again to get stream URL

### Proposed Flow
1. User runs `/play <url>`
2. `music.py` extracts info once
3. Store relevant info (title, formats, etc.) with playlist entry
4. When playing, use stored info instead of re-extracting

## Benefits
- Faster response times
- Reduced YouTube API usage
- Cleaner console output
- Better user experience
- Less chance of rate limiting

## Notes
- Stream URLs from YouTube expire after a few hours, so long-term caching needs consideration
- Consider memory usage if caching full info dicts
- May need to handle cache invalidation for long playlists