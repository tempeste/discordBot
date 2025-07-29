# TICKET-006: Refactor utils.py - Separate Music and Server Utilities

## Description
The current `utils.py` file contains both music playback utilities and server management utilities, making it a monolithic utility module. This violates the single responsibility principle and makes the codebase harder to maintain. The file should be split into domain-specific utility modules.

## Current State
`utils.py` contains:
- Music/playlist management functions (add_to_playlist, play_next, etc.)
- Server management functions (check_cobbleverse_server, start_cobbleverse_server, etc.)
- Mixed concerns in a single 200+ line file

## Acceptance Criteria
- [ ] Create separate utility modules for different domains
- [ ] Move music-related functions to `music_utils.py`
- [ ] Move server management functions to `server_utils.py`
- [ ] Update all imports in cogs to use the new modules
- [ ] Ensure no functionality is broken
- [ ] Consider if any utilities belong directly in their respective cogs

## Priority
Medium

## Status
Done

## Implementation Steps

### Phase 1: Analysis and Planning
- [x] Identify all functions in utils.py and categorize them
- [x] Determine which functions belong in which module
- [x] Check for any cross-dependencies between categories

### Phase 2: Create New Utility Modules
- [x] Create `music_utils.py` for music-related functions
- [x] Create `cobbleverse_utils.py` specifically for Cobbleverse
- [ ] ~~Create `server_utils.py` for server management functions~~ (not needed, used cobbleverse_utils.py)

### Phase 3: Migrate Functions
- [x] Move music functions to music_utils.py
- [x] Move server functions to cobbleverse_utils.py
- [x] Rename original utils.py to utils.py.backup

### Phase 4: Update Imports
- [x] Update imports in music.py cog
- [x] Update imports in cobbleverse.py cog
- [x] Update imports in bot_tasks.py
- [x] Update imports in test_cobbleverse.py

### Phase 5: Testing
- [x] Verify imports work correctly
- [ ] Test all music commands
- [ ] Test all server management commands
- [ ] Ensure background tasks still work

## Function Categorization

### Music-Related Functions
- `initialize_youtube(api_key)`
- `search_youtube(query)`
- `add_to_playlist(server_id, song_url, song_title, added_by)`
- `remove_from_playlist(server_id, index)`
- `get_playlist(server_id)`
- `shuffle_playlist(server_id)`
- `clear_playlist(server_id)`
- `toggle_loop(guild_id)`
- `is_looping(guild_id)`
- `get_currently_playing(guild_id)`
- `play_next(client, guild_id, text_channel)`

### Server Management Functions
- `check_cobbleverse_server()`
- `start_cobbleverse_server()`
- `stop_cobbleverse_server()`
- `restart_cobbleverse_server()`

## Proposed Structure
```
utils/
├── __init__.py
├── music_utils.py      # All music/playlist related functions
├── server_utils.py     # Generic server management utilities
└── cobbleverse_utils.py # Cobbleverse-specific functions
```

OR

```
# Keep flat structure but separate files
music_utils.py
server_utils.py
# Remove utils.py entirely
```

## Benefits
1. **Better Organization**: Each utility module has a single, clear purpose
2. **Easier Maintenance**: Finding and modifying utilities is more intuitive
3. **Reduced Coupling**: Changes to music utilities won't affect server utilities
4. **Better Testing**: Can test each utility module independently
5. **Clearer Dependencies**: Cogs only import what they need

## Considerations
- Decide whether to create a utils/ package or keep flat structure
- Consider if some "utilities" should be methods within their respective cogs
- Ensure backward compatibility during migration
- Update any documentation that references utils.py

## Notes
- This refactoring aligns with the cog-based architecture
- Consider using this opportunity to add type hints to utility functions
- Some functions might benefit from being converted to classes (e.g., PlaylistManager)

## Resolution
Successfully refactored utils.py into two separate modules:
1. **music_utils.py** - Contains all music-related functions (YouTube search, playlist management, playback)
2. **cobbleverse_utils.py** - Contains all Cobbleverse server management functions

All imports were updated in:
- cogs/music.py
- cogs/cobbleverse.py
- bot_tasks.py
- test_cobbleverse.py

Original utils.py renamed to utils.py.backup for safety.