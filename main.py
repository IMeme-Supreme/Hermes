import discord
from discord.ext import commands
from discord import app_commands, ui, TextStyle
import logging
from dotenv import load_dotenv
import os
from datetime import UTC, datetime, timedelta
import asyncio
import announcement
from apscheduler.schedulers.asyncio import AsyncIOScheduler

updateTimes = []
storedMessages =[]

#initialize scheduler
scheduler = AsyncIOScheduler()



load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
GUILD = discord.Object(id = 914746562268241950)

class scheduleModal(ui.Modal, title="Schedule Annoucnement"):
    message = ui.TextInput(label="Message", style = TextStyle.long)
    date = ui.TextInput(label ="Date (MM-YYYY-DD)")
    time = ui.TextInput(label="Time (HH:MM )")

async def on_submit(self, interaction: discord.Interaction):
    scheduled_datetime = datetime.strptime(f"{self.date}-{self.time}", "%m-%Y-%d-%H-%M")
    await interaction.response.send_message(f"Scheduled announcement for {scheduled_datetime} UTC:\n{self.message}")

def message_sent():
    print(f"Message sent at: {datetime.now().strftime('%H:%M:%S')}")

#commands
@bot.tree.command(name="test", description="tester for bot command", guild = GUILD)
async def foo(interaction: discord.Interaction, arg: str): 
    await interaction.response.send_message(f"Hello {arg}!\nI have been lobotomized.")

#allow the user to schedule an annoucnemt in the given channel
@bot.tree.command(name="announcement", description="create a scheduled announcment", guild = GUILD)
async def announcements(interaction: discord.Interaction, role: discord.Role, message: str, date:str = None, time:str = None):
    newAnnouncement = announcement.announcement(message, role)
    #if (date == None and time == None):
    #      await interaction.response.send_message(f"{message} {role.mention}")
    #scheduled announcements
    #elif(date != None and time != None):
    #dateToken = date.split(':')
    #timeToken = time.split(':')
    #updateTimes.append(datetime(year=dateToken(0), month=dateToken(1), day=dateToken(2), hour=timeToken(0), minute=timeToken(1)))
    run_date = datetime.now() + timedelta(seconds=10)
    scheduler.add_job(message_sent, 'date', run_date = run_date)
    #storedMessages.append(f"{message} {role.mention}")
    await interaction.response.send_message(f"{message} {role.mention}")

#TODO: send announcement at scheduled time

@bot.event
async def on_ready():
    guild = GUILD
    try:
        synced = await bot.tree.sync(guild = guild)
        print(f"synced {len(synced)} commands to the guild!")
    except Exception as e:
        print(f"Error synciing commands: {e}")
    
    if not scheduler.running:
        scheduler.start()
        print(f"Scheduler started!")


    
    

    print(f"This is a test\nHi! my name is {bot.user.name}")


bot.run(token, log_handler=handler, log_level=logging.DEBUG)

