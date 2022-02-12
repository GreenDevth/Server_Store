import discord
from discord.ext import commands
from database.Store import *
from database.Players import *


class StoreButtonEventCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        store_btn = interaction.component.custom_id
        member = interaction.author
        p = players(member.id)
        player_coin = p[5]
        player_level = p[6]
        player_exp = p[8]
        newbie = p[7]
        check_player = players_exists(member.id)
        pack = get_command(store_btn)
        price = get_price(store_btn)
        minus = player_coin - price
        plus = player_coin + price

        if store_btn == 'atv_blue' and check_player == 1:
            if newbie == 0:
                newbie_pay = player_coin - newbie_get_price(f'{store_btn}_newbie')
                await interaction.respond(content=f'{newbie_pay}')

            # await interaction.respond(content='โปรดรอสักครู่ระบบกำลังตรวจสอบสิทธิ์ในการสั่งซื้อของคุณ')

            await interaction.respond(content=f'player not found {price} {player_coin}')
            # package = get_command(store_btn)
            # package_cmd = package.split(",")
            # await interaction.respond(content=f'{member.name} click the button {store_btn}')
            # for pack in package_cmd:
            #     await interaction.channel.send(f'{pack}')
            #     await asyncio.sleep(1)
            # await interaction.respond(content='คุณได้รับสิทธิ์ในการสั่งซื้อครั้งแรก')



def setup(bot):
    bot.add_cog(StoreButtonEventCommand(bot))
