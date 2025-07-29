import discord
from discord.ext import commands
import os
import bot_tasks
from dotenv import load_dotenv
import asyncio
import logging
import traceback
from typing import Optional

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('discord_bot')

# Load environment variables
load_dotenv()
bot_token = os.getenv("BOT_TOKEN")

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True

class DiscordBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None,
            description="A versatile Discord bot with music and server management features"
        )
        self.initial_extensions = []
        self.failed_cogs = {}
        
    async def setup_hook(self):
        """Load all cogs and sync slash commands"""
        logger.info("Starting bot setup...")
        
        # Load all cogs from cogs directory
        cogs_dir = os.path.join(os.path.dirname(__file__), "cogs")
        
        if os.path.exists(cogs_dir):
            for filename in os.listdir(cogs_dir):
                if filename.endswith(".py") and not filename.startswith("__"):
                    cog_name = filename[:-3]
                    extension = f"cogs.{cog_name}"
                    self.initial_extensions.append(extension)
                    
                    try:
                        await self.load_extension(extension)
                        logger.info(f"Successfully loaded cog: {cog_name}")
                    except Exception as e:
                        logger.error(f"Failed to load cog {cog_name}: {type(e).__name__}: {e}")
                        self.failed_cogs[cog_name] = str(e)
                        # Log full traceback for debugging
                        logger.debug(traceback.format_exc())
        else:
            logger.warning(f"Cogs directory not found at {cogs_dir}")
        
        # Add developer cog if not already loaded
        if not any("developer" in ext for ext in self.extensions):
            try:
                self.add_cog(DeveloperCog(self))
                logger.info("Added internal developer cog")
            except Exception as e:
                logger.error(f"Failed to add developer cog: {e}")
        
        # Sync slash commands
        await self.sync_commands()
    
    async def sync_commands(self, guild: Optional[discord.Guild] = None):
        """Sync slash commands globally or to a specific guild"""
        try:
            if guild:
                synced = await self.tree.sync(guild=guild)
                logger.info(f"Synced {len(synced)} command(s) to guild {guild.name}")
            else:
                synced = await self.tree.sync()
                logger.info(f"Synced {len(synced)} command(s) globally")
            return len(synced)
        except Exception as e:
            logger.error(f"Failed to sync commands: {e}")
            raise
    
    async def on_ready(self):
        """Called when the bot is ready"""
        logger.info(f"Bot is ready! Logged in as: {self.user.name} ({self.user.id})")
        logger.info(f"Connected to {len(self.guilds)} guild(s)")
        
        # Report any failed cogs
        if self.failed_cogs:
            logger.warning(f"Failed to load {len(self.failed_cogs)} cog(s):")
            for cog, error in self.failed_cogs.items():
                logger.warning(f"  - {cog}: {error}")
        
        # Start background tasks
        try:
            bot_tasks.start_update_task(self)
            logger.info("Started background tasks")
        except Exception as e:
            logger.error(f"Failed to start background tasks: {e}")
    
    async def on_guild_join(self, guild: discord.Guild):
        """Called when the bot joins a new guild"""
        logger.info(f"Joined new guild: {guild.name} ({guild.id})")
        # Optionally sync commands to the new guild
        try:
            await self.sync_commands(guild)
        except Exception as e:
            logger.error(f"Failed to sync commands to new guild: {e}")
    
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        """Global error handler for traditional commands"""
        if isinstance(error, commands.CommandNotFound):
            return
        
        logger.error(f"Command error in {ctx.command}: {type(error).__name__}: {error}")
        
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing required argument: {error.param.name}")
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"Invalid argument: {error}")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("You don't have permission to use this command.")
        else:
            await ctx.send(f"An error occurred: {error}")

