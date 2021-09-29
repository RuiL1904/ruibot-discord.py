import dotenv
import nextcord as discord
from nextcord.ext import commands
import aiohttp

# Load .env
dotenv.load_dotenv()
vars = dotenv.dotenv_values('data/.env')
client_id = vars['UNSPLASH']

# Load config
from config import config
color = config.color

class Image(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command(name = 'image')
    async def image(self, context, *, argument):
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
                        color = color
                    )

                    config.embed_completion(context, embed)

                    await context.reply(embed = embed) 
                
                else:
                    data = await response.json()
                    url = data['urls']['regular']

                    #Embed sent by the bot
                    embed = discord.Embed(
                        title = f'Encontrei esta imagem relacionada a {argument}',
                        color = color,
                        url = url
                    )

                    embed.set_image(url = url)
                    config.embed_completion(context, embed)

                    await context.reply(embed = embed) 

def setup(client):
    client.add_cog(Image(client))
