from datetime import datetime
import nextcord as discord

# Vars
timestamp = datetime.utcnow()
color = discord.Color(0xcc3300)

# Set embed footer and timestamp
def embed_completion(context, embed):
    embed.set_footer(text = f'Requested by {context.message.author.name}')
    embed.timestamp = timestamp
