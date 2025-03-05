import discord
from discord import app_commands
from discord.ext import commands 
from datetime import datetime
import json
import time

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
    class VerifyButton(discord.ui.View):
        pass
        def __init__(
                self
            ) -> None:
            super().__init__()
            self.value = None
        @discord.ui.button(label = "Verify", style = discord.ButtonStyle.green)
        async def verifyButton(self, interaction: discord.Interaction, button: discord.ui.button):
            verifiedRole = guild.get_role(int(config["verifiedRole"]))
            user = interaction.user
            if verifiedRole in user.roles:
                await interaction.response.send_message("You are already verified!", ephemeral=True)
            else:
                await user.add_roles(verifiedRole)
                await interaction.response.send_message("You have successfully been verified.", ephemeral=True)
    embed = discord.Embed(title = "Reboot Rust verification", description = "Click the 'Accept' Button to verify now.", color = 0xFF0000)
    embed.add_field(name = "Why verify?", value = "We, at Reboot, have decided to add this feature to stop bot accounts & scammers from joining the Server.", inline = False)
    guild = client.get_guild(int(config["guildID"]))
    channel = guild.get_channel(int(config["channelID"]))
    message = await channel.send(embed = embed, view = VerifyButton())
    time.sleep(10)
    await message.delete()
    message = await channel.send(embed = embed, view = VerifyButton())

client.run(config["token"])