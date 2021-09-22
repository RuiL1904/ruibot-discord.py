import io
from datetime import datetime
from datetime import date
import nextcord as discord
from nextcord.ext import commands
import json
import pandas
import aiofiles
import aiohttp

class ipma(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command(name = 'ipma')
    async def ipma(self, context, *, argument):

        timestamp = datetime.utcnow()
        
        # Get counties data
        async with aiofiles.open('data/ipma/concelhos-metadata.json', mode = 'r') as file:
            content = await file.read() 
        
        # Order dicofre codes by district
        distritos = {
            'Aveiro': [101, 119],
            'Beja': [201, 214],
            'Braga': [301, 314],
            'Bragança': [401, 412],
            'Castelo Branco': [501, 511],
            'Coimbra': [601, 617],
            'Évora': [701, 714],
            'Faro': [801, 816],
            'Guarda': [901, 914],
            'Leiria': [1001, 1016],
            'Lisboa': [1101, 1116],
            'Portalegre': [1201, 1215],
            'Porto': [1301, 1318],
            'Santarém': [1401, 1421],
            'Setúbal': [1501, 1513],
            'Viana do Castelo': [1601, 1610],
            'Vila Real': [1701, 1714],
            'Viseu': [1801, 1824],
        }
        
        data = json.loads(content)
        data = data['data']
        
        try:
            # Get counties data
            concelhos = []
            for i in range(len(data)):
                concelhos.append(data[i]['designacao'])
        
            for i, concelho in enumerate(concelhos):
                if argument.lower() == concelho.lower():
                    dicofre = int(data[i]['dicofre'])
                    image = data[i]['brasao']
                    break
            
            # Check in which district a county is
            for district, [min, max] in distritos.items():
                if min <= dicofre <= max:
                    distrito = district

            # Format url vars
            district_url = (distrito.lower()).replace(' ', '-')
            
            if dicofre < 1000:
                dicofre_url = str(dicofre)
                dicofre_url = f'0{dicofre_url}'
            else:
                dicofre_url = dicofre
            
            concelho_url = (argument.lower()).replace(' ', '-')
            
            # Get IPMA data
            async with aiohttp.ClientSession() as session:
                # Get maximum temperature
                async with session.get(f'https://api.ipma.pt/open-data/observation/climate/temperature-max/{district_url}/mtxmx-{dicofre_url}-{concelho_url}.csv') as response:

                    data = await response.text()

                    # Format data as I want
                    data = io.StringIO(data)
                    data = pandas.read_csv(data, sep = ',')

                    # If server is up (Code 200)
                    if response.status == 200:
                        
                        # Organise data as I want
                        dia = data.values[-1][0]
                        dia = datetime.strptime(dia, '%Y-%m-%d').strftime('%d-%m-%Y')
                        max = round(data.values[-1][2], 2)
                        min = round(data.values[-1][1], 2)

                        # Format county name on embed
                        splits = argument.split(' ')
                        
                        if len(splits) >= 3:
                            argument = f'{splits[0].capitalize()} {splits[1]} {splits[2].capitalize()}'
                        else:
                            argument = argument.title()

                        # Embed sent by the bot
                        embed = discord.Embed(
                            title = f'Temperatura em {argument} ({distrito})',
                            description = f'Dia {dia}',
                            color = discord.Color(0xcc3300)
                        )
                        
                        fields = [(f'Mínima', f'{min}ºC'),
                        (f'Máxima', f'{max}ºC')]

                        for name, value in fields:
                            embed.add_field(
                                name = name,
                                value = value,
                                inline = True
                            )
                        
                        embed.set_thumbnail(url = image)
                        embed.set_footer(text = (f'Requested by {context.message.author.name}'))
                        embed.timestamp = timestamp
                        
                        await context.reply(embed = embed)
        
        except:
            embed = discord.Embed(
                title = 'ERRO',
                description = '```Esse concelho não existe ou não se encontra registado na API...```',
                color = discord.Color(0xcc3300) 
            )

            embed.set_footer(text = (f'Requested by {context.message.author.name}'))
            embed.timestamp = timestamp
            
            await context.reply(embed = embed)

def setup(client):
    client.add_cog(ipma(client))
