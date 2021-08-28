import discord
from discord.ext import commands
import json
import requests

class covid(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name = 'covid')
    @commands.cooldown(rate = 1, per = 5, type = commands.BucketType.member)
    async def covid(self, context, place):    
        if place in ['Portugal', 'portugal']:
            url_pt = requests.get('https://covid19-api.vost.pt/Requests/get_last_update')
            data = json.loads(url_pt.text)

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
                title = (f'COVID 19 EM PORTUGAL (Dia {dia[:-5]})'),
                description = '\u200b',
                color = discord.Color(0xcc3300)
            )

            embed.add_field(
                name = 'Casos confirmados',
                value = confirmados,
                inline = False
            )
            embed.add_field(
                name = 'Casos novos',
                value = novos,
                inline = False
            )
            
            embed.add_field(
                name = 'Casos ativos',
                value = ativos,
                inline = False
            )

            embed.add_field(
                name = 'Casos recuperados',
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
                value = internados,
                inline = False
            )

            embed.add_field(
                name = 'Internados em UCI',
                value = uci,
                inline = False
            )

            embed.add_field(
                name = 'Contactos em vigilância',
                value = vigilancia,
                inline = False
            )
            
            embed.add_field(
                name = 'Incidência por 100mil habitantes',
                value = incidencia,
                inline = False
            )

            embed.add_field(
                name = 'Indíce de transmissão',
                value = rt,
                inline = False
            )
            await context.reply(embed = embed)

def setup(client):
    client.add_cog(covid(client))