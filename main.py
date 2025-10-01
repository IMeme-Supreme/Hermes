import discord
from discord.ext import commands
from discord import app_commands
import logging
from dotenv import load_dotenv
import os
import heapq
import json

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
GUILD = discord.Object(id = 914746562268241950)

#commands
@bot.tree.command(name="test", description="tester for bot command", guild = GUILD)
async def foo(interaction: discord.Interaction, arg: str): 
    await interaction.response.send_message(f"Hello {arg}!\nI have been lobotomized.")

@bot.tree.command(name="announcement", description="create a scheduled announcment", guild = GUILD)
async def announcement(interaction: discord.Interaction, role: discord.Role):
    await interaction.response.send_message(f"Hello, here is an example annoucement {role.mention}")

@bot.event
async def on_ready():
    guild = GUILD
    try:
        synced = await bot.tree.sync(guild = guild)
        print(f"synced {len(synced)} commands to the guild!")
    except Exception as e:
        print(f"Error synciing commands: {e}")

    
    

    print(f"This is a test\nHi! my name is {bot.user.name}")


bot.run(token, log_handler=handler, log_level=logging.DEBUG)

