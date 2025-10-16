from ssl import CHANNEL_BINDING_TYPES
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

async def on_submit(self, interaction: discord.Interaction):
    scheduled_datetime = datetime.strptime(f"{self.date}-{self.time}", "%m-%d-%Y-%H-%M")
    await interaction.response.send_message(f"Scheduled announcement for {scheduled_datetime} UTC:\n{self.message}", silent=True)

async def message_sent(channelID, myAnnouncement):
    print(f"Message sent at: {datetime.now().strftime('%H:%M:%S')}")
    channel = bot.get_channel(channelID)
    await channel.send(f"{myAnnouncement.message} {myAnnouncement.role.mention}")

#commands
@bot.tree.command(name="test", description="tester for bot command", guild = GUILD)
async def foo(interaction: discord.Interaction, arg: str): 
    await interaction.response.send_message(f"Hello {arg}!\nI have been lobotomized.")

#allow the user to schedule an annoucnemt in the given channel
@bot.tree.command(name="announcement", description="create a scheduled announcment", guild = GUILD)
async def announcements(interaction: discord.Interaction, role: discord.Role, message: str, set_date:str = None, set_time:str = None):
    #this how you always ensure a quick reponse

    channel = interaction.channel_id
    try:
        set_date = set_date.strip() if set_date else None
        set_time = set_time.strip() if set_time else None
        if(set_date is None and set_time is None):
            await interaction.response.defer(ephemeral=False)
            print(f"You just created an unscheduled announcement!")
            await interaction.followup.send(f"{message} {role.mention}")
        elif set_date is None and set_time is not None:
            today = datetime.today()
            print(f"#1")
            time_parse = datetime.strptime(set_time, "%H:%M").time()
            print(f"#2")
            combined_datetime = datetime.combine(today, time_parse)
            print(f"You just created a datetime")
            newAnnouncement = announcement.announcement(message, role, combined_datetime)
            print(f"You just created a scheduled announcement with no date!")
            run_date = datetime.now() + timedelta(seconds=10)
            scheduler.add_job(message_sent, 'date', run_date = run_date)


        elif set_date and set_time:
            time_parse = datetime.strptime(set_time, "%H:%M").time()
            date_parse = datetime.strptime(set_date, "%m-%d-%Y").date()
            combined_datetime = datetime.combine(date_parse, time_parse)
            newAnnouncement = announcement.announcement(message, role, combined_datetime)
            print(f"You just created a scheduled announcement with a date and time!")
            run_date = combined_datetime
            scheduler.add_job(func = message_sent, run_date = run_date, args=(channel, newAnnouncement))

            
        else:
            await interaction.followup.send(f"YOU SHALL NOT PROVIDE A DATE WITHOUT A TIME!!!!!!!!")
        

    except Exception as e:
            print(f"ERROR IN ANNOUNCEMENT: {e}")
            await interaction.followup.send(f"Something entered wrong :C")
    

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

