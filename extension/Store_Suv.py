import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle

class StoreSuvCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='suv')
    async def suv_command(self, ctx):
        await ctx.send(
            file=discord.File('./img/suv/black.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='PURCHASE NOW', emoji='💵', custom_id='suv_black'),
                    Button(style=ButtonStyle.gray, label='FIRST PURCHASE CLICK', emoji='🏷', custom_id='new_player'),
                ]
            ]
        )
        await ctx.send(
            file=discord.File('./img/suv/blue.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='PURCHASE NOW', emoji='💵', custom_id='suv_blue'),
                    Button(style=ButtonStyle.gray, label='FIRST PURCHASE CLICK', emoji='🏷', custom_id='new_player'),
                ]
            ]
        )
        await ctx.send(
            file=discord.File('./img/suv/orange.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='PURCHASE NOW', emoji='💵', custom_id='suv_orange'),
                    Button(style=ButtonStyle.gray, label='FIRST PURCHASE CLICK', emoji='🏷', custom_id='new_player'),
                ]
            ]
        )
        await ctx.send(
            file=discord.File('./img/suv/police.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='PURCHASE NOW', emoji='💵', custom_id='suv_police'),
                    Button(style=ButtonStyle.gray, label='FIRST PURCHASE CLICK', emoji='🏷', custom_id='new_player'),
                ]
            ]
        )

        await ctx.message.delete()

def setup(bot):
    bot.add_cog(StoreSuvCommand(bot))
