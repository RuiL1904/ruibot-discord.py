from datetime import datetime
import nextcord as discord
from nextcord.ext import commands
import aiosqlite

class leaderboard(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name = 'leaderboard', aliases = ['lb'])
    async def leaderboard(self, context):
        timestamp = datetime.utcnow()

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
                    color = discord.Color(0xcc3300)
                )
                
                fields = []
                for i in range(len(data)):
                    # Check if user has at least 10 answered questions
                    if data[i][3] > 10:
                        fields.append((f'{i + 1}. {data[i][1]}', f'{data[i][4]}% respostas corretas ({data[i][2]}/{data[i][3]})'))
                
                for name, value in fields:
                    embed.add_field(
                        name = name,
                        value = value,
                        inline = False
                    )
                
                embed.set_footer(text = (f'Requested by {context.message.author.name}'))
                embed.timestamp = timestamp
                
                await context.reply(embed = embed) 

def setup(client):
    client.add_cog(leaderboard(client))