import discord
import random
from discord.ext import commands
from database.Store import *
from database.Players import *
from datetime import datetime


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
        code = random.randint(9, 999999)
        order_number = f'order{code}'
        # current dateTime
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        print(time)
        shop_open = "18:00:00"
        if time < shop_open:
            await interaction.respond(
                content='ตอนนี้ ร้านค้ายังไม่เปิดทำการ กรุณามาใหม่ในช่วงเวลา 6 โมงเย็น ถึง เที่ยงคืน '
                        'ขออภัยในความไม่สะดวก')
        if store_btn == 'atv_blue' and check_player == 1:
            if newbie == 0:
                await interaction.respond(content=f'ยินดีด้วยคุณได้ซื้อสินค้าในราคาพิเศษ {order_number} '
                                                  'กำลังเตรียมการจัดส่งไปยังตัวผู้เล่นในเกมส์')
                add_to_cart(member.id, member.name, p[3], order_number, store_btn)
                newbie_pay = player_coin - newbie_get_price(f'{store_btn}_newbie')
                players_update_coin(member.id, newbie_pay)
                players_newbie_update(member.id)

            if player_coin < price:
                await interaction.respond(content='ยอดเงินของคุณไม่เพียงพอสำหรับการสั่งซื้อครั้งนี้')

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
