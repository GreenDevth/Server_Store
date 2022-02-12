import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle


class StoreCruiserCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='cruiser')
    async def cruiser_command(self, ctx):
        await ctx.send(
            file=discord.File('./img/cruiser/black.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='PURCHASE NOW', emoji='💵', custom_id='cruiser_black'),
                    Button(style=ButtonStyle.gray, label='FIRST PURCHASE CLICK', emoji='🏷', custom_id='new_player'),
                ]
            ]
        )
        await ctx.send(
            file=discord.File('./img/cruiser/blue.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='PURCHASE NOW', emoji='💵', custom_id='cruiser_blue'),
                    Button(style=ButtonStyle.gray, label='FIRST PURCHASE CLICK', emoji='🏷', custom_id='new_player'),
                ]
            ]
        )
        await ctx.send(
            file=discord.File('./img/cruiser/green.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='PURCHASE NOW', emoji='💵', custom_id='cruiser_green'),
                    Button(style=ButtonStyle.gray, label='FIRST PURCHASE CLICK', emoji='🏷', custom_id='new_player'),
                ]
            ]
        )
        await ctx.send(
            file=discord.File('./img/cruiser/red.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='PURCHASE NOW', emoji='💵', custom_id='cruiser_red'),
                    Button(style=ButtonStyle.gray, label='FIRST PURCHASE CLICK', emoji='🏷', custom_id='new_player'),
                ]
            ]
        )
        await ctx.send(
            file=discord.File('./img/cruiser/violet.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='PURCHASE NOW', emoji='💵', custom_id='cruiser_violet'),
                    Button(style=ButtonStyle.gray, label='FIRST PURCHASE CLICK', emoji='🏷', custom_id='new_player'),
                ]
            ]
        )
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(StoreCruiserCommand(bot))
