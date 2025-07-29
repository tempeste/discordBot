import discord
from discord import app_commands
from discord.ext import commands


class UtilityCog(commands.Cog):
    """General utility commands for the Discord bot"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="ping", description="Check if the bot is responsive")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message('Pong!')
    
    @app_commands.command(name="latency", description="Check the bot's latency")
    async def latency(self, interaction: discord.Interaction):
        latency_ms = round(self.bot.latency * 1000)
        await interaction.response.send_message(f'🏓 Pong! Latency: {latency_ms}ms')
    
    @app_commands.command(name="botinfo", description="Get information about the bot")
    async def botinfo(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Bot Information",
            description="A versatile Discord bot with music playback and game server management capabilities.",
            color=discord.Color.blue()
        )
        
        embed.add_field(name="Bot Name", value=self.bot.user.name, inline=True)
        embed.add_field(name="Bot ID", value=self.bot.user.id, inline=True)
        embed.add_field(name="Server Count", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="Python Version", value="3.x", inline=True)
        embed.add_field(name="Discord.py Version", value=discord.__version__, inline=True)
        
        embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else None)
        embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="serverinfo", description="Get information about the current server")
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild
        
        embed = discord.Embed(
            title=f"Server Information - {guild.name}",
            color=discord.Color.green()
        )
        
        embed.add_field(name="Server ID", value=guild.id, inline=True)
        embed.add_field(name="Owner", value=guild.owner.mention if guild.owner else "Unknown", inline=True)
        embed.add_field(name="Member Count", value=guild.member_count, inline=True)
        embed.add_field(name="Text Channels", value=len(guild.text_channels), inline=True)
        embed.add_field(name="Voice Channels", value=len(guild.voice_channels), inline=True)
        embed.add_field(name="Role Count", value=len(guild.roles), inline=True)
        embed.add_field(name="Created At", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="userinfo", description="Get information about a user")
    @app_commands.describe(user="The user to get information about (defaults to yourself)")
    async def userinfo(self, interaction: discord.Interaction, user: discord.Member = None):
        user = user or interaction.user
        
        embed = discord.Embed(
            title=f"User Information - {user.name}",
            color=user.color if hasattr(user, 'color') else discord.Color.default()
        )
        
        embed.add_field(name="User ID", value=user.id, inline=True)
        embed.add_field(name="Username", value=f"{user.name}#{user.discriminator}", inline=True)
        embed.add_field(name="Nickname", value=user.nick if hasattr(user, 'nick') and user.nick else "None", inline=True)
        embed.add_field(name="Account Created", value=user.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
        
        if hasattr(user, 'joined_at') and user.joined_at:
            embed.add_field(name="Joined Server", value=user.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
        
        if hasattr(user, 'roles'):
            roles = [role.mention for role in user.roles if role != interaction.guild.default_role]
            if roles:
                embed.add_field(name="Roles", value=", ".join(roles[:10]), inline=False)
        
        if user.avatar:
            embed.set_thumbnail(url=user.avatar.url)
        
        embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="help", description="Get help with bot commands")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Bot Commands Help",
            description="Here are all available commands organized by category:",
            color=discord.Color.blue()
        )
        
        music_commands = """
        `/join` - Join your voice channel
        `/leave` - Leave the voice channel
        `/play <query>` - Play music from YouTube
        `/search <query>` - Search YouTube for videos
        `/pause` - Pause the current song
        `/resume` - Resume playback
        `/skip` - Skip the current song
        `/stop` - Stop playback and disconnect
        `/view_playlist` - View the server playlist
        `/shuffle_playlist` - Shuffle the playlist
        `/clear_playlist` - Clear the playlist
        `/remove_from_playlist <index>` - Remove a song
        `/loop` - Toggle playlist looping
        """
        
        cobbleverse_commands = """
        `/cobbleverse_status` - Check Cobbleverse server status
        `/cobbleverse_info` - Show server information
        `/cobbleverse_start` - Start the server (Owner only)
        `/cobbleverse_stop` - Stop the server (Owner only)
        `/cobbleverse_restart` - Restart the server (Owner only)
        """
        
        utility_commands = """
        `/ping` - Check bot responsiveness
        `/latency` - Check bot latency
        `/botinfo` - Get bot information
        `/serverinfo` - Get server information
        `/userinfo [user]` - Get user information
        `/help` - Show this help message
        """
        
        embed.add_field(name="🎵 Music Commands", value=music_commands, inline=False)
        embed.add_field(name="⛏️ Cobbleverse Server Commands", value=cobbleverse_commands, inline=False)
        embed.add_field(name="🔧 Utility Commands", value=utility_commands, inline=False)
        
        embed.set_footer(text="Use /command to execute any command")
        
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(UtilityCog(bot))