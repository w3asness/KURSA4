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

class EventsCog(commands.Cog, name="EventsCog"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------- #
     #задержка(colldown)#
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            jour = round(error.retry_after/86400)
            heure = round(error.retry_after/3600)
            minute = round(error.retry_after/60)
            if jour > 0:
                await ctx.send('У этой команды есть время восстановления, обязательно дождитесь '+str(jour)+ "day(s)")
            elif heure > 0:
                await ctx.send('У этой команды есть время восстановления, обязательно дождитесь '+str(heure)+ " hour(s)")
            elif minute > 0:
                await ctx.send('У этой команды есть время восстановления, обязательно дождитесь '+ str(minute)+" minute(s)")
            else:
                await ctx.send(f'У этой команды есть время восстановления, обязательно дождитесь {error.retry_after:.2f} second(s)')
        if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
            await ctx.send("У вас нет необходимого разрешения для размещения этой команды.")
        else:
            print(error)

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(EventsCog(bot))