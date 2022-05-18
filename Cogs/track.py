import discord
import configuration
import requests # для get rest api
import json
import os
import datetime
import asyncio

from datetime import datetime
from discord.ext import commands

# ------------------------ COGS ------------------------ #  

class TrackCog(commands.Cog, name="TrackCog"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------- #

    @commands.command(name = 'track')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def track (self, ctx, *args):

        music = " ".join(args)

        requestSearch = requests.get(f'https://api.deezer.com/search/track?q={music}&index=0&limit=10&output=json') # Лимит : 10
        data = requestSearch.json()

        if data['data'] == []:
            embed = discord.Embed(title = f"**Музыка не найдена**", description = f"По вашему запросу музыка не найдена : ``\"{music}\"``", color = 0xff0000)
            embed.set_footer(text = "Bot Created by ?likk#7144")
            await ctx.channel.send(embed = embed)
            ctx.command.reset_cooldown(ctx) # Сброс задержки
        else:
            numberOfMusicInList = 0
            musicList = ""
            for x in data['data']:
                numberOfMusicInList +=1
                musicList = f"{musicList}**{numberOfMusicInList})** {x['title']} - {x['artist']['name']}\n"
            
            # Вывод списка музыки
            embed = discord.Embed(title = f"**СПИСОК НАЙДЕННОЙ МУЗЫКИ**", color = 0xea8700)
            embed.add_field(name = "**ВЫБЕРИТЕ НОМЕР, СООТВЕТСТВУЮЩИЙ МУЗЫКИ :**", value = f"{musicList}\n**0) Для выхода ( без кулдауна )**", inline=False)
            embed.set_footer(text = "Bot Created by likk#7144")
            await ctx.channel.send(embed = embed)

            def check(message):
                try:
                    message.content = int(message.content)
                    if ((message.content >= 0) and (message.content <= numberOfMusicInList)):
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
                    ctx.command.reset_cooldown(ctx) # сброс задержки
                else:
                    # Загрузка отправки сообщения 
                    embed = discord.Embed(title = f"", description = "Подождите, идет загрузка музыки ...", color = 0xea8700)
                    embed.set_footer(text = "Bot Created by likk#7144")
                    embedDownloading = await ctx.channel.send(embed = embed)

                    msg.content = int(msg.content)
                    msg.content = msg.content - 1
                    # Поиск даты
                    musicId = data['data'][msg.content]['id']
                    musicUrl = data['data'][msg.content]['link']
                    longMusicName = data['data'][msg.content]['title']
                    musicName = data['data'][msg.content]['title_short']
                    musicAuthor = data['data'][msg.content]['artist']['name']
                    musicDuration = data['data'][msg.content]['duration']
                    musicCover = data['data'][msg.content]['album']['cover_big']
                    musicAlbum = data['data'][msg.content]['album']['title']
                    musicPreview = data['data'][msg.content]['preview']
                    
                    # Поиск даты альбома 
                    requestTrack = requests.get(f'https://api.deezer.com/track/{musicId}') 
                    dataTrack = requestTrack.json()
                    
                    albumDate = dataTrack['album']['release_date']

                    # Поиск продолжительности трека
                    musicDurationMin = 0
                    while musicDuration > 60:
                        musicDuration -= 60
                        musicDurationMin += 1
                    if musicDuration < 10:
                        musicDuration = f"0{musicDuration}"

                    # Загрузка превью (пробная прослушка)
                    url = musicPreview
                    r = requests.get(url, allow_redirects=True)
                    open(f'C:\\download {musicName}.mp3', 'wb').write(r.content)

                    # Вывод сообщения 
                    embed = discord.Embed(title = f"**{longMusicName} - {musicAuthor}**", color = 0x2f9622)
                    embed.set_thumbnail(url = f"{musicCover}")
                    embed.add_field(name = "**Информация о треке :**", value = f"**Артист :** {musicAuthor}\n**Альбом :** {musicAlbum} ({albumDate[:4]})\n**Продолжительность :** {musicDurationMin}:{musicDuration} мин", inline=False)
                    embed.set_footer(text = "Bot Created by likk#7144")
                    file = discord.File(f'C:\\download {musicName}.mp3')
                    await ctx.channel.send(file=file, embed=embed) # Отправка вставки
                    await embedDownloading.delete() # Удаление сообщения о загрузке

                    os.remove(f"C:\\download {musicName}.mp3") # удаление превью

                    
            except (asyncio.TimeoutError):
                embed = discord.Embed(title = f"**ВРЕМЯ ВЫШЛО**", description = "Вы превысили время ответа (15с)", color = 0xff0000)
                embed.set_footer(text = "Bot Created by likk#7144")
                await ctx.channel.send(embed = embed)
                ctx.command.reset_cooldown(ctx) # Сброс задержки

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(TrackCog(bot))