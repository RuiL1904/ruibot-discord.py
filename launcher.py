import os
import discord
from discord.ext import commands
import dotenv
import json

# Initial setup
dotenv.load_dotenv()

vars = dotenv.dotenv_values('data/.env')

with open(r'data/cmd-handler.json') as file:
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
async def load(context, extension = None):
    try:
        if extension is None:
            embed = discord.Embed(
                title = 'Error',
                description = '```É necessário fornecer o nome do comando! \n\nEste comando usa-se assim: .load <comando>```',
                color = discord.Color(0xcc3300)
            )
            await context.send(embed = embed)
    
        elif extension in data['loaded']:
            embed = discord.Embed(
                title = 'Error',
                description = (f'```O comando {extension} já está ativado!```'),
                color = discord.Color(0xcc3300)
            )
            await context.send(embed = embed)
        
        else:
            client.load_extension(f'cogs.{extension}')

            embed = discord.Embed(
                title = 'Aviso',
                description = (f'```O comando {extension} foi ativado com sucesso!```'),
                color = discord.Color(0xcc3300)
            )
            await context.send(embed = embed)
            
            data['unloaded'].remove(extension) 
            data['loaded'].append(extension)              
    except:
        embed = discord.Embed(
            title = 'Error',
            description = '```Esse comando não existe! \n\nUsa .help list para mais informações!```',
            color = discord.Color(0xcc3300)
        )
        await context.send(embed = embed)
  
@client.command(name = 'unload')
@commands.has_role('Developer')
async def unload(context, extension = None):
    try:
        if extension is None:
            embed = discord.Embed(
                title = 'Error',
                description = '```É necessário fornecer o nome do comando! \n\nEste comando usa-se assim: .load <comando>```',
                color = discord.Color(0xcc3300)
            )
            await context.send(embed = embed)
    
        elif extension in data['unloaded']:
            embed = discord.Embed(
                title = 'Error',
                description = (f'```O comando {extension} já está desativado!```'),
                color = discord.Color(0xcc3300)
            )
            await context.send(embed = embed)
            
        else:
            client.unload_extension(f'cogs.{extension}')

            embed = discord.Embed(
                title = 'Aviso',
                description = (f'```O comando {extension} foi desativado com sucesso!```'),
                color = discord.Color(0xcc3300)
            )
            await context.send(embed = embed)
            
            data['loaded'].remove(extension)
            data['unloaded'].append(extension)
    except:
        embed = discord.Embed(
            title = 'Error',
            description = '```Esse comando não existe! \n\nUsa .help list para mais informações!```',
            color = discord.Color(0xcc3300)
        )
        await context.send(embed = embed)

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
    await context.send(embed = embed)

@client.event
async def on_command_error(context, error):

    embed = discord.Embed(
        title = 'Error',
        description = '```Esse comando não existe. \n\nUsa .help para mais informações!```',
        color = discord.Color(0xcc3300)
    )
    await context.send(embed = embed)
    print(error)

client.run(vars['TOKEN'])