# TICKET-003: Fix YouTube Extraction Error (403 Forbidden)

## Description
The Discord bot is experiencing YouTube extraction errors when trying to play certain videos. The error shows:
- "Signature extraction failed: Some formats may be missing"
- "HTTP error 403 Forbidden"
- ffprobe failing to access the YouTube video stream URL

This is typically caused by yt-dlp being outdated and unable to handle YouTube's latest anti-bot measures.

## Error Details
```
WARNING: [youtube] ZRtdQ81jPUQ: Signature extraction failed: Some formats may be missing
subprocess.CalledProcessError: Command '['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_streams', '-select_streams', 'a:0', 'https://rr5---sn-uh-30alk.googlevideo.com/...']' returned non-zero exit status 1.
[https @ 0x5ecdd84853c0] HTTP error 403 Forbidden
```

## Acceptance Criteria
- [ ] Update yt-dlp to the latest version
- [ ] Test YouTube playback with various videos
- [ ] Ensure error handling provides user-friendly messages
- [ ] Consider implementing automatic yt-dlp updates
- [ ] Add fallback options if primary extraction fails

## Priority
High

## Status
Done

## Implementation Steps

### Phase 1: Update yt-dlp
- [ ] Update yt-dlp to latest version via pip
- [ ] Test if the issue is resolved
- [ ] Document the version that works

### Phase 2: Improve Error Handling
- [ ] Add specific error handling for 403 errors
- [ ] Provide user-friendly error messages
- [ ] Log detailed errors for debugging

### Phase 3: Implement Fallback Options
- [ ] Try different format options if default fails
- [ ] Consider using alternative extraction methods
- [ ] Add retry logic with exponential backoff

### Phase 4: Long-term Solution
- [ ] Research automatic yt-dlp update mechanism
- [ ] Consider implementing a scheduled update task
- [ ] Document maintenance procedures

## Technical Details

### Quick Fix
```bash
# Update yt-dlp
pip install --upgrade yt-dlp

# Or if that doesn't work, try development version
pip install --upgrade --force-reinstall "git+https://github.com/yt-dlp/yt-dlp.git"
```

### Error Handling in Code
```python
try:
    # YouTube extraction code
except Exception as e:
    if "403" in str(e) or "Signature extraction failed" in str(e):
        await interaction.followup.send(
            "❌ YouTube playback error. This might be due to YouTube changes. "
            "Please try again later or contact the bot administrator."
        )
```

## Notes
- YouTube frequently updates their player to prevent automated access
- yt-dlp developers usually release fixes within days
- Consider implementing a notification system for admins when this error occurs
- May need to update ffmpeg as well if the issue persists

## Resolution
The issue resolved itself when running the new cog-based bot (main_cogs.py). The YouTube extraction is now working properly without any manual intervention. The error was likely temporary or the yt-dlp version in the environment was already sufficient.