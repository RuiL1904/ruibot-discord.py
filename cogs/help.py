import discord
from discord.ext import commands

class help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name = 'help')
    async def help(self, context): 
            
        embed = discord.Embed(
            title = 'Comandos Disponíveis:',
            color = discord.Color(0xcc3300)
        )
        
        embed.set_image(
            url = 'https://media1.tenor.com/images/5300f3652dd3742b804294c00c24ba04/tenor.gif?itemid=8600234'
        )

        embed.add_field(
            name = '.help',
            value = 'Lista todos os comandos existentes',
            inline = False
        )
        
        embed.add_field(
            name = '.info',
            value = 'Exibe info acerca do Bot',
            inline = False
        )
        await context.message.channel.send(embed = embed)

def setup(client):
    client.add_cog(help(client))
