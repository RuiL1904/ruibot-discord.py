import io
from datetime import datetime
import nextcord as discord
from nextcord.ext import commands
import aiohttp
import pandas

class Covid(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name = 'covid')
    @commands.cooldown(rate = 1, per = 5, type = commands.BucketType.member) # Add cooldown of 5 seconds between command requests
    async def covid(self, context, *, place):
        timestamp = datetime.utcnow()
        
        # Portugal data extraction
        if place.lower() == 'portugal':
            async with aiohttp.ClientSession() as session:   
                async with session.get('https://covid19-api.vost.pt/Requests/get_last_update') as response:
                    
                    # If server is down (Not Code 200)
                    if response.status != 200:
                        # Embed sent by the bot
                        embed = discord.Embed(
                            title = 'ERRO',
                            description = '```A API de Covid-19 está desligada...Contacta um @Developer```',
                            color = discord.Color(0xcc3300)
                        )

                        embed.set_footer(text = (f'Requested by {context.message.author.name}'))
                        embed.timestamp = timestamp

                        await context.reply(embed = embed)
                    else:    
                        data = await response.json()
                    
                        # Portugal vaccination data extraction
                        async with aiohttp.ClientSession() as session:
                            async with session.get('https://raw.githubusercontent.com/dssg-pt/covid19pt-data/master/vacinas.csv') as response_vax:
                                
                                data_vax = await response_vax.text()

                                # Format data_vax as I want
                                data_vax = io.StringIO(data_vax)
                                data_vax = pandas.read_csv(data_vax, sep = ',')

                                # If server is down (Not Code 200)
                                if response.status != 200:
                                    # Embed sent by the bot
                                    embed = discord.Embed(
                                        title = 'ERRO',
                                        description = '```A API de Covid-19 está desligada...Contacta um @Developer```',
                                        color = discord.Color(0xcc3300)
                                    )

                                    embed.set_footer(text = (f'Requested by {context.message.author.name}'))
                                    embed.timestamp = timestamp

                                    await context.reply(embed = embed)

                                else:      
                                    # Organise data as I want
                                    dia = data['data_dados']
                                    confirmados = data['confirmados']
                                    novos = data['confirmados_novos']
                                    recuperados = data['recuperados']
                                    obitos = data['obitos']
                                    
                                    if data['ativos'] != None:
                                        ativos = str(data['ativos'])[:-2]
                                    else:
                                        ativos = 'None'
                                    
                                    if data['incidencia_nacional'] != None:
                                        incidencia = str(data['incidencia_nacional'])[:-2]
                                    else:
                                        incidencia = 'None'
                                    
                                    rt = data['rt_nacional']

                                    if response_vax.status == 200:
                                        vacinadas_total = str(data_vax['pessoas_vacinadas_completamente'].max())[:-2]
                                        vacinadas_total_hoje = str(data_vax['pessoas_vacinadas_completamente_novas'].max())[:-2]

                                    # Embed sent by the bot
                                    embed = discord.Embed(
                                        title = 'COVID-19 em Portugal',
                                        description = (f'Dia {dia[:-5]}'),
                                        color = discord.Color(0xcc3300)
                                    )
                            
                                    fields = [('Casos Totais', confirmados),
                                    ('Novos Casos', novos),
                                    ('Casos Ativos', ativos),
                                    ('Recuperados', recuperados),
                                    ('Óbitos', obitos),
                                    ('Totalmente Vacinadas', f'{vacinadas_total} (+{vacinadas_total_hoje})'),
                                    ('Incidência por 100mil Habitantes', incidencia),
                                    ('Indice de Transmissibilidade', rt)]

                                    for name, value in fields:
                                        embed.add_field(
                                            name = name,
                                            value = value,
                                            inline = False
                                        )

                                    embed.set_footer(text = (f'Requested by {context.message.author.name}'))
                                    embed.timestamp = timestamp
                                    
                                    await context.reply(embed = embed)                                                        
        
        # County data extraction
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://covid19-api.vost.pt/Requests/get_last_update_specific_county/{place}') as response:
                    
                    # If server is down (Not code 200)
                    if response.status != 200:
                        # Embed sent by the bot
                        embed = discord.Embed(
                            title = 'ERRO',
                            description = '```A API de Covid-19 está desligada...Contacta um @Developer```',
                            color = discord.Color(0xcc3300)
                        )

                        embed.set_footer(text = (f'Requested by {context.message.author.name}'))
                        embed.timestamp = timestamp

                        await context.reply(embed = embed)
                    
                    else:
                        data = await response.json()
                        data = data[0]

                        # Organise data as I want
                        dia = data['data']
                        confirmados = data['confirmados_14']
                        confirmados_ontem = data['confirmados_1']
                        incidencia = data['incidencia']
                        categoria = data['incidencia_categoria']
                        risco = data['incidencia_risco']
                        distrito = data['distrito']
                        population = data['population']

                        # Embed sent by the bot
                        embed = discord.Embed(
                            title = (f'COVID-19 em {place.title()} ({distrito})'),
                            description = (f'Dia {dia}'),
                            color = discord.Color(0xcc3300)
                        )

                        fields = [('Confirmados nos Últimos 14 Dias', confirmados),
                        ('Confirmados no Último Dia', confirmados_ontem),
                        ('Risco de Contágio', f'{risco} {categoria}'),
                        ('População', population)]
                        
                        for name, value in fields:
                            embed.add_field(
                                name = name,
                                value = value,
                                inline = False
                            )

                        embed.set_footer(text = (f'Requested by {context.message.author.name}'))
                        embed.timestamp = timestamp
                        
                        await context.reply(embed = embed)              

def setup(client):
    client.add_cog(Covid(client))