import discord
from discord.ext import commands
import os
import bot_tasks
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()
bot_token = os.getenv("BOT_TOKEN")

# Bot setup
intents = discord.Intents.default()
intents.message_content = True

class DiscordBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents)
    
    async def setup_hook(self):
        # Load all cogs from cogs directory
        cogs_dir = os.path.join(os.path.dirname(__file__), "cogs")
        
        if os.path.exists(cogs_dir):
            for filename in os.listdir(cogs_dir):
                if filename.endswith(".py") and not filename.startswith("__"):
                    cog_name = filename[:-3]
                    try:
                        await self.load_extension(f"cogs.{cog_name}")
                        print(f"Loaded cog: {cog_name}")
                    except Exception as e:
                        print(f"Failed to load cog {cog_name}: {e}")
        
        # Sync slash commands
        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(f"Failed to sync commands: {e}")
    
    async def on_ready(self):
        print('Bot is ready.')
        print(f"Logged in as: {self.user.name}\n")
        # Start background tasks
        bot_tasks.start_update_task(self)

# Create bot instance
bot = DiscordBot()

if __name__ == "__main__":
    bot.run(bot_token)