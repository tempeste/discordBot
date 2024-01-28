import discord
from discord.ext import tasks
import utils

@tasks.loop(minutes=10)
async def update_bot_status(client):
    _, cpu_usage, mem_usage, server_status = await utils.check_palworld_server()
    status_message = f"CPU: {cpu_usage}, Memory: {mem_usage}, Status: {server_status}"
    await client.change_presence(activity=discord.Game(name=status_message))

def start_update_task(client):
    update_bot_status.start(client)