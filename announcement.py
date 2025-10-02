import discord
from datetime import UTC, datetime, timedelta

class announcement(object):

    def __init__(self, message: str, role: discord.role, myDate: datetime):
        self.message = message
        self.role = role
        self.myDate = myDate
        print(f"You just created an announcement object!")

    
#getters
@property
def getMessage(self):
    return self.message

def getRole(self):
    return self.role

def getDate(self):
    return self.myDate
        