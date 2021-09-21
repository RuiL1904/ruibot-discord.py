import nextcord as discord
from nextcord.ext import commands
import apraw

# Not working on it right now
class reddit(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command(name = 'reddit')
    @commands.cooldown(rate = 1, per = 5, type = commands.BucketType.member)
    async def reddit(self, context, *, argument):
        pass

def setup(client):
    client.add_cog(reddit(client))