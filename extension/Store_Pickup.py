import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle

class StorePickupCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='pickup')
    async def pickup_command(self, ctx):
        await ctx.send(
            file=discord.File('./img/pickup/black.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='PURCHASE NOW', emoji='💵', custom_id='pickup_black'),
                    Button(style=ButtonStyle.gray, label='SPECIAL PRICE FOR NEWBIE', emoji='🏷', disabled=True)
                ]
            ]
        )
        await ctx.send(
            file=discord.File('./img/pickup/blue.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='PURCHASE NOW', emoji='💵', custom_id='pickup_blue'),
                    Button(style=ButtonStyle.gray, label='SPECIAL PRICE FOR NEWBIE', emoji='🏷', disabled=True)
                ]
            ]
        )
        await ctx.send(
            file=discord.File('./img/pickup/red.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='PURCHASE NOW', emoji='💵', custom_id='pickup_red'),
                    Button(style=ButtonStyle.gray, label='SPECIAL PRICE FOR NEWBIE', emoji='🏷', disabled=True)
                ]
            ]
        )
        await ctx.send(
            file=discord.File('./img/pickup/camo.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='PURCHASE NOW', emoji='💵', custom_id='pickup_camo'),
                    Button(style=ButtonStyle.gray, label='SPECIAL PRICE FOR NEWBIE', emoji='🏷', disabled=True)
                ]
            ]
        )
        await ctx.send(
            file=discord.File('./img/pickup/red_white.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='PURCHASE NOW', emoji='💵', custom_id='pickup_red_white'),
                    Button(style=ButtonStyle.gray, label='SPECIAL PRICE FOR NEWBIE', emoji='🏷', disabled=True)
                ]
            ]
        )
        await ctx.send(
            file=discord.File('./img/pickup/orange.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='PURCHASE NOW', emoji='💵', custom_id='pickup_orange'),
                    Button(style=ButtonStyle.gray, label='SPECIAL PRICE FOR NEWBIE', emoji='🏷', disabled=True)
                ]
            ]
        )
        await ctx.send(
            file=discord.File('./img/pickup/hell.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='PURCHASE NOW', emoji='💵', custom_id='pickup_hell'),
                    Button(style=ButtonStyle.gray, label='SPECIAL PRICE FOR NEWBIE', emoji='🏷', disabled=True)
                ]
            ]
        )
        await ctx.send(
            file=discord.File('./img/pickup/white.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='PURCHASE NOW', emoji='💵', custom_id='pickup_white'),
                    Button(style=ButtonStyle.gray, label='SPECIAL PRICE FOR NEWBIE', emoji='🏷', disabled=True)
                ]
            ]
        )
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(StorePickupCommand(bot))
