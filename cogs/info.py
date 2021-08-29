import discord
from discord.ext import commands
import datetime

class info(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command(name = 'info')
    async def info(self, context):
        timestamp = datetime.datetime.utcnow()
        
        embed = discord.Embed(
            title = 'Bot Info', 
            color = discord.Color(0xcc3300)
        )
    
        embed.set_image(
            url = 'https://i.imgur.com/POStobb.png'
        )

        embed.add_field(
            name = 'Data de Lançamento:',
            value = '29 de Dezembro de 2020'
        )

        embed.set_footer(text = (f'Request by {context.message.author.name}'))
        embed.timestamp = timestamp
        
        await context.message.channel.send(embed = embed)

def setup(client):
    client.add_cog(info(client))
