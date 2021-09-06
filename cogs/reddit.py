import discord
from discord.ext import commands

class reddit(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command(name = 'reddit')
    @commands.cooldown(rate = 1, per = 5, type = commands.BucketType.member)
    async def reddit(self, context, *, argument):
        await context.send('O comando funciona!')
    

def setup(client):
    client.add_cog(reddit(client))