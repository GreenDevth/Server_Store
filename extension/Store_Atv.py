import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle

class StoreAtvCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='atv')
    async def atv_command(self, ctx):
       
        await ctx.send(
            file=discord.File('./img/atv/blue.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='สั่งซื้อตอนนี้', emoji='💵', custom_id='atv_blue'),
                    Button(style=ButtonStyle.gray, label='สำหรับผู้เล่นใหม่และสั่งซื้อครั้งแรกจะได้รับในราคาพิเศษ', emoji='🏷', disabled=True),
                ]
            ]
        )
        await ctx.send(
            file=discord.File('./img/atv/camo.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='สั่งซื้อตอนนี้', emoji='💵', custom_id='atv_camo'),
                    Button(style=ButtonStyle.gray, label='สำหรับผู้เล่นใหม่และสั่งซื้อครั้งแรกจะได้รับในราคาพิเศษ', emoji='🏷', disabled=True),
                ]
            ]
        )
        await ctx.send(
            file=discord.File('./img/atv/red.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='สั่งซื้อตอนนี้', emoji='💵', custom_id='atv_red'),
                    Button(style=ButtonStyle.gray, label='สำหรับผู้เล่นใหม่และสั่งซื้อครั้งแรกจะได้รับในราคาพิเศษ', emoji='🏷', disabled=True),
                ]
            ]
        )

        await ctx.send(
            file=discord.File('./img/atv/yellow.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='สั่งซื้อตอนนี้', emoji='💵', custom_id='atv_yellow'),
                    Button(style=ButtonStyle.gray, label='สำหรับผู้เล่นใหม่และสั่งซื้อครั้งแรกจะได้รับในราคาพิเศษ', emoji='🏷', disabled=True),
                ]
            ]
        )

        await ctx.message.delete()

def setup(bot):
    bot.add_cog(StoreAtvCommand(bot))
