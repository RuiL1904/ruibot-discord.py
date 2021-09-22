import platform
from datetime import datetime
import nextcord as discord
from nextcord.ext import commands
import aiosqlite

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

        fields = [('Data de Lançamento:', '29 de dezembro de 2020'),
        ('Desenvolvedor:', 'Rui Lopes')
        ('Python Version', platform.python_version()),
        ('Nextcord Version', discord.__version__),
        ('SQLite Version', aiosqlite.sqlite_version),
        ('Ping', f'{int(round((self.client.latency * 1000), 0))} ms')]
        
        for name, value in fields:
            embed.add_field(
                name = name,
                value = value,
                inline = False
            )
        
        url = 'https://i.imgur.com/POStobb.png'
        
        embed.set_image(url = url)
        embed.set_footer(text = (f'Request by {context.message.author.name}'))
        embed.timestamp = timestamp
        
        await context.reply(embed = embed)

def setup(client):
    client.add_cog(info(client))
