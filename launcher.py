from datetime import datetime, time
import os
import discord
from discord.ext import commands
import dotenv
import json
import datetime

# Initial setup
dotenv.load_dotenv()

vars = dotenv.dotenv_values('data/.env')

with open(r'data/cmd_handler.json') as file:
    data = json.load(file)

prefix = '.'

client = commands.Bot(command_prefix = commands.when_mentioned_or(prefix), help_command = None, owner_id = vars['MY_ID'])

timestamp = datetime.datetime.utcnow()

cogs = []
for filename in os.listdir('./cogs'):        
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        cogs.append(filename[:-3])

@client.event
async def on_ready():
    os.system('cls')
    print(f'O Bot está online! ({client.user})')
    print(f'Os seguintes comandos foram carregados: {cogs}')
    await client.change_presence(status = discord.Status.do_not_disturb, activity = discord.Game(name = '.help'))

# Command Handler
@client.command(name = 'load')
@commands.has_role('Developer')
async def load(context, extension):
    
    if extension in data['loaded']:
        embed = discord.Embed(
            title = 'ERRO',
            description = (f'```O comando {extension} já está ativo!```'),
            color = discord.Color(0xcc3300)
        )

        embed.set_footer(text = (f'Requested by {context.message.author.name}'))
        embed.timestamp = timestamp
        
        await context.reply(embed = embed)
    
    elif extension in data['unloaded']:
        client.load_extension(f'cogs.{extension}')

        embed = discord.Embed(
            title = 'AVISO',
            description = (f'```O comando {extension} foi ativado com sucesso!```'),
            color = discord.Color(0xcc3300)
        )

        embed.set_footer(text = (f'Requested by {context.message.author.name}'))
        embed.timestamp = timestamp
        
        await context.reply(embed = embed)
        
        data['unloaded'].remove(extension) 
        data['loaded'].append(extension)              
  
@client.command(name = 'unload')
@commands.has_role('Developer')
async def unload(context, extension):
    
    if extension in data['unloaded']:
        embed = discord.Embed(
            title = 'ERRO',
            description = (f'```O comando {extension} já está inativo!```'),
            color = discord.Color(0xcc3300)
        )

        embed.set_footer(text = (f'Requested by {context.message.author.name}'))
        embed.timestamp = timestamp
        
        await context.reply(embed = embed)
        
    elif extension in data['loaded']:
        client.unload_extension(f'cogs.{extension}')

        embed = discord.Embed(
            title = 'AVISO',
            description = (f'```O comando {extension} foi desativado com sucesso!```'),
            color = discord.Color(0xcc3300)
        )

        embed.set_footer(text = (f'Requested by {context.message.author.name}'))
        embed.timestamp = timestamp
        
        await context.reply(embed = embed)
        
        data['loaded'].remove(extension)
        data['unloaded'].append(extension)

@client.command(name = 'list')
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

# Error Handler
@client.event
async def on_command_error(context, error):

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
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title = 'ERRO',
                description = '```Um ou mais argumentos estão em falta... \nDigita .help para mais info!```',
                color = discord.Color(0xcc3300)
            )   
        
        else:
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
    
    else:
        embed = discord.Embed(
            title = 'ERRO',
            description = (f'```Algo correu mal! \nErro encontrado: {error}```'),
            color = discord.Color(0xcc3300)       
        )
    
    embed.set_footer(text = (f'Requested by {context.message.author.name}'))
    embed.timestamp = timestamp

    await context.reply(embed = embed)

client.run(vars['TOKEN'])