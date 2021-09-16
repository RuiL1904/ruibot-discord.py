import os
import dotenv
import discord
from discord.ext import commands
import json
from datetime import datetime

# Initial setup
dotenv.load_dotenv()

vars = dotenv.dotenv_values('data/.env')

with open(r'data/cmd_handler.json') as file:
    data = json.load(file)   

prefix = '.'

client = commands.Bot(command_prefix = commands.when_mentioned_or(prefix), help_command = None, owner_id = int(vars['MY_ID']))

timestamp = datetime.utcnow()

# Add each cog to the bot commands
cogs = []
for filename in os.listdir('./cogs'):        
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        cogs.append(filename[:-3])

# Load jishaku
client.load_extension('jishaku')

# Bot ready event
@client.event
async def on_ready():
    if client.is_ready():
        os.system('clear')
        print(f'O Bot foi reconectado! ({client.user})')
        print(f'Os seguintes comandos foram carregados: {cogs}')
    else:
        print(f'O Bot está online! ({client.user})')
        print(f'Os seguintes comandos foram carregados: {cogs}')
    
    await client.change_presence(status = discord.Status.do_not_disturb, activity = discord.Game(name = '.help'))

# Error handler
@client.event
async def on_command_error(context, error, member = discord.Member):

    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title = 'ERRO',
            description = (f'```Esse comando não existe!```'),
            color = discord.Color(0xcc3300)
        )

    elif isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(
            title = 'ERRO',
            description = (f'```Este comando está em cooldown... \nPor favor tenta novamente após {round(error.retry_after, 1)} segundos!```'),
            color = discord.Color(0xcc3300)
        )

    elif isinstance(error, commands.UserInputError):
        embed = discord.Embed(
            title = 'ERRO',
            description = (f'```Algo está mal no teu input... \nRetifica-o e tenta novamente!```'),
            color = discord.Color(0xcc3300)
        )           
    
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title = 'ERRO',
            description = '```Não tens as permissões necessárias!```',
            color = discord.Color(0xcc3300)
        )
    
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title = 'ERRO',
            description = '```Um ou mais argumentos estão em falta... \nDigita .help para mais info!```',
            color = discord.Color(0xcc3300)
        )
    
    elif isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(
            title = 'ERRO',
            description = '```Infelizmente não tenho permissões para fazer isso...```',
            color = discord.Color(0xcc3300)
        )
    
    elif isinstance(error, commands.TooManyArguments):
        embed = discord.Embed(
            title = 'ERRO',
            description = '```Existem aí argumentos a mais... \n Digita .help para mais info!```',
            color = discord.Color(0xcc3300)
        )
    
    else:
        embed = discord.Embed(
            title = 'ERRO',
            description = (f'```Algo correu mal! Contacta um @Developer \nErro encontrado: {error}```'),
            color = discord.Color(0xcc3300)       
        )
    
    embed.set_footer(text = (f'Requested by {context.message.author.name}'))
    embed.timestamp = timestamp

    await context.reply(embed = embed)

# Run the bot
client.run(vars['TOKEN'])