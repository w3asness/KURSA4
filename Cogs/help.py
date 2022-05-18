import discord

from discord.ext import commands

# ------------------------ COGS ------------------------ #  

class HelpCog(commands.Cog, name="help"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #  
    #получение списка команд
    @commands.command(name = 'help')
    async def help (self, ctx):
        embed = discord.Embed(title=f"__**Меню помощи TopChartBOT (by LIKK) *__", color=0xdeaa0c)
        embed.set_thumbnail(url=f'{self.bot.user.avatar_url}')
        embed.add_field(name="__Команды :__", value=f"**{self.bot.command_prefix}track <Назваие музыки> :** Найти информацию о треке и ее заставка. \n**{self.bot.command_prefix}artist <Имя Артиста> :** Найдите информацию об артисте.\n**{self.bot.command_prefix}album <Название альбома> :** Найдите информацию об альбоме.\n**{self.bot.command_prefix}top :** Поиск топ плейлистов по всему миру.", inline=False)
        embed.set_footer(text="Bot Created by likk#7144")
        await ctx.channel.send(embed=embed)
            

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.remove_command("help")
    bot.add_cog(HelpCog(bot))