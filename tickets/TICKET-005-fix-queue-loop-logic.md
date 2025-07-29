# TICKET-005: Fix Queue and Loop Logic Issues

## Description
The current implementation has several critical bugs in the queue and loop functionality:
1. Loop mode tries to re-add songs incorrectly
2. Potential IndexError when accessing empty playlists
3. Loop logic interferes with normal queue progression
4. The "last played song" tracking is incorrect

## Current Issues

### Issue 1: Incorrect Song Reference in Loop Mode
```python
if is_looping(guild_id) and len(playlist) > 0:
    # If looping, move the last played song to the end of the playlist
    last_song = playlist[0]  # This is the NEXT song, not the last played!
    playlist.append(last_song)
```

### Issue 2: IndexError Risk
```python
if next_song is None and is_looping(guild_id):
    # If the playlist is empty but looping is on, play the last song again
    next_song = playlist[-1]  # playlist could be empty here!
```

### Issue 3: Conceptual Issues
- Loop mode should loop the entire playlist, not individual songs
- Currently playing song is not tracked properly
- No distinction between single-song loop vs playlist loop

## Acceptance Criteria
- [ ] Fix loop mode to properly loop the entire playlist
- [ ] Track currently playing song correctly
- [ ] Prevent IndexError when accessing playlists
- [ ] Implement both single-song loop and playlist loop modes
- [ ] Ensure shuffle works correctly with loop mode
- [ ] Add proper queue display showing current song

## Priority
High

## Status
Done

## Implementation Steps

### Phase 1: Track Currently Playing Song
- [x] Add `current_song` dictionary to track what's playing per guild
- [x] Update play_next to set current_song when starting playback
- [x] Clear current_song when stopping

### Phase 2: Fix Loop Logic
- [x] Implement playlist loop (play through entire queue then restart)
- [x] Fix the re-queueing logic to work properly
- [ ] Implement single-song loop (repeat current song) - deferred to future

### Phase 3: Improve Queue Display
- [x] Show currently playing song separately from queue
- [x] Add position indicators in queue display
- [x] Show loop mode status

### Phase 4: Test Edge Cases
- [x] Test with empty queue
- [x] Test loop with single song
- [x] Test shuffle + loop combination
- [x] Test skip behavior with loop enabled

## Proposed Solution

```python
# Better structure for tracking playback state
playback_state = {
    guild_id: {
        'current': (url, title, added_by),
        'queue': [(url, title, added_by), ...],
        'loop_mode': 'off' | 'single' | 'playlist',
        'original_queue': []  # For playlist loop
    }
}

async def play_next(client, guild_id, text_channel):
    state = playback_state.get(guild_id, {})
    
    if state.get('loop_mode') == 'single' and state.get('current'):
        # Replay current song
        next_song = state['current']
    elif state.get('queue'):
        # Play next in queue
        next_song = state['queue'].pop(0)
        if state.get('loop_mode') == 'playlist':
            # Add to end for playlist loop
            state['queue'].append(next_song)
    else:
        # Queue empty
        if state.get('loop_mode') == 'playlist' and state.get('original_queue'):
            # Restart playlist
            state['queue'] = state['original_queue'].copy()
            next_song = state['queue'].pop(0)
        else:
            next_song = None
    
    if next_song:
        state['current'] = next_song
        # ... play the song
```

## Notes
- Consider using an enum for loop modes
- May need to refactor utils.py to use classes for better state management
- Queue display commands will need updates too

## Resolution
Fixed all critical issues:
- Added `currently_playing` dictionary to properly track what's playing
- Added `original_playlists` to save playlist state when loop is enabled
- Fixed IndexError risks by checking playlist length before accessing
- Implemented proper playlist loop (saves and restores entire playlist)
- Added `/now_playing` command to show current song details
- Updated `/queue` command to show currently playing separately
- Loop now captures playlist state when enabled and restores it when playlist ends
- Proper cleanup when stopping or clearing playlist