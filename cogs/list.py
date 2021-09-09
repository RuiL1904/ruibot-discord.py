import discord
from discord.ext import commands
import json
from datetime import datetime

timestamp = datetime.utcnow()

# Import cogs data
with open(r'data/cmd_handler.json') as file:
    data = json.load(file)   

class list(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    
    @commands.command(name = 'list')
    @commands.has_role('Developer')
    async def list(self, context):

        loaded = data['loaded']
        unloaded = data['unloaded']

        embed = discord.Embed(
            title = 'Lista de comandos',
            description = '\u200b',
            color = discord.Color(0xcc3300)
        )

        fields = [('Comandos ativos', loaded),
        ('Comandos inativos', unloaded)]

        for name, value in fields:
            embed.add_field(
                name = name,
                value = value,
                inline = False
            )

        embed.set_footer(text = (f'Requested by {context.message.author.name}'))
        embed.timestamp = timestamp

        await context.reply(embed = embed)

def setup(client):
    client.add_cog(list(client))