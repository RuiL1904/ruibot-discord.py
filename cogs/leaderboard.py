import nextcord as discord
from nextcord.ext import commands
import aiosqlite

# Load config
from config import config
color = config.color

class Leaderboard(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name = 'leaderboard', aliases = ['lb'])
    async def leaderboard(self, context):

        # Open connection
        async with aiosqlite.connect('data/database.db') as connection:
            async with connection.cursor() as cursor:
                
                # Get the data from the database as I want
                await cursor.execute('SELECT * FROM leaderboard ORDER BY percentage DESC')
                data = await cursor.fetchall()
                await cursor.close()

                # Embed sent by the bot
                embed = discord.Embed(
                    title = 'Leaderboard (.pergunta)',
                    description = 'Quem estiver em primeiro é o :rei:',
                    color = color
                )
                
                fields = []
                for i in range(len(data)):
                    # Check if user has at least 10 answered questions (in order to display it on leaderboard)
                    if data[i][3] > 10:
                        fields.append((f'{i + 1}. {data[i][1]}', f'{data[i][4]}% respostas corretas ({data[i][2]}/{data[i][3]})'))
                
                for name, value in fields:
                    embed.add_field(
                        name = name,
                        value = value,
                        inline = False
                    )
                
                config.embed_completion(context, embed)    
               
                await context.reply(embed = embed) 

def setup(client):
    client.add_cog(Leaderboard(client))
