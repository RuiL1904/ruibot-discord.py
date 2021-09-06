import platform
import discord
from discord.ext import commands
from datetime import datetime

class info(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command(name = 'info')
    async def info(self, context):
        timestamp = datetime.utcnow()
        
        # Embed sent by the Bot
        embed = discord.Embed(
            title = 'Bot Info', 
            color = discord.Color(0xcc3300)
        )
    
        embed.set_image(
            url = 'https://i.imgur.com/POStobb.png'
        )

        embed.add_field(
            name = 'Data de Lançamento:',
            value = '29 de Dezembro de 2020',
            inline = False
        )

        embed.add_field(
            name = 'Python Version',
            value = platform.python_version()
        )

        embed.add_field(
            name = 'Discord.py Version',
            value = discord.__version__
        )

        embed.add_field(
            name = 'Latência',
            value = (f'{int(round((self.client.latency * 1000), 0))} ms')
        )

        embed.set_footer(text = (f'Request by {context.message.author.name}'))
        embed.timestamp = timestamp
        
        await context.reply(embed = embed)

def setup(client):
    client.add_cog(info(client))
