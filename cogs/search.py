from datetime import datetime
import nextcord as discord
from nextcord.ext import commands
import wikipedia
import asyncio

# Load config
from config import config
color = config.color

class Search(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command(name = 'search')
    async def search(self, context, results = None, *, argument):
        
        if results is None:
            results = 5
        
        # Search wikipedia for x results regarding the given argument
        results = wikipedia.search(argument, results = results)

        if len(results) == 0:
            await context.reply('Não foram encontrados resultados...')
  
        # Embed sent by the bot
        embed = discord.Embed(
            title = 'Search',
            description = 'Qual destes resultados pretendes pesquisar?',
            color = color
        )

        for i in range(len(results)):
            embed.add_field(
                name = f'{i + 1}. {results[i]}',
                value = '\u200b',
                inline = False
            )

        config.embed_completion(context, embed)

        sent = await context.reply(embed = embed)
        
        # Check user response
        try:
            def check(message):
                return message.author == context.message.author and message.channel == context.message.channel

            user_response = await self.client.wait_for(
                "message",
                timeout = 30,
                check = check
            )
            
            # Response meets requirements
            str_range = []
            for i in range(len(results)):
                str_range.append(str(i + 1))
            
            if user_response.content in str_range:

                definition = wikipedia.summary(
                    results[(int(user_response.content)) - 1],
                    sentences = 3,
                    chars = 1000,
                    auto_suggest = True,
                    redirect = True
                )

                user_response_url = (str(results[(int(user_response.content)) - 1])).replace(' ', '_')
                url = f'https://en.wikipedia.org/wiki/{user_response_url}'
                
                # Embed sent by the bot
                embed = discord.Embed(
                    title = f'Definição para {str(results[(int(user_response.content)) - 1])}',
                    description = definition,
                    color = color,
                    url = url
                )

                config.embed_completion(context, embed)
                
                await user_response.reply(embed = embed)
            
            # Response does not meet requirements
            else:
                # Embed sent by the bot
                embed = discord.Embed(
                    title = 'ERRO',
                    description = (f'```Resposta fora do range... \nRetifica-a e tenta novamente!```'),
                    color = color
                )

                config.embed_completion(context, embed)
                
                await user_response.reply(embed = embed)                

        # Timer (30 seconds) has ended
        except asyncio.TimeoutError:
            await sent.reply(f'Infelizmente o tempo acabou, {context.author.mention}.')

def setup(client):
    client.add_cog(Search(client))