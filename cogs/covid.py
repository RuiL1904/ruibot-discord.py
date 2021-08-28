import discord
from discord.ext import commands
import json
import requests

class covid(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name = 'covid')
    @commands.cooldown(rate = 1, per = 5, type = commands.BucketType.member)
    async def covid(self, context, *, place):    
        url = requests.get('https://covid19-api.vost.pt/Requests/get_status')
        data = json.loads(url.text)
        
        if data['status'] == 'Server is OK':  
            if place.lower() == 'portugal':
                url = requests.get('https://covid19-api.vost.pt/Requests/get_last_update')
                data = json.loads(url.text)

                dia = data['data_dados']
                confirmados = data['confirmados']
                novos = data['confirmados_novos']
                recuperados = data['recuperados']
                obitos = data['obitos']
                internados = data['internados']
                uci = data['internados_uci']
                vigilancia = data['vigilancia']
                ativos = data['ativos']
                incidencia = data['incidencia_nacional']
                rt = data['rt_nacional']
            
                embed = discord.Embed(
                    title = 'COVID 19 EM Portugal',
                    description = (f'Dia {dia[:-5]}'),
                    color = discord.Color(0xcc3300)
                )

                embed.add_field(
                    name = 'Casos totais',
                    value = (f'{confirmados} (+{novos})'),
                    inline = False
                )
                
                embed.add_field(
                    name = 'Casos ativos',
                    value = (str(ativos))[:-2],
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
                    name = 'Internados',
                    value = (str(internados))[:-2],
                    inline = False
                )

                embed.add_field(
                    name = 'Internados em UCI',
                    value = (str(uci))[:-2],
                    inline = False
                )

                embed.add_field(
                    name = 'Contactos em vigilância',
                    value = (str(vigilancia))[:-2],
                    inline = False
                )
                
                embed.add_field(
                    name = 'Incidência por 100mil habitantes',
                    value = incidencia,
                    inline = False
                )

                embed.add_field(
                    name = 'Indíce de transmissibilidade',
                    value = rt,
                    inline = False
                )
                await context.reply(embed = embed)
            
            else:       
                url = requests.get(f'https://covid19-api.vost.pt/Requests/get_last_update_specific_county/{place}')
                data = json.loads(url.text)
                data_dict = data[0]

                dia = data_dict['data']
                confirmados = data_dict['confirmados_14']
                confirmados_ontem = data_dict['confirmados_1']
                incidencia = data_dict['incidencia']
                categoria = data_dict['incidencia_categoria']
                risco = data_dict['incidencia_risco']
                distrito = data_dict['distrito']
                population = data_dict['population']

                embed = discord.Embed(
                    title = (f'COVID 19 em {place.title()} ({distrito})'),
                    description = (f'Dia {dia}'),
                    color = discord.Color(0xcc3300)
                )
                
                embed.add_field(
                    name = 'Confirmados nos últimos 14 dias',
                    value = confirmados,
                    inline = False
                )

                embed.add_field(
                    name = 'Confirmados no último dia',
                    value = confirmados_ontem,
                    inline = False
                )

                embed.add_field(
                    name = 'Risco de contágio',
                    value = (f'{risco} ({categoria})'),
                    inline = False
                )

                embed.add_field(
                    name = 'População',
                    value = population,
                    inline = False
                )

                await context.send(embed = embed)

def setup(client):
    client.add_cog(covid(client))