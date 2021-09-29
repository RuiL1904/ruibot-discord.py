from datetime import datetime
import dotenv
import nextcord as discord
from nextcord.ext import commands
import aiohttp

# Load .env
dotenv.load_dotenv()
vars = dotenv.dotenv_values('data/.env')
client_id = vars['UNSPLASH']

class Image(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command(name = 'image')
    async def image(self, context, *, argument):
        timestamp = datetime.utcnow()
        argument_url = argument.strip()
        
        # API data extraction
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.unsplash.com/photos/random/?query={argument_url}&client_id={client_id}') as response:

                # If server is down (Not code 200)
                if response.status != 200:
                    # Embed sent by the bot
                    embed = discord.Embed(
                        title = 'ERRO',
                        description = '```A API de imagens está desligada ou o teu argumento não se encontra registado...Contacta um @Developer```',
                        color = discord.Color(0xcc3300)
                    )

                    embed.set_footer(text = (f'Requested by {context.message.author.name}'))
                    embed.timestamp = timestamp

                    await context.reply(embed = embed) 
                
                else:
                    data = await response.json()
                    url = data['urls']['regular']

                    #Embed sent by the bot
                    embed = discord.Embed(
                        title = f'Encontrei esta imagem relacionada a {argument}',
                        color = discord.Color(0xcc3300),
                        url = url
                    )

                    embed.set_image(url = url)
                    embed.set_footer(text = (f'Requested by {context.message.author.name}'))
                    embed.timestamp = timestamp

                    await context.reply(embed = embed) 

def setup(client):
    client.add_cog(Image(client))