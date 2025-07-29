import discord
from discord.ext import commands
from discord import app_commands
from utils import cobbleverse_utils
import os
from dotenv import load_dotenv

load_dotenv()
cobbleverse_domain = os.getenv("COBBLEVERSE_DOMAIN", "cobbleverse.example.com")


def is_owner():
    """Custom check for owner-only commands"""
    async def predicate(interaction: discord.Interaction):
        owner_id = int(os.getenv("OWNER_ID"))
        return interaction.user.id == owner_id
    return app_commands.check(predicate)

class Cobbleverse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="cobbleverse_status", description="Check Cobbleverse server status")
    async def cobbleverse_status(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer()
            server_ip, cpu_usage, mem_usage, server_status = await cobbleverse_utils.check_cobbleverse_server()
            
            if server_ip.startswith("Error"):
                await interaction.followup.send(
                    f"❌ Failed to get server status: {server_ip}", 
                    ephemeral=True
                )
                return
            
            color = 0x2ecc71 if server_status == "STARTED" else 0xe74c3c
            thumbnail_url = "https://www.minecraft.net/content/dam/games/minecraft/logos/Minecraft-logo.png" if server_status == "STARTED" else "https://www.minecraft.net/content/dam/games/minecraft/screenshots/carousel-alex-sunset.jpg"
            
            embed = discord.Embed(title="⛏️ Cobbleverse Server Status", color=color)
            embed.add_field(name="🔗 Connection", value=cobbleverse_domain, inline=True)
            embed.add_field(name="🖥️ CPU Usage", value=cpu_usage, inline=True)
            embed.add_field(name="💾 Memory Usage", value=mem_usage, inline=True)
            
            embed.set_footer(text=f"Server Status: {server_status}")
            embed.set_thumbnail(url=thumbnail_url)
            embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
            
            await interaction.followup.send(embed=embed)
        except Exception as e:
            await interaction.followup.send(
                f"❌ An unexpected error occurred: {str(e)}", 
                ephemeral=True
            )
    
    @app_commands.command(name="cobbleverse_start", description="Start the Cobbleverse server")
    @is_owner()
    async def cobbleverse_start(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer()
            returncode, stdout, stderr = await cobbleverse_utils.start_cobbleverse_server()
            
            if returncode is None:
                await interaction.followup.send("⏱️ Timeout occurred while starting the Cobbleverse server.")
                return
            
            if returncode == 0:
                await interaction.followup.send(f"✅ Cobbleverse server started successfully.\n```{stdout}```")
            else:
                await interaction.followup.send(f"❌ Failed to start Cobbleverse server.\nError:```{stderr}```")
        except Exception as e:
            await interaction.followup.send(f"❌ An error occurred: {e}")
    
    @app_commands.command(name="cobbleverse_stop", description="Stop the Cobbleverse server")
    @is_owner()
    async def cobbleverse_stop(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer()
            returncode, stdout, stderr = await cobbleverse_utils.stop_cobbleverse_server()
            
            if returncode is None:
                await interaction.followup.send("⏱️ Timeout occurred while stopping the Cobbleverse server.")
                return
            
            if returncode == 0:
                await interaction.followup.send(f"✅ Cobbleverse server stopped successfully.\n```{stdout}```")
            else:
                await interaction.followup.send(f"❌ Failed to stop Cobbleverse server.\nError:```{stderr}```")
        except Exception as e:
            await interaction.followup.send(f"❌ An error occurred: {e}")
    
    @app_commands.command(name="cobbleverse_restart", description="Restart the Cobbleverse server")
    @is_owner()
    async def cobbleverse_restart(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer()
            returncode, stdout, stderr = await cobbleverse_utils.restart_cobbleverse_server()
            
            if returncode is None:
                await interaction.followup.send("⏱️ Timeout occurred while restarting the Cobbleverse server.")
                return
            
            if returncode == 0:
                await interaction.followup.send(f"✅ Cobbleverse server restarted successfully.\n```{stdout}```")
            else:
                await interaction.followup.send(f"❌ Failed to restart Cobbleverse server.\nError:```{stderr}```")
        except Exception as e:
            await interaction.followup.send(f"❌ An error occurred: {e}")
    
    @app_commands.command(name="cobbleverse_info", description="Display information about the Cobbleverse server")
    async def cobbleverse_info(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(
                title="⛏️ Cobbleverse Server Information",
                color=0x3498db
            )
            embed.add_field(
                name="🌐 Server Type",
                value="Minecraft Cobblemon Server",
                inline=True
            )
            embed.add_field(
                name="📍 Server Location",
                value="/home/tempeste/Drive2_symlink/cobbleverse",
                inline=True
            )
            embed.add_field(
                name="🔧 Management",
                value="LinuxGSM (mcserver)",
                inline=True
            )
            embed.add_field(
                name="🌍 Domain",
                value=cobbleverse_domain,
                inline=True
            )
            embed.add_field(
                name="📋 Available Commands",
                value=(
                    "`/cobbleverse_status` - Check server status\n"
                    "`/cobbleverse_start` - Start server (owner only)\n"
                    "`/cobbleverse_stop` - Stop server (owner only)\n"
                    "`/cobbleverse_restart` - Restart server (owner only)"
                ),
                inline=False
            )
            embed.set_thumbnail(url="https://www.minecraft.net/content/dam/games/minecraft/logos/Minecraft-logo.png")
            embed.set_footer(text="Use /cobbleverse_status to check current server status")
            
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(
                f"❌ An error occurred: {str(e)}",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(Cobbleverse(bot))