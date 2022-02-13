import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle

class StoreBikeCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='bike')
    async def bike_command(self, ctx):
        await ctx.send(
            file=discord.File('./img/bike/black.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='PURCHASE NOW', emoji='💵', custom_id='bike_black'),
                    Button(style=ButtonStyle.gray, label='SPECIAL PRICE FOR NEWBIE', emoji='🏷', disabled=True)
                ]
            ]
        )
        await ctx.send(
            file=discord.File('./img/bike/blue.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='PURCHASE NOW', emoji='💵', custom_id='bike_blue'),
                    Button(style=ButtonStyle.gray, label='SPECIAL PRICE FOR NEWBIE', emoji='🏷', disabled=True)
                ]
            ]
        )
        await ctx.send(
            file=discord.File('./img/bike/green.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='PURCHASE NOW', emoji='💵', custom_id='bike_green'),
                    Button(style=ButtonStyle.gray, label='SPECIAL PRICE FOR NEWBIE', emoji='🏷', disabled=True)
                ]
            ]
        )
        await ctx.send(
            file=discord.File('./img/bike/hell.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='PURCHASE NOW', emoji='💵', custom_id='bike_hell'),
                    Button(style=ButtonStyle.gray, label='SPECIAL PRICE FOR NEWBIE', emoji='🏷', disabled=True)
                ]
            ]
        )
        await ctx.send(
            file=discord.File('./img/bike/red.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='PURCHASE NOW', emoji='💵', custom_id='bike_red'),
                    Button(style=ButtonStyle.gray, label='SPECIAL PRICE FOR NEWBIE', emoji='🏷', disabled=True)
                ]
            ]
        )
        await ctx.send(
            file=discord.File('./img/bike/white.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='PURCHASE NOW', emoji='💵', custom_id='bike_white'),
                    Button(style=ButtonStyle.gray, label='SPECIAL PRICE FOR NEWBIE', emoji='🏷', disabled=True)
                ]
            ]
        )
        await ctx.send(
            file=discord.File('./img/bike/yellow.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='PURCHASE NOW', emoji='💵', custom_id='bike_yellow'),
                    Button(style=ButtonStyle.gray, label='SPECIAL PRICE FOR NEWBIE', emoji='🏷', disabled=True)
                ]
            ]
        )

        await ctx.message.delete()

def setup(bot):
    bot.add_cog(StoreBikeCommand(bot))
