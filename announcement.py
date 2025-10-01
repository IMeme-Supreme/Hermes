import discord

class announcement(object):
    #constructor
    def __init__(self, message: str, role: discord.role):
        self.message = message
        self.role = role
    
#getters
@property
def getMessage(self):
    return self.message

def getRole(self):
    return self.role
        