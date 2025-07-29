# Migration Guide: Transitioning to Cog-Based Architecture

This guide helps you transition from the monolithic `main.py` to the new modular cog-based architecture using `main_cogs.py`.

## Overview of Changes

The Discord bot has been refactored from a single-file architecture to a modular cog-based system:
- **Before**: All 20 commands in `main.py` (427+ lines)
- **After**: Commands organized into 4 cogs in the `cogs/` directory

## New Structure

```
discordBot/
├── main.py          # Original bot (kept for backup)
├── main_cogs.py     # New cog-based bot
├── bot_tasks.py     # Background tasks (unchanged)
├── utils.py         # Shared utilities (unchanged)
└── cogs/           # Command modules
    ├── __init__.py
    ├── music.py     # 11 music commands
    ├── cobbleverse.py # 5 Cobbleverse commands
    └── utility.py   # 4 utility commands
```

## Migration Steps

### 1. Test the New System
Before fully migrating, test that everything works:
```bash
# Run the new cog-based bot
python main_cogs.py
```

### 2. Verify Commands
Check that all commands appear in Discord:
- Music: `/play`, `/pause`, `/skip`, `/queue`, etc.
- Cobbleverse: `/cobbleverse_status`, `/cobbleverse_start`, etc.
- Utility: `/ping`, `/help`

### 3. Developer Commands
The new system includes developer commands (owner-only):
- `!load <cog>` - Load a cog
- `!unload <cog>` - Unload a cog
- `!reload <cog>` - Reload a cog
- `!reloadall` - Reload all cogs
- `!cogs` - List cog status
- `!sync` - Sync slash commands

### 4. Switch Over
Once verified, make `main_cogs.py` your primary bot:
```bash
# Stop the old bot
# Start the new bot
python main_cogs.py
```

### 5. Update Deployment
If using systemd or screen:
```bash
# For screen users
screen -S discordbot
source venv/bin/activate
python main_cogs.py  # Instead of main.py
```

## Key Differences

### Command Names
- Palworld commands have been removed
- Cobbleverse commands remain the same
- Music commands remain the same

### Error Handling
- Better error messages with logging
- Detailed error tracking for debugging

### Development Benefits
- Hot-reload cogs without restarting
- Easier to add new features
- Better code organization

## Troubleshooting

### Commands Not Appearing
1. Use `!sync` to sync commands globally
2. Use `!sync guild` to sync to current guild only
3. Check logs for any loading errors

### Cog Loading Issues
1. Check `!cogs` to see which cogs are loaded
2. Try `!reload <cog>` to reload a specific cog
3. Check console for detailed error messages

### Permission Issues
- Ensure `OWNER_ID` is set correctly in `.env`
- Owner-only commands require the bot owner's Discord ID

## Rollback Plan

If you need to rollback:
1. Stop `main_cogs.py`
2. Start the original `main.py`
3. All commands will work as before

The original `main.py` remains unchanged as a backup.

## Next Steps

After successful migration:
1. Monitor bot performance
2. Add new features as separate cogs
3. Consider removing old `main.py` after a stable period

## Adding New Features

To add new commands:
1. Create a new cog file or add to existing cog
2. Implement commands using `@app_commands.command()`
3. Use `!reload <cog>` to load changes without restarting

Example:
```python
# In cogs/newfeature.py
from discord import app_commands
from discord.ext import commands

class NewFeature(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command()
    async def newcommand(self, interaction: discord.Interaction):
        await interaction.response.send_message("New feature!")

async def setup(bot):
    await bot.add_cog(NewFeature(bot))
```