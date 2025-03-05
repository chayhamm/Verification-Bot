import discord
from discord import app_commands
from discord.ext import commands 
from datetime import datetime
import json

with open("config.json") as config:
    config = json.load(config)

intents = discord.Intents.default()
client = commands.Bot(command_prefix=config["prefix"], intents=intents)

@client.event
async def on_ready():
    print("bot is ready")
    await client.change_presence(status=discord.Status.online)
    try:
        synced = await client.tree.sync(guild=discord.Object(id=config["guildID"]))
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
    embed = discord.Embed(title = "Reboot Rust verification", description = "Click the 'Accept' Button to verify now.", color = 0xFF0000)
    embed.add_field(name = "Why verify?", value = "We, at Reboot, have decided to add this feature to stop bot accounts & scammers from joining the Server.", inline = False)
    guild = client.get_guild(config["guildID"])
    channel = guild.get_channel(config["channelID"])