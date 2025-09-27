import discord
from discord.ext import commands
from discord import app_commands
import logging
from dotenv import load_dotenv
import os
import heapq

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

announcementsList = []
heapq.heapify(announcementsList)

#commands
@bot.tree.command(name="test", description="tester for bot command")
async def foo(interaction: discord.Interaction, arg: str): 
    announcementsList.append(arg)  
    await interaction.response.send_message(f"Hello {arg}!\nI have been lobotomized.")


@bot.event
async def on_ready():
    guild = discord.Object(id = 914746562268241950)
    try:
        synced = await bot.tree.sync(guild = guild)
        print(f"synced to the guild!")
    except Exception as e:
        print(f"Error synciing commands: {e}")

    print(f"This is a test\nHi! my name is {bot.user.name}")
    print(announcementsList)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)

