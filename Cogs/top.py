import discord
import random 
import asyncio
import time
import configuration
import requests # For get rest api
import json
import os
import platform
import datetime

from datetime import datetime
from discord.ext import commands

# ------------------------ COGS ------------------------ #  

class TopCog(commands.Cog, name="TopCog"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------- #

    @commands.command(name = 'top')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def top (self, ctx):

        # Получение топ листа
        topList = "**1)** Топ России \n**2)** Топ США\n**3)** Топ Франции\n**4)** Топ Великобритания\n**5)** Топ Бразилия\n**6)** Топ Германия\n**7)** Топ Бельгия\n**8)** Топ Испания\n**9)** Топ Италия\n**10)** Топ Канада\n"

        embed = discord.Embed(title = f"**СПИСОК ТОП СТРАН**", color = 0xea8700)
        embed.add_field(name = "**ВЫБЕРИТЕ НОМЕР, СООТВЕТСТВУЮЩИЙ ПОЗИЦИИ :**", value = f"{topList}\n**0) Чтобы выйти (без кулдауна)**", inline=False)
        embed.set_footer(text = "Bot Created by likk#7144")
        await ctx.channel.send(embed = embed)

        def check(message):
            try:
                message.content = int(message.content)
                if ((message.content >= 0) and (message.content <= 10)):
                    message.content = str(message.content)
                    return message.content
                else:
                    pass
            except:
                pass
        try:
            msg = await self.bot.wait_for('message', timeout=15.0, check=check)
            if (int(msg.content) == 0):
                # Остановка и сброс задержки
                embed = discord.Embed(title = f"", description = "Вы прекратили поиск. ", color = 0xff0000)
                embed.set_footer(text = "Bot Created by likk#7144")
                await ctx.channel.send(embed = embed)
                ctx.command.reset_cooldown(ctx) # Сброс времени задержки
            else:
                msg.content = int(msg.content)
                # Поиск топа по странам 
                if msg.content == 1:
                    top = 1116189381 # 1) Топ России
                elif msg.content == 2:
                    top = 1313621735 # 2) Топ США
                elif msg.content == 3:
                    top = 1109890291 # 3) Топ Франции
                elif msg.content == 4:
                    top = 1111142221 # 4) Топ Великобритания
                elif msg.content == 5:
                    top = 1111141961 # 5) Топ Бразилия
                elif msg.content == 6:
                    top = 1111143121 # 6) Топ Германия
                elif msg.content == 7:
                    top = 1266968331 # 7) Топ Бельгия
                elif msg.content == 8:
                    top = 1116190041 # 8) Топ Испания
                elif msg.content == 9:
                    top = 1116187241 # 9) Топ Италия
                elif msg.content == 10:
                    top = 1652248171 # 10) Топ Канада
                    
                    


                # Поиск топа через deezer
                requestTopTracks = requests.get(f'https://api.deezer.com//playlist/{top}')
                dataTop = requestTopTracks.json()

                topTitle = dataTop['title']
                topFans = dataTop['fans']
                topImage = dataTop['picture_big']
                
                musicTop = ""
                numberOfMusicInList = 0
                for x in dataTop['tracks']['data']:
                    if numberOfMusicInList < 20:
                        numberOfMusicInList +=1
                        musicTop = f"{musicTop}**{numberOfMusicInList})** {x['title']} - {x['artist']['name']}\n"
                    else:
                        break
                
                # Настройка вывода 
                embed = discord.Embed(title = f"**{topTitle}**", color = 0x2f9622)
                embed.set_thumbnail(url = f"{topImage}")
                embed.add_field(name = "**Лучшая информация :**", value = f"**Описание :** Этот топ обновляется каждый день\n**Фанаты :** {topFans}", inline=False)
                embed.add_field(name = "**Музыкальный топ :**", value = f"{musicTop}", inline=False)
                embed.set_footer(text = "Bot Created by likk#7144")
                topMessage = await ctx.channel.send(embed = embed)

                # Добавление реакций для переключения листа
                await topMessage.add_reaction("⬅️")
                await topMessage.add_reaction("➡️") 

                async def editTopMessage(page):
                    if page < 0:
                        page = 4
                    elif page > 4:
                        page = 0

                    requestTopTracks = requests.get(f'https://api.deezer.com//playlist/{top}?index={page*20}&limit=20')
                    dataTop = requestTopTracks.json()

                    musicTop = ""
                    numberOfMusicInList = page*20
                    for x in dataTop['tracks']['data']:
                        numberOfMusicInList +=1
                        musicTop = f"{musicTop}**{numberOfMusicInList})** {x['title']} - {x['artist']['name']}\n"

                    new_embed = discord.Embed(title = f"**{topTitle}**", color = 0x2f9622)
                    new_embed.set_thumbnail(url = f"{topImage}")
                    new_embed.add_field(name = "**Лучшая информация :**", value = f"**Description :** Этот топ обновляется каждый день\n**Фанаты :** {topFans}", inline=False)
                    new_embed.add_field(name = "**Топ музыки :**", value = f"{musicTop}", inline=False)
                    new_embed.set_footer(text = "Bot Created by likk#7144")
                    await topMessage.edit(embed = new_embed)

                    # вызов функции waitReaction
                    await waitReaction(ctx, page, topMessage)

                async def waitReaction(ctx, page, topMessage):
                    
                    def check2(reaction, user):
                        if user == ctx.author:
                            if str(reaction.emoji) == '➡️':
                                return reaction.emoji, user
                            elif str(reaction.emoji) == '⬅️':
                                return reaction.emoji, user

                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=45.0, check=check2)
                        if str(reaction.emoji) == '➡️':
                            pass
                            await topMessage.remove_reaction('➡️', user)
                            page += 1
                            await editTopMessage(page)
                        elif str(reaction.emoji) == '⬅️':
                            await topMessage.remove_reaction('⬅️', user)
                            page -= 1
                            await editTopMessage(page)
                    except asyncio.TimeoutError:
                        await topMessage.clear_reactions()

                # вызов waitReaction
                page = 0
                await waitReaction(ctx, page, topMessage)
        
        except (asyncio.TimeoutError):
            embed = discord.Embed(title = f"**Время ожидания вышло**", description = "Ваше время выбора вышло (15с)", color = 0xff0000)
            embed.set_footer(text = "Bot Created by likk#7144")
            await ctx.channel.send(embed = embed)
            ctx.command.reset_cooldown(ctx) # сброс времени задержки

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(TopCog(bot))