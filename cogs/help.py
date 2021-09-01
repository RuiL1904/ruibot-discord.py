import discord
from discord.ext import commands
import datetime

class help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name = 'help')
    async def help(self, context): 
        timestamp = datetime.datetime.utcnow()
            
        embed = discord.Embed(
            title = 'Comandos Disponíveis: [Obrigatório] <Opcional>',
            color = discord.Color(0xcc3300)
        )
        
        embed.set_image(
            url = 'https://media1.tenor.com/images/5300f3652dd3742b804294c00c24ba04/tenor.gif?itemid=8600234'
        )

        embed.add_field(
            name = '.help',
            value = 'É preciso apresentações?',
            inline = False
        )
        
        embed.add_field(
            name = '.info',
            value = 'Exibe info acerca do Bot',
            inline = False
        )

        embed.add_field(
            name = '.covid [place]',
            value = 'Exibe dados sobre a COVID-19 em Portugal ou numa cidade',
            inline = False
        )

        embed.set_footer(text = (f'Request by {context.message.author.name}'))
        embed.timestamp = timestamp
        
        await context.reply(embed = embed)

def setup(client):
    client.add_cog(help(client))
