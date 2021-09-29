import os
import nextcord as discord
from nextcord.ext import commands
import pytube

class Youtube(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command(name = 'youtube', aliases = ['yt'])
    async def youtube(self, context, url):
        
        # Check if 20 files limit has been exceeded
        count = 0
        for file in os.listdir('data/music'):
            count += 1
        
        if count > 20:
            for file in os.listdir('data/music'):
                os.remove(file)

        # Pytube things
        downloader = pytube.YouTube(url)
        music = downloader.streams.filter(only_audio = True).first()
        out_file = music.download(output_path = 'data/music')

        # Create file on my computer
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)

        # Send the file to Discord
        music_file = discord.File(new_file, filename = 'music.mp3')
        
        await context.reply(file = music_file)

def setup(client):
    client.add_cog(Youtube(client))