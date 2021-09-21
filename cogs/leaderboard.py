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
                await cursor.execute('SELECT * FROM leaderboard')
                data = await cursor.fetchall()
                await cursor.close()

                # Sort by % of correct_answers
                sort = [] 
                for i in range(len(data)):
                    percentage = round((data[i][2] * 100) / data[i][3], 1) # Calculate % of correct_answers based on total_answers
                    sort.append((data[i][1], data[i][2], data[i][3], percentage))
                
                # Embed sent by the bot
                embed = discord.Embed(
                    title = 'Leaderboard (.pergunta)',
                    description = 'Quem estiver em primeiro é o :rei:',
                    color = discord.Color(0xcc3300)
                )
                
                fields = []
                for i in range(len(sort)):
                    fields.append((f'{i + 1}. {sort[i][0]}', f'{sort[i][3]}% respostas corretas ({sort[i][1]}/{sort[i][2]})'))

                for name, value in fields:
                    embed.add_field(
                        name = name,
                        value = value,
                        inline = False
                    )
                
                embed.set_footer(text = (f'Request by {context.message.author.name}'))
                embed.timestamp = timestamp
                
                await context.send(embed = embed)              

def setup(client):
    client.add_cog(leaderboard(client))