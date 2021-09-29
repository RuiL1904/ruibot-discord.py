from datetime import datetime
import nextcord as discord
from nextcord.ext import commands
import aiohttp

class Word(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command(name = 'word')
    async def word(self, context, count):
        timestamp = datetime.utcnow()

        # Get data from the API
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://random-word-api.herokuapp.com/word?number={count}') as response:

                data = await response.json()
                
                # Embed sent by the bot 
                embed = discord.Embed(
                    title = f'Aqui tens {count} palavras',
                    description = (', '.join(data)),
                    color = discord.Color(0xcc3300)
                )

                await context.reply(embed = embed)

def setup(client):
    client.add_cog(Word(client))