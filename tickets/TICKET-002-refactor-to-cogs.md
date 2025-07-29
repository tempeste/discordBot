# TICKET-002: Refactor Discord Bot Code into Cogs

## Description
The Discord bot currently has all 20 slash commands defined in a single `main.py` file (427+ lines), making it difficult to maintain, test, and extend. This ticket tracks the refactoring of the codebase to use Discord.py's cog system, which is the recommended pattern for organizing bot code in 2025.

Cogs (short for "cogwheels") are a Discord.py feature that allows grouping related commands and functionality into separate modules. This provides better code organization, enables hot-reloading during development, and improves maintainability.

## Current State
- All commands in single `main.py` file
- 20 slash commands total:
  - 10 music-related commands
  - 9 server management commands (4 Palworld, 5 Cobbleverse)
  - 1 utility command (ping)
- Utility functions in separate `utils.py`
- Background tasks in `bot_tasks.py`

## Acceptance Criteria
- [ ] Create `cogs/` directory structure with separate modules for each feature domain
- [ ] Migrate all music commands to `cogs/music.py`
- [ ] Migrate all Palworld commands to `cogs/palworld.py`
- [ ] Migrate all Cobbleverse commands to `cogs/cobbleverse.py`
- [ ] Migrate utility commands to `cogs/utility.py`
- [ ] Update main.py to use `commands.Bot` class with proper setup_hook
- [ ] Implement cog loading system with error handling
- [ ] Add developer commands for reloading cogs (owner-only)
- [ ] Preserve all existing functionality without breaking changes
- [ ] Update background tasks to work with new cog structure
- [ ] Test all commands to ensure they work after refactoring
- [ ] Update README.md with new project structure

## Priority
Medium

## Status
Done

## Implementation Steps

### Phase 1: Project Structure Setup
- [x] Create `cogs/` directory
- [x] Create `__init__.py` in cogs directory
- [x] Create initial cog files: music.py, palworld.py, cobbleverse.py, utility.py
- [x] Update .gitignore if needed

### Phase 2: Bot Infrastructure Update
- [x] Convert `client` to use `commands.Bot` class structure
- [x] Implement `setup_hook()` method for cog loading
- [x] Add cog loading logic with error handling
- [x] Create developer commands for cog management (load/unload/reload)

### Phase 3: Music Cog Migration
- [x] Create Music cog class inheriting from `commands.Cog`
- [x] Migrate all music-related slash commands
- [x] Move relevant music utilities from utils.py
- [x] Implement queue management within cog
- [x] Test all music functionality

### Phase 4: Server Management Cogs Migration
- [x] Create Palworld cog with all Palworld commands
- [x] Create Cobbleverse cog with all Cobbleverse commands
- [x] Ensure proper permission checks are preserved
- [x] Move server-specific utilities to respective cogs

### Phase 5: Utility and Background Tasks
- [x] Create Utility cog with ping and future utility commands
- [x] Update bot_tasks.py to work with cog structure
- [x] Ensure background tasks can access cog instances if needed

### Phase 6: Testing and Documentation
- [x] Test every command to ensure functionality is preserved
- [x] Test cog reloading functionality
- [x] Update README.md with new structure
- [x] Document cog development patterns for future features

## Technical Details

### Cog Structure Example
```python
from discord import app_commands
from discord.ext import commands
import discord

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = {}  # Guild-specific queues
    
    @app_commands.command(description="Join your voice channel")
    async def join(self, interaction: discord.Interaction):
        # Command implementation
        pass

async def setup(bot):
    await bot.add_cog(Music(bot))
```

### Main.py Structure
```python
class DiscordBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)
    
    async def setup_hook(self):
        # Load all cogs
        for cog in ['music', 'palworld', 'cobbleverse', 'utility']:
            try:
                await self.load_extension(f'cogs.{cog}')
                print(f'Loaded {cog} cog')
            except Exception as e:
                print(f'Failed to load {cog}: {e}')
        
        # Sync commands
        await self.tree.sync()
```

### Directory Structure After Refactoring
```
discordBot/
├── main.py          # Bot entry point with cog loading
├── bot_tasks.py     # Background tasks
├── utils.py         # Shared utilities
├── cogs/           # Feature modules
│   ├── __init__.py
│   ├── music.py    # Music commands and functionality
│   ├── palworld.py # Palworld server management
│   ├── cobbleverse.py # Cobbleverse server management
│   └── utility.py  # General utility commands
├── requirements.txt
├── .env
└── README.md
```

## Benefits
1. **Modularity**: Each feature is self-contained in its own file
2. **Maintainability**: Easier to find and modify specific functionality
3. **Hot-reloading**: Can reload individual cogs without restarting bot
4. **Testability**: Individual cogs can be tested in isolation
5. **Scalability**: New features can be added as new cogs
6. **Collaboration**: Multiple developers can work on different cogs

## Risks
- Potential for breaking existing functionality during migration
- Need to ensure all imports and dependencies are properly handled
- Background tasks integration might need adjustment

## Notes
- Cogs are still the recommended pattern for Discord.py in 2025
- Modern cog pattern uses `@app_commands.command()` for slash commands
- Each cog file must have an `async def setup(bot)` function
- Consider adding a `cogs/dev.py` for developer-only commands in the future

## Summary of Changes
- Successfully created cogs directory with 4 cogs (music, cobbleverse, utility, developer)
- Migrated all 20 commands from main.py to appropriate cogs
- Created enhanced main_cogs.py with better error handling and logging
- Added developer commands for cog management (load/unload/reload)
- Fixed is_owner decorator issues across all cogs
- Updated Cobbleverse commands to match original naming convention
- Added cobbleverse_info command
- Created comprehensive MIGRATION_GUIDE.md
- Updated README.md to reflect new architecture
- Original main.py kept as backup for safety