import os
import dotenv
from datetime import datetime
import nextcord as discord
from nextcord.ext import commands

# Initialise some vars
timestamp = datetime.utcnow()

# Load .env
dotenv.load_dotenv()
vars = dotenv.dotenv_values('data/.env')

# Initialise client (bot)
client = commands.Bot(command_prefix = commands.when_mentioned_or('.'), help_command = None, owner_id = int(vars['MY_ID']))

# Add each cog (./cogs) to the bot commands
cogs = []
for filename in os.listdir('./cogs'):        
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        cogs.append(filename)

# Nextcord does not support jishaku yet (waiting for ti do so)
# client.load_extension('jishaku')

# Bot on_ready event
@client.event
async def on_ready():
    os.system('clear')
    
    # Checks whether the bot is already ready or not
    if client.is_ready():
        print(f'O Bot foi reconectado! ({client.user} - {client.owner_id})')
        print(f'Os seguintes comandos foram carregados: {cogs}')
    else:
        print(f'O Bot está online! ({client.user} - {client.owner_id})')
        print(f'Os seguintes comandos foram carregados: {cogs}')
    
    # Set bot status (Discord Rich Presence)
    await client.change_presence(status = discord.Status.do_not_disturb, activity = discord.Game(name = '.help'))

# Bot on_command_error (error handler)
@client.event
async def on_command_error(context, error):

    # Set embed footer and timestamp for each exception
    def embed_complete(embed):
        embed.set_footer(text = (f'Requested by {context.message.author.name}'))
        embed.timestamp = timestamp

    # Command does not exists or is disabled
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title = 'ERRO',
            description = (f'```Esse comando não existe!```'),
            color = discord.Color(0xcc3300)
        )

        embed_complete(embed)
        await context.reply(embed = embed)
    
    # Command in on cooldown
    elif isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(
            title = 'ERRO',
            description = (f'```Este comando está em cooldown... \nPor favor tenta novamente após {round(error.retry_after, 1)} segundos!```'),
            color = discord.Color(0xcc3300)
        )
        
        embed_complete(embed)
        await context.reply(embed = embed)

    # There's a error on user input
    elif isinstance(error, commands.UserInputError):
        embed = discord.Embed(
            title = 'ERRO',
            description = (f'```Algo está mal no teu input... \nRetifica-o e tenta novamente!```'),
            color = discord.Color(0xcc3300)
        )

        embed_complete(embed)
        await context.reply(embed = embed)           
    
    # User is missing permissions
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title = 'ERRO',
            description = '```Não tens as permissões necessárias!```',
            color = discord.Color(0xcc3300)
        )

        embed_complete(embed)
        await context.reply(embed = embed)
    
    # There is a lack of arguments on user input
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title = 'ERRO',
            description = '```Um ou mais argumentos estão em falta... \nDigita .help para mais info!```',
            color = discord.Color(0xcc3300)
        )

        embed_complete(embed)
        await context.reply(embed = embed)
    
    # Bot is missing permissions
    elif isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(
            title = 'ERRO',
            description = '```Infelizmente não tenho permissões para fazer isso...```',
            color = discord.Color(0xcc3300)
        )

        embed_complete(embed)
        await context.reply(embed = embed)
    
    # There are too many arguments on user input
    elif isinstance(error, commands.TooManyArguments):
        embed = discord.Embed(
            title = 'ERRO',
            description = '```Existem aí argumentos a mais... \n Digita .help para mais info!```',
            color = discord.Color(0xcc3300)
        )

        embed_complete(embed)
        await context.reply(embed = embed)
    
    # Any other exception
    else:
        embed = discord.Embed(
            title = 'ERRO',
            description = (f'```Algo correu mal! Contacta um @Developer \nErro encontrado: {error}```'),
            color = discord.Color(0xcc3300)       
        )

        embed_complete(embed)
        await context.reply(embed = embed)

# Run the bot
client.run(vars['TOKEN'])