import platform
import nextcord as discord
from nextcord.ext import commands
import aiosqlite

# Load config
from config import config
color = config.color

class Info(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command(name = 'info')
    async def info(self, context):
        
        # Embed sent by the Bot
        embed = discord.Embed(
            title = 'Bot Info', 
            color = color
        )

        fields = [('Data de Lançamento:', '29 de dezembro de 2020'),
        ('Desenvolvedor:', 'Rui Lopes'),
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
        
        embed.set_thumbnail(url = 'https://i.imgur.com/POStobb.png')
        config.embed_completion(context, embed)
        
        await context.reply(embed = embed)

def setup(client):
    client.add_cog(Info(client))
