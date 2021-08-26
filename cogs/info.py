import discord
from discord.ext import commands

class info(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command(name = 'info')
    async def info(self, context):
        
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

        embed.set_footer(
            text = 'Bot desenvolvido por RuiL1904'
        )
        await context.message.channel.send(embed = embed)

def setup(client):
    client.add_cog(info(client))
