import discord
import random 
import asyncio
import time
import requests # Для get rest api
import json
import os

from datetime import datetime
from discord.ext import commands

# ------------------------ COGS ------------------------ #  

class AlbumCog(commands.Cog, name="AlbumCog"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------- #

    @commands.command(name = 'album')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def album (self, ctx, *args):

        album = " ".join(args)

        requestSearch = requests.get(f'https://api.deezer.com/search/album?q={album}&index=0&limit=10&output=json') # лимит : 10
        data = requestSearch.json()

        if data['data'] == []:
            embed = discord.Embed(title = f"**Альбом не найден**", description = f"Не удалось найти альбом по вашему запросу : ``\"{album}\"``", color = 0xff0000)
            embed.set_footer(text = "Bot Created by likk#7144")
            await ctx.channel.send(embed = embed)
            ctx.command.reset_cooldown(ctx) # Сброс времени задержки
        else:
            numberOfAlbumInList = 0
            albumList = ""
            for x in data['data']:
                numberOfAlbumInList +=1
                albumList = f"{albumList}**{numberOfAlbumInList})** {x['title']} - {x['artist']['name']}\n"
            
            # Отправка списка альбомов
            embed = discord.Embed(title = f"**СПИСОК НАЙДЕНЫХ АЛЬБОМОВ**", color = 0xea8700)
            embed.add_field(name = "**ВЫБЕРИТЕ НОМЕР, СООТВЕТСТВУЮЩИЙ АЛЬБОМУ :**", value = f"{albumList}\n**0) ВЫХОД (без кулдауна)**", inline=False)
            embed.set_footer(text = "Bot Created by likk#7144")
            await ctx.channel.send(embed = embed)

            def check(message):
                try:
                    message.content = int(message.content)
                    if ((message.content >= 0) and (message.content <= numberOfAlbumInList)):
                        message.content = str(message.content)
                        return message.content
                except:
                    pass
            try:
                msg = await self.bot.wait_for('message', timeout=15.0, check=check)
                if (int(msg.content) == 0):
                    # Остановка и сброс времени задержки
                    embed = discord.Embed(title = f"", description = "Вы остановили поиск. ", color = 0xff0000)
                    embed.set_footer(text = "Bot Created by likk#7144")
                    await ctx.channel.send(embed = embed)
                    ctx.command.reset_cooldown(ctx) # Сброс времени задержки
                else:
                    msg.content = int(msg.content)
                    msg.content = msg.content - 1
                    
                    # Поиск данных альбома 
                    albumId = data['data'][msg.content]['id']
                    requestAlbum = requests.get(f'https://api.deezer.com/album/{albumId}') 
                    dataAlbum = requestAlbum.json()

                    albumTitle = dataAlbum['title']
                    albumCover = dataAlbum['cover_big']                    
                    albumAuthor = dataAlbum['artist']['name']
                    albumLabel = dataAlbum['label']
                    albumTracksNumber = dataAlbum['nb_tracks']
                    albumReleaseDate = dataAlbum['release_date']
                    albumFans = dataAlbum['fans']
                    # Поиск жанров
                    albumGenres = ""
                    for x in dataAlbum['genres']['data']:
                        albumGenres = f"{albumGenres}{x['name']} - "
                    albumGenres = albumGenres[:-2]

                    # Поиск списка треков
                    albumTracks = ""
                    trackNumber =  0
                    for x in dataAlbum['tracks']['data']:
                        trackNumber +=1
                        albumTracks = f"{albumTracks}{trackNumber}. **{x['title']}**\n"

                    # Получение информации об альбоме
                    embed = discord.Embed(title = f"**{albumTitle} - {albumAuthor}**", color = 0x2f9622)
                    embed.set_thumbnail(url = f"{albumCover}")
                    embed.add_field(name = "**ИНФОРМАЦИЯ ОБ АЛЬБОМЕ :**", value = f"**Жанр :** {albumGenres}\n**Дата реализации :** {albumReleaseDate}\n**Номерация треков :** {albumTracksNumber}\n**Фанатов :** {albumFans}\n**Лейбл :** {albumLabel}", inline=False)
                    embed.add_field(name = "**MUSIC LIST :**", value = f"{albumTracks}", inline=False)
                    embed.set_footer(text = "Bot Created by likk#7144")
                    await ctx.channel.send(embed = embed)
                    
            except (asyncio.TimeoutError):
                embed = discord.Embed(title = f"**Время запроса вышло**", description = "Вы превысили время ответа (15с)", color = 0xff0000)
                embed.set_footer(text = "Bot Created by likk#7144")
                await ctx.channel.send(embed = embed)
                ctx.command.reset_cooldown(ctx) # Сброс времени задержки

        
# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(AlbumCog(bot))