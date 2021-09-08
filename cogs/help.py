import discord
from discord.ext import commands
from datetime import datetime

class help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name = 'help')
    async def help(self, context): 
        timestamp = datetime.utcnow()
        
        # Embed sent by the Bot
        embed = discord.Embed(
            title = 'Comandos Disponíveis: [Obrigatório] <Opcional>',
            color = discord.Color(0xcc3300)
        )

        fields = [('.help', 'É preciso apresentações?'),
        ('.info', 'Exibe info acerca do bot'),
        ('.covid [place]', 'Exibe dados sobre a COVID-19 em Portugal ou numa cidade')]
        
        for name, value in fields:
            embed.add_field(
                name = name,
                value = value,
                inline = False
            )
        
        url = 'https://media1.tenor.com/images/5300f3652dd3742b804294c00c24ba04/tenor.gif?itemid=8600234'
        
        embed.set_image(url = url)
        embed.set_footer(text = (f'Request by {context.message.author.name}'))
        embed.timestamp = timestamp
        
        await context.reply(embed = embed)

def setup(client):
    client.add_cog(help(client))
