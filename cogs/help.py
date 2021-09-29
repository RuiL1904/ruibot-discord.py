from datetime import datetime
import nextcord as discord
from nextcord.ext import commands

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name = 'help')
    async def help(self, context): 
        timestamp = datetime.utcnow()
        
        # Embed sent by the Bot
        embed = discord.Embed(
            title = 'Comandos: [Obrigatório] <Opcional> (alias)',
            color = discord.Color(0xcc3300)
        )

        fields = [('.help', 'É preciso apresentações?'),
        ('.info', 'Exibe info acerca do bot'),
        ('.covid [place]', 'Exibe dados sobre a COVID-19 em Portugal ou numa cidade'),
        ('.reddit [subreddit]', 'Ainda em construção...'),
        ('.ipma [concelho]', 'Temperaturas máxima e mínima no concelho dado'),
        ('.pergunta (.p)', 'Faz-te uma pergunta sobre o código da estrada'),
        ('.leaderboard (.lb)', 'Exibe a leaderboard do comando .pergunta'),
        ('.image [request]', 'Envia uma imagem baseada no argumento dado'),
        ('.youtube [url] (.yt)', 'Envia a música solicitada em formato mp3'),
        ('.word [count]', 'Envia quantas palavras random forem solicitadas')]
        
        for name, value in fields:
            embed.add_field(
                name = name,
                value = value,
                inline = False
            )
        
        url = 'https://media1.tenor.com/images/5300f3652dd3742b804294c00c24ba04/tenor.gif?itemid=8600234'
        
        embed.set_thumbnail(url = url)
        embed.set_footer(text = (f'Requested by {context.message.author.name}'))
        embed.timestamp = timestamp
        
        await context.reply(embed = embed)

def setup(client):
    client.add_cog(Help(client))