class DeveloperCog(commands.Cog):
    """Developer commands for managing the bot"""
    
    def __init__(self, bot: DiscordBot):
        self.bot = bot
        
    def cog_check(self, ctx: commands.Context) -> bool:
        """Check if the user is the bot owner"""
        owner_id = os.getenv("OWNER_ID")
        if owner_id:
            return ctx.author.id == int(owner_id)
        return False
    
    @commands.command(name='load')
    async def load_cog(self, ctx: commands.Context, *, cog: str):
        """Load a cog"""
        try:
            extension = f"cogs.{cog}" if not cog.startswith("cogs.") else cog
            await self.bot.load_extension(extension)
            await ctx.send(f"✅ Successfully loaded: `{cog}`")
            logger.info(f"Loaded cog: {cog} (requested by {ctx.author})")
        except commands.ExtensionAlreadyLoaded:
            await ctx.send(f"❌ Cog `{cog}` is already loaded.")
        except commands.ExtensionNotFound:
            await ctx.send(f"❌ Cog `{cog}` not found.")
        except commands.ExtensionFailed as e:
            await ctx.send(f"❌ Failed to load `{cog}`: {e}")
            logger.error(f"Failed to load cog {cog}: {e}")
        except Exception as e:
            await ctx.send(f"❌ Unexpected error: {type(e).__name__}: {e}")
            logger.error(f"Unexpected error loading {cog}: {e}")
    
    @commands.command(name='unload')
    async def unload_cog(self, ctx: commands.Context, *, cog: str):
        """Unload a cog"""
        try:
            extension = f"cogs.{cog}" if not cog.startswith("cogs.") else cog
            await self.bot.unload_extension(extension)
            await ctx.send(f"✅ Successfully unloaded: `{cog}`")
            logger.info(f"Unloaded cog: {cog} (requested by {ctx.author})")
        except commands.ExtensionNotLoaded:
            await ctx.send(f"❌ Cog `{cog}` is not loaded.")
        except Exception as e:
            await ctx.send(f"❌ Error unloading `{cog}`: {type(e).__name__}: {e}")
            logger.error(f"Error unloading {cog}: {e}")
    
    @commands.command(name='reload')
    async def reload_cog(self, ctx: commands.Context, *, cog: str):
        """Reload a cog"""
        try:
            extension = f"cogs.{cog}" if not cog.startswith("cogs.") else cog
            await self.bot.reload_extension(extension)
            await ctx.send(f"✅ Successfully reloaded: `{cog}`")
            logger.info(f"Reloaded cog: {cog} (requested by {ctx.author})")
        except commands.ExtensionNotLoaded:
            await ctx.send(f"❌ Cog `{cog}` is not loaded.")
        except commands.ExtensionNotFound:
            await ctx.send(f"❌ Cog `{cog}` not found.")
        except commands.ExtensionFailed as e:
            await ctx.send(f"❌ Failed to reload `{cog}`: {e}")
            logger.error(f"Failed to reload cog {cog}: {e}")
        except Exception as e:
            await ctx.send(f"❌ Unexpected error: {type(e).__name__}: {e}")
            logger.error(f"Unexpected error reloading {cog}: {e}")
    
    @commands.command(name='reloadall')
    async def reload_all_cogs(self, ctx: commands.Context):
        """Reload all cogs"""
        successful = []
        failed = []
        
        for extension in list(self.bot.extensions.keys()):
            try:
                await self.bot.reload_extension(extension)
                successful.append(extension.replace("cogs.", ""))
            except Exception as e:
                failed.append((extension.replace("cogs.", ""), str(e)))
                logger.error(f"Failed to reload {extension}: {e}")
        
        embed = discord.Embed(
            title="Reload All Cogs",
            color=discord.Color.green() if not failed else discord.Color.orange()
        )
        
        if successful:
            embed.add_field(
                name=f"✅ Successfully Reloaded ({len(successful)})",
                value="\n".join(successful) or "None",
                inline=False
            )
        
        if failed:
            embed.add_field(
                name=f"❌ Failed ({len(failed)})",
                value="\n".join([f"{cog}: {error}" for cog, error in failed]) or "None",
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='cogs')
    async def list_cogs(self, ctx: commands.Context):
        """List all cogs and their status"""
        cogs_dir = os.path.join(os.path.dirname(__file__), "cogs")
        available_cogs = []
        
        if os.path.exists(cogs_dir):
            for filename in os.listdir(cogs_dir):
                if filename.endswith(".py") and not filename.startswith("__"):
                    available_cogs.append(filename[:-3])
        
        loaded_cogs = [ext.replace("cogs.", "") for ext in self.bot.extensions.keys() if ext.startswith("cogs.")]
        unloaded_cogs = [cog for cog in available_cogs if cog not in loaded_cogs]
        
        embed = discord.Embed(
            title="Cog Status",
            color=discord.Color.blue(),
            timestamp=ctx.message.created_at
        )
        
        embed.add_field(
            name=f"✅ Loaded ({len(loaded_cogs)})",
            value="\n".join(loaded_cogs) or "None",
            inline=True
        )
        
        embed.add_field(
            name=f"❌ Unloaded ({len(unloaded_cogs)})",
            value="\n".join(unloaded_cogs) or "None",
            inline=True
        )
        
        if self.bot.failed_cogs:
            embed.add_field(
                name=f"⚠️ Failed to Load ({len(self.bot.failed_cogs)})",
                value="\n".join([f"{cog}: {error[:50]}..." for cog, error in self.bot.failed_cogs.items()]) or "None",
                inline=False
            )
        
        embed.set_footer(text=f"Total: {len(available_cogs)} cogs available")
        await ctx.send(embed=embed)
    
    @commands.command(name='sync')
    async def sync_commands(self, ctx: commands.Context, scope: Optional[str] = None):
        """Sync slash commands
        
        Usage:
        !sync - Sync globally
        !sync guild - Sync to current guild only
        !sync clear - Clear guild commands
        """
        try:
            if scope == "guild":
                synced = await self.bot.tree.sync(guild=ctx.guild)
                await ctx.send(f"✅ Synced {len(synced)} command(s) to this guild")
            elif scope == "clear":
                self.bot.tree.clear_commands(guild=ctx.guild)
                await self.bot.tree.sync(guild=ctx.guild)
                await ctx.send("✅ Cleared all guild commands")
            else:
                synced = await self.bot.tree.sync()
                await ctx.send(f"✅ Synced {len(synced)} command(s) globally")
        except Exception as e:
            await ctx.send(f"❌ Failed to sync commands: {e}")
            logger.error(f"Failed to sync commands: {e}")
    
    @commands.command(name='shutdown')
    async def shutdown_bot(self, ctx: commands.Context):
        """Gracefully shutdown the bot"""
        await ctx.send("Shutting down...")
        logger.info(f"Shutdown requested by {ctx.author}")
        await self.bot.close()

# Create bot instance
bot = DiscordBot()

# Error handler for application commands
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    """Handle errors in slash commands"""
    logger.error(f"Application command error: {type(error).__name__}: {error}")
    
    if isinstance(error, discord.app_commands.CheckFailure):
        message = "You don't have permission to use this command."
    elif isinstance(error, discord.app_commands.CommandOnCooldown):
        message = f"Command is on cooldown. Try again in {error.retry_after:.1f} seconds."
    else:
        message = f"An error occurred: {str(error)[:100]}"
    
    try:
        if interaction.response.is_done():
            await interaction.followup.send(message, ephemeral=True)
        else:
            await interaction.response.send_message(message, ephemeral=True)
    except Exception as e:
        logger.error(f"Failed to send error message: {e}")

if __name__ == "__main__":
    if not bot_token:
        logger.error("BOT_TOKEN not found in environment variables!")
        exit(1)
    
    try:
        bot.run(bot_token, log_handler=None)
    except KeyboardInterrupt:
        logger.info("Bot shutdown via KeyboardInterrupt")
    except Exception as e:
        logger.error(f"Failed to run bot: {e}")
        raise