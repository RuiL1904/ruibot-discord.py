from datetime import datetime
import random
import nextcord as discord
from nextcord.ext import commands
import asyncio
import aiofiles
import aiosqlite

class pergunta(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name = 'pergunta', aliases = ['p'])
    async def pergunta(self, context):
        
        timestamp = datetime.utcnow()

        num = random.randint(1, 3911) # Randomize a number in questions range
        
        # Read questions
        async with aiofiles.open('data/Categoria B/perguntas.txt', mode = 'r') as file:
            questions = []
            async for line in file:
                questions.append(line)

        # Read possible answers (1, 2 or 3)
        answers = {}
        for i in range(1, 4): # Each "i" is a possible answer
            async with aiofiles.open(f'data/Categoria B/resposta{i}.txt', mode = 'r') as file:
                answers[f'answer_{i}'] = []
                async for line in file:
                    answers[f'answer_{i}'].append(line)
        
        # Read image of question
        async with aiofiles.open('data/Categoria B/imgs.txt', mode = 'r') as file:
            images = []
            async for line in file:
                images.append(line)

        # Read correct answer
        async with aiofiles.open('data/Categoria B/certa.txt', mode = 'r') as file:
            answer = []
            async for line in file:
                answer.append(line)
        
        correct_answer = answer[num].strip()

        # Embed sent by the bot
        embed = discord.Embed(
            title = 'Pergunta de Categoria B (30 segundos)',
            description = questions[num],
            color = discord.Color(0xcc3300)
        )

        fields = [('1.', f'{answers["answer_1"][num]}'),
        ('2.', f'{answers["answer_2"][num]}')]
        
        for name, value in fields:
            embed.add_field(
                name = name,
                value = value,
                inline = False
            )

        # Check whether answer_3 exists or not
        if answers['answer_3'][num].strip() != '':
            embed.add_field(
                name = '3.',
                value = f'{answers["answer_3"][num]}',
                inline = False
            )
        
        image = discord.File(f'data/Imagens B/{(images[num]).strip()}.jpg', filename = 'image.jpg') # Set the image as a discord.File, since .set_image method only supports HTTP(S)
        embed.set_image(url = 'attachment://image.jpg')

        embed.set_footer(text = (f'Requested by {context.message.author.name}'))
        embed.timestamp = timestamp
        
        sent = await context.reply(file = image, embed = embed)
        
        # Check user response
        try:
            def check(message):
                return message.author == context.message.author and message.channel == context.message.channel
            
            user_response = await self.client.wait_for(
                "message",
                timeout = 30,
                check = check
            )

            # Check wether the response is correct or not
            if user_response:
                # Initialise the database connection
                try:
                    async with aiosqlite.connect('data/database.db') as connection:
                        async with connection.cursor() as cursor:
            
                            # Correct answer
                            if user_response.content == correct_answer:

                                await user_response.reply('Parabéns, acertaste!')
                                
                                discord_id = context.author.id
                                discord_name = context.author.name

                                # Verify if user exists
                                user_id = await cursor.execute('SELECT user_id FROM leaderboard WHERE user_id = ?', [discord_id])
                                user_id = await cursor.fetchone()
                                
                                # Get correct_answers
                                correct_answers = await cursor.execute('SELECT correct_answers FROM leaderboard WHERE user_id = ?', [discord_id])
                                correct_answers = await cursor.fetchone()
                                
                                # Get total_answers
                                total_answers = await cursor.execute('SELECT total_answers FROM leaderboard WHERE user_id = ?', [discord_id])
                                total_answers = await cursor.fetchone()
                                
                                if not user_id:
                                    # Create user by his discord_id
                                    await cursor.execute('INSERT INTO leaderboard VALUES (?, ?, ?, ?)', [discord_id, discord_name, 1, 1])
                                    await connection.commit()
                                    await cursor.close()
                                else:
                                    # Update correct_answers and total_answers (+1)
                                    for row in correct_answers:
                                        row += 1
                                        correct_answers = row
                                    
                                    for row in total_answers:
                                        row += 1
                                        total_answers = row
                                    
                                    await cursor.execute('UPDATE leaderboard SET correct_answers = ? WHERE user_id = ?', [correct_answers, discord_id])
                                    await cursor.execute('UPDATE leaderboard SET total_answers = ? WHERE user_id = ?', [total_answers, discord_id])
                                    await connection.commit()
                                    await cursor.close()
                            
                            # Wrong answer
                            else:
                                await user_response.reply(f'Ups, parece que erraste! A resposta correta era a {correct_answer}...')

                                discord_id = context.author.id
                                discord_name = context.author.name

                                # Verify if user exists
                                user_id = await cursor.execute('SELECT user_id FROM leaderboard WHERE user_id = ?', [discord_id])
                                user_id = await cursor.fetchone()
                                
                                # Get total_answers
                                total_answers = await cursor.execute('SELECT total_answers FROM leaderboard WHERE user_id = ?', [discord_id])
                                total_answers = await cursor.fetchone()
                                
                                if not user_id:
                                    # Create user by his discord_id
                                    await cursor.execute('INSERT INTO leaderboard VALUES (?, ?, ?, ?)', [discord_id, discord_name, 0, 1])
                                    await connection.commit()
                                    await cursor.close()
                                else:
                                    # Update total_answers (+1)
                                    for row in total_answers:
                                        row += 1
                                        total_answers = row

                                    await cursor.execute('UPDATE leaderboard SET total_answers = ? WHERE user_id = ?', [total_answers, discord_id])
                                    await connection.commit()
                                    await cursor.close()
                
                # Weird "no active connection" error
                except ValueError:
                    return

        # Time (30 seconds) has ended 
        except asyncio.TimeoutError:
            await sent.reply(f'Infelizmente o tempo acabou, {context.author.mention}.')

def setup(client):
    client.add_cog(pergunta(client))