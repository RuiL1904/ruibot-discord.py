import os
import discord
from discord.ext import commands
from discord.ext.commands.core import command
import dotenv
import json

# Initial setup
dotenv.load_dotenv()

vars = dotenv.dotenv_values('data/.env')

with open(r'data/cmd_handler.json') as file:
    data = json.load(file)

prefix = '.'

client = commands.Bot(command_prefix = commands.when_mentioned_or(prefix), help_command = None, owner_id = vars['MY_ID'])

cogs = []
for filename in os.listdir('./cogs'):        
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        cogs.append(filename[:-3])

@client.event
async def on_ready():
    os.system('cls')
    print('O Bot está online!')
    print(f'Os seguintes comandos foram carregados: \n{cogs}')
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
        await context.reply(embed = embed)
    
    elif extension in data['unloaded']:
        client.load_extension(f'cogs.{extension}')

        embed = discord.Embed(
            title = 'AVISO',
            description = (f'```O comando {extension} foi ativado com sucesso!```'),
            color = discord.Color(0xcc3300)
        )
        await context.reply(embed = embed)
        
        data['unloaded'].remove(extension) 
        data['loaded'].append(extension)              
  
@client.command(name = 'unload')
@commands.has_role('Developer')
async def unload(context, extension):
    
    if extension in data['unloaded']:
        embed = discord.Embed(
            title = 'Error',
            description = (f'```O comando {extension} já está inativo!```'),
            color = discord.Color(0xcc3300)
        )
        await context.reply(embed = embed)
        
    elif extension in data['loaded']:
        client.unload_extension(f'cogs.{extension}')

        embed = discord.Embed(
            title = 'Aviso',
            description = (f'```O comando {extension} foi desativado com sucesso!```'),
            color = discord.Color(0xcc3300)
        )
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
            description = (f'```Este comando está em cooldown \n Por favor tenta novamente após {round(error.retry_after, 1)} segundos!```'),
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
            description = '```Um ou mais argumentos estão em falta... \n Digita .help para mais info!```',
            color = discord.Color(0xcc3300)
        )
    
    else:
        embed = discord.Embed(
            title = 'ERRO',
            description = '```Algo correu mal, mas não consegui detetar o que foi...```',
            color = discord.Color(0xcc3300)       
        )

    await context.reply(embed = embed)
    print(f'Erro encontrado: {error}')

client.run(vars['TOKEN'])