import os
import traceback
import dotenv
import nextcord as discord
from nextcord.ext import commands

# Load config
from config import config
color = config.color

# Load .env
dotenv.load_dotenv()
vars = dotenv.dotenv_values('data/.env')

# Initialise client (bot)
client = commands.Bot(
    command_prefix = commands.when_mentioned_or('.'), 
    help_command = None, 
    owner_id = int(vars['MY_ID']),
    intents = discord.Intents.all(),
    case_insensitive = True
)

# Add each cog (./cogs) to the bot commands
cogs = []
for filename in os.listdir('./cogs'):        
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        cogs.append(filename[:-3])

# Nextcord does not support jishaku yet (waiting for it to do so)
# client.load_extension('jishaku')

# Bot on_ready event
@client.event
async def on_ready():
    # Clear terminal ('cls' for Windows and 'clear' for Linux)
    os.system('clear')

    # Get bot guilds
    guilds = []
    for guild in client.guilds:
        guilds.append(guild.name)
    
    print(f'O Bot ficou online! ({client.user} - {client.owner_id})')
    print(f'Os seguintes comandos foram carregados: {cogs}')
    print(f'Os seguintes servidores foram carregados: {guilds}')
    
    # Set bot status (Discord Rich Presence)
    await client.change_presence(status = discord.Status.do_not_disturb, activity = discord.Game(name = '.help'))

# Bot on_command_error (error handler)
@client.event
async def on_command_error(context, error: traceback.format_exc()):

    # Command does not exists or is disabled
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title = 'ERRO',
            description = (f'```Esse comando não existe!```'),
            color = color
        )

        config.embed_completion(context, embed)
        await context.reply(embed = embed)
    
    # Command in on cooldown
    elif isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(
            title = 'ERRO',
            description = (f'```Este comando está em cooldown... \nPor favor tenta novamente após {round(error.retry_after, 1)} segundos!```'),
            color = color
        )
        
        config.embed_completion(context, embed)
        await context.reply(embed = embed)

    # There's a error on user input
    elif isinstance(error, commands.UserInputError):
        # Avoid weird error that assumes missing required argument(s) as an user input error exception
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title = 'ERRO',
                description = '```Um ou mais argumentos estão em falta... \nDigita .help para mais info!```',
                color = color
            )

            config.embed_completion(context, embed)
            await context.reply(embed = embed)
        
        else:
            embed = discord.Embed(
            title = 'ERRO',
            description = (f'```Algo está mal no teu input... \nRetifica-o e tenta novamente!```'),
            color = color
            )

            config.embed_completion(context, embed)
            await context.reply(embed = embed)           
    
    # User is missing permissions
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title = 'ERRO',
            description = '```Não tens as permissões necessárias!```',
            color = color
        )

        config.embed_completion(context, embed)
        await context.reply(embed = embed)
    
    # There is a lack of arguments on user input
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title = 'ERRO',
            description = '```Um ou mais argumentos estão em falta... \nDigita .help para mais info!```',
            color = color
        )

        config.embed_completion(context, embed)
        await context.reply(embed = embed)
    
    # Bot is missing permissions
    elif isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(
            title = 'ERRO',
            description = '```Infelizmente não tenho permissões para fazer isso...```',
            color = color
        )

        config.embed_completion(context, embed)
        await context.reply(embed = embed)
    
    # There are too many arguments on user input
    elif isinstance(error, commands.TooManyArguments):
        embed = discord.Embed(
            title = 'ERRO',
            description = '```Existem aí argumentos a mais... \n Digita .help para mais info!```',
            color = color
        )

        config.embed_completion(context, embed)
        await context.reply(embed = embed)
    
    # Any other exception
    else:
        embed = discord.Embed(
            title = 'ERRO',
            description = (f'```Algo correu mal! Contacta um @Developer \nErro encontrado: {error}```'),
            color = color       
        )

        config.embed_completion(context, embed)
        await context.reply(embed = embed)

# Run the bot
client.run(vars['TOKEN'])
