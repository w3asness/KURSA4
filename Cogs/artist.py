import discord
import random 
import asyncio
import time
import configuration
import requests # Для get rest api
import json
import os
import platform
import datetime

from datetime import datetime
from discord.ext import commands

# ------------------------ COGS ------------------------ #  

class ArtistCog(commands.Cog, name="ArtistCog"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------- #

    @commands.command(name = 'artist')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def artist (self, ctx, *args):

        artist = " ".join(args)

        requestSearch = requests.get(f'https://api.deezer.com/search/artist?q={artist}&index=0&limit=3&output=json') # Limit : 1
        data = requestSearch.json()

        if data['data'] == []:
            embed = discord.Embed(title = f"**Исполнитель не найден**", description = f"Исполнитель не найден по вашему запросу : ``\"{artist}\"``", color = 0xff0000)
            embed.set_footer(text = "Bot Created likk#7144")
            await ctx.channel.send(embed = embed)
            ctx.command.reset_cooldown(ctx) # Сброс времени задержки
        else:
            numberOfArtistInList = 0
            artistList = ""
            for x in data['data']:
                numberOfArtistInList +=1
                artistList = f"{artistList}**{numberOfArtistInList})** {x['name']}\n"
            
            # Получение списка альбомов
            embed = discord.Embed(title = f"**СПИСОК НАЙДЕННЫХ ИСПОЛНИТЕЛЕЙ**", color = 0xea8700)
            embed.add_field(name = "**ВЫБЕРИТЕ НОМЕР, СООТВЕТСТВУЮЩЕГО ИСПОЛНИТЕЛЯ :**", value = f"{artistList}\n**0) Отменить (без кулдауна)**", inline=False)
            embed.set_footer(text = "Bot Created likk#7144")
            await ctx.channel.send(embed = embed)

            def check(message):
                try:
                    message.content = int(message.content)
                    if ((message.content >= 0) and (message.content <= numberOfArtistInList)):
                        message.content = str(message.content)
                        return message.content
                    else:
                        pass
                except:
                    pass
            try:
                msg = await self.bot.wait_for('message', timeout=15.0, check=check)
                if (int(msg.content) == 0):
                    # Остановка и сброс времени задержки
                    embed = discord.Embed(title = f"", description = "Вы остановили поиск. ", color = 0xff0000)
                    embed.set_footer(text = "Bot Created likk#7144")
                    await ctx.channel.send(embed = embed)
                    ctx.command.reset_cooldown(ctx) # Сброс времени задержки
                else:
                    msg.content = int(msg.content)
                    msg.content = msg.content - 1
                    # Поиск даты
                    artistId = data['data'][msg.content]['id']
                    artistUrl = data['data'][msg.content]['link']
                    artistName = data['data'][msg.content]['name']
                    artistImage = data['data'][msg.content]['picture_xl']

                    # Поиск трех популярных треков на данный момент
                    requestTopTracks = requests.get(f'https://api.deezer.com/artist/{artistId}/top?limit=3') # лимит : 3
                    dataTopTracks = requestTopTracks.json()
                    
                    try:
                        musicName1 = dataTopTracks['data'][0]['title']
                        musicLink1 = dataTopTracks['data'][0]['link']
                    except:
                        musicName1 = ""; musicLink1 = ""
                    try:
                        musicName2 = dataTopTracks['data'][1]['title']
                        musicLink2 = dataTopTracks['data'][1]['link']
                    except:
                        musicName2 = ""; musicLink2 = ""
                    try:
                        musicName3 = dataTopTracks['data'][2]['title']
                        musicLink3 = dataTopTracks['data'][2]['link']
                    except:
                        musicName3 = ""; musicLink3 = ""

                    # Поиск артистов
                    artistRequest = requests.get(f'https://api.deezer.com/artist/{artistId}') 
                    dataArtist = artistRequest.json()
                    # Поиск альбомов 
                    requestArtistAlbums = requests.get(f'https://api.deezer.com/artist/{artistId}/albums') 
                    dataAlbums = requestArtistAlbums.json()

                    # Поиск данных о фанатах и альбоме
                    artistFans = dataArtist['nb_fan']
                    artistAlbums = dataArtist['nb_album']

                    # Поиск названия альбома и ссылки
                    albums = ""
                    othersAlbums = 0
                    for x in dataAlbums['data']:
                        albumName = x['title']  
                        albumLink = x['link'] 
                        if (len(albums) > 900):
                            othersAlbums += 1
                        else: 
                            albums = albums + f"[{albumName}]({albumLink}) - "
                    albums = albums[:-2]
                    if othersAlbums > 0:
                        albums = albums + f"и {othersAlbums} остальные..."

                    # Получение информации в окне  
                    embed = discord.Embed(title = f"**{artistName}**", color = 0x2f9622)
                    embed.set_thumbnail(url = f"{artistImage}")
                    embed.add_field(name = "**Информация об Исполнителе :**", value = f"**Исполнитель :** [{artistName}]({artistUrl})\n**Поклонников :** {artistFans}\n**Номер исполнителя :** {artistAlbums}", inline=False)
                    embed.add_field(name = "**Актуальные песни исполнителя :**", value = f"**1)** [{musicName1}]({musicLink1})\n**2)** [{musicName2}]({musicLink2})\n**3)** [{musicName3}]({musicLink3})", inline=False)
                    embed.add_field(name = "**Альбомы :**", value = f"{albums}", inline=False)
                    embed.set_footer(text = "Bot Created likk#7144")
                    await ctx.channel.send(embed = embed)
            
            except (asyncio.TimeoutError):
                embed = discord.Embed(title = f"**Время ожидания вышло**", description = "Вы превысили время ответа (15с)", color = 0xff0000)
                embed.set_footer(text = "Bot Created likk#7144")
                await ctx.channel.send(embed = embed)
                ctx.command.reset_cooldown(ctx) # Сброс времени задержки

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(ArtistCog(bot))