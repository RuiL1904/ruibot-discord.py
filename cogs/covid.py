from os import times
import discord
from discord.ext import commands
import json
import requests
import pandas
import datetime

class covid(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name = 'covid')
    @commands.cooldown(rate = 1, per = 5, type = commands.BucketType.member)
    async def covid(self, context, *, place):
        timestamp = datetime.datetime.utcnow()   
        url = requests.get('https://covid19-api.vost.pt/Requests/get_status')
        data = json.loads(url.text)
        
        # Portugal Data
        if data['status'] == 'Server is OK':  
            if place.lower() == 'portugal':
                url = requests.get('https://covid19-api.vost.pt/Requests/get_last_update')
                data = json.loads(url.text)

                data_vax = pandas.read_csv('https://raw.githubusercontent.com/dssg-pt/covid19pt-data/master/vacinas.csv')

                dia = data['data_dados']
                confirmados = data['confirmados']
                novos = data['confirmados_novos']
                recuperados = data['recuperados']
                obitos = data['obitos']
                internados = str(data['internados'])[:-2]
                uci = str(data['internados_uci'])[:-2]
                vigilancia = str(data['vigilancia'])[:-2]
                ativos = str(data['ativos'])[:-2]
                incidencia = data['incidencia_nacional']
                rt = data['rt_nacional']
                vacinadas_total = str(data_vax['pessoas_vacinadas_completamente'].max())[:-2]
                vacinadas_1 = str(data_vax['pessoas_vacinadas_parcialmente'].max())[:-2]
                vacinadas_total_hoje = str(data_vax['pessoas_vacinadas_completamente_novas'].max())[:-2]
                vacinadas_1_hoje = str(data_vax['pessoas_vacinadas_parcialmente_novas'].max())[:-2]
            
                embed = discord.Embed(
                    title = 'COVID-19 em Portugal',
                    description = (f'Dia {dia[:-5]}'),
                    color = discord.Color(0xcc3300)
                )

                embed.add_field(
                    name = 'Casos Totais',
                    value = (f'{confirmados} (+{novos})'),
                    inline = False
                )
                
                embed.add_field(
                    name = 'Casos Ativos',
                    value = ativos,
                    inline = False
                )

                embed.add_field(
                    name = 'Recuperados',
                    value = recuperados,
                    inline = False
                )

                embed.add_field(
                    name = 'Óbitos',
                    value = obitos,
                    inline = False
                )
                
                embed.add_field(
                    name = 'Parcialmente Vacinadas',
                    value = (f'{vacinadas_1} (+{vacinadas_1_hoje})'),
                    inline = False
                )

                embed.add_field(
                    name = 'Totalmente Vacinadas',
                    value = (f'{vacinadas_total} (+{vacinadas_total_hoje})'),
                    inline = False
                )

                embed.add_field(
                    name = 'Internados',
                    value = internados,
                    inline = False
                )

                embed.add_field(
                    name = 'Internados em UCI',
                    value = uci,
                    inline = False
                )

                embed.add_field(
                    name = 'Contactos em Vigilância',
                    value = vigilancia,
                    inline = False
                )
                
                embed.add_field(
                    name = 'Incidência por 100mil Habitantes',
                    value = incidencia,
                    inline = False
                )

                embed.add_field(
                    name = 'Indice de Transmissibilidade',
                    value = rt,
                    inline = False
                )

                embed.set_footer(text = (f'Requested by {context.message.author.name}'))
                embed.timestamp = timestamp
                
                await context.reply(embed = embed)
            
            # County Data
            else:       
                url = requests.get(f'https://covid19-api.vost.pt/Requests/get_last_update_specific_county/{place}')
                data = (json.loads(url.text))[0]

                dia = data['data']
                confirmados = data['confirmados_14']
                confirmados_ontem = data['confirmados_1']
                incidencia = data['incidencia']
                categoria = data['incidencia_categoria']
                risco = data['incidencia_risco']
                distrito = data['distrito']
                population = data['population']

                embed = discord.Embed(
                    title = (f'COVID-19 em {place.title()} ({distrito})'),
                    description = (f'Dia {dia}'),
                    color = discord.Color(0xcc3300)
                )
                
                embed.add_field(
                    name = 'Confirmados nos Últimos 14 Dias',
                    value = confirmados,
                    inline = False
                )

                embed.add_field(
                    name = 'Confirmados no Último Dia',
                    value = confirmados_ontem,
                    inline = False
                )

                embed.add_field(
                    name = 'Risco de Contágio',
                    value = (f'{risco} ({categoria})'),
                    inline = False
                )

                embed.add_field(
                    name = 'População',
                    value = population,
                    inline = False
                )

                embed.set_footer(text = (f'Requested by {context.message.author.name})'))
                embed.timestamp = timestamp

                await context.send(embed = embed)

def setup(client):
    client.add_cog(covid(client))