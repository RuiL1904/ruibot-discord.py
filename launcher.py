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

client = commands.Bot(command_prefix = commands.when_mentioned_or(prefix), help_command = None, owner_id = vars['MY_ID'])

timestamp = datetime.utcnow()

# Add each cog to the bot commands
cogs = []
for filename in os.listdir('./cogs'):        
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        cogs.append(filename[:-3])

# Bot ready event
@client.event
async def on_ready():
    if client.is_ready():
        os.system('cls')
        print(f'O Bot foi reconectado! ({client.user})')
        print(f'Os seguintes comandos foram carregados: {cogs}')
    else:
        print(f'O Bot está online! ({client.user})')
        print(f'Os seguintes comandos foram carregados: {cogs}')
    
    await client.change_presence(status = discord.Status.do_not_disturb, activity = discord.Game(name = '.help'))

# Command handler
@client.command(name = 'load')
@commands.has_role('Developer')
async def load(context, cog):
    
    if cog in data['loaded']:
        embed = discord.Embed(
            title = 'ERRO',
            description = (f'```O comando {cog} já está ativo!```'),
            color = discord.Color(0xcc3300)
        )

        embed.set_footer(text = (f'Requested by {context.message.author.name}'))
        embed.timestamp = timestamp
        
        await context.reply(embed = embed)
    
    elif cog in data['unloaded']:
        client.load_extension(f'cogs.{cog}')

        embed = discord.Embed(
            title = 'AVISO',
            description = (f'```O comando {cog} foi ativado com sucesso!```'),
            color = discord.Color(0xcc3300)
        )

        embed.set_footer(text = (f'Requested by {context.message.author.name}'))
        embed.timestamp = timestamp
        
        await context.reply(embed = embed)
        
        data['unloaded'].remove(cog) 
        data['loaded'].append(cog)              
  
@client.command(name = 'unload')
@commands.has_role('Developer')
async def unload(context, cog):
    
    if cog in data['unloaded']:
        embed = discord.Embed(
            title = 'ERRO',
            description = (f'```O comando {cog} já está inativo!```'),
            color = discord.Color(0xcc3300)
        )

        embed.set_footer(text = (f'Requested by {context.message.author.name}'))
        embed.timestamp = timestamp
        
        await context.reply(embed = embed)
        
    elif cog in data['loaded']:
        client.unload_extension(f'cogs.{cog}')

        embed = discord.Embed(
            title = 'AVISO',
            description = (f'```O comando {cog} foi desativado com sucesso!```'),
            color = discord.Color(0xcc3300)
        )

        embed.set_footer(text = (f'Requested by {context.message.author.name}'))
        embed.timestamp = timestamp
        
        await context.reply(embed = embed)
        
        data['loaded'].remove(cog)
        data['unloaded'].append(cog)

# List each command
@client.command(name = 'list')
@commands.has_role('Developer')
async def list(context):
    
    loaded = data['loaded']
    unloaded = data['unloaded']

    embed = discord.Embed(
        title = 'Lista de comandos',
        description = '\u200b',
        color = discord.Color(0xcc3300)
    )

    embed.add_field(
        name = 'Comandos ativos',
        value = loaded,
    )

    embed.add_field(
        name = 'Comandos inativos',
        value = unloaded,
        inline = False
    )

    embed.set_footer(text = (f'Requested by {context.message.author.name}'))
    embed.timestamp = timestamp

    await context.reply(embed = embed)

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
        if not isinstance(error, commands.MissingRequiredArgument):
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