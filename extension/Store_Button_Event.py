import discord
import random
from discord.ext import commands
from database.Store import *
from database.Players import *
from database.Bank import cash

code = random.randint(9, 999999)
order_number = f'order{code}'

shop = shop_is_open("12:00:00")

class StoreButtonEventCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        cmd_channel = self.bot.get_channel(925559937323659274)
        run_cmd_channel = self.bot.get_channel(927796274676260944)
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
        if shop == 'Close':
            print('Shop is closed.')
            await interaction.respond(
                    content='ตอนนี้ ร้านค้ายังไม่เปิดทำการ กรุณามาใหม่ในช่วงเวลา 6 โมงเย็น ถึง เที่ยงคืน '
                            'ขออภัยในความไม่สะดวก')
            return
        if store_btn == 'atv_blue':
            await interaction.respond(content=f'{member.name} clicked.')
            if price < player_coin:
                await interaction.respond(content='โปรดรอสักครู่ระบบกำลังตรวจสอบสิทธิ์ในการสั่งซื้อของคุณ')
                checkout_order = cash(member.id, price)
                if checkout_order == 1:
                    add_to_cart(member.id, member.name, p[3], order_number, store_btn)
                    queue = check_queue()
                    order = in_order(member.id)
                    await interaction.send(f"คำสั่งหมายเลข {order_number} {store_btn} กำลังดำเนินการจัดส่งให้คุณ")
                    await cmd_channel.send(
                        f'{member.mention} '
                        f'```คำสั่งซื้อหมายเลข {order_number} กำลังเตรียมการจัดส่งจากทั้งหมด {order}/{queue}```'
                    )

                    await run_cmd_channel.send('!checkout {}'.format(order_number))

            await interaction.respond(content='หรือยอดเงินในบัญชีของคุณไม่เพียงพอ')
        # if store_btn == 'atv_blue' and check_player == 1:
        #     if newbie == 0:
        #         await interaction.respond(content=f'ยินดีด้วยคุณได้ซื้อสินค้าในราคาพิเศษ {order_number} '
        #                                           'กำลังเตรียมการจัดส่งไปยังตัวผู้เล่นในเกมส์')
        #         add_to_cart(member.id, member.name, p[3], order_number, store_btn)
        #         newbie_pay = player_coin - newbie_get_price(f'{store_btn}_newbie')
        #         players_update_coin(member.id, newbie_pay)
        #         players_newbie_update(member.id)
        #
        #     if player_coin < price:
        #         await interaction.respond(content='ยอดเงินของคุณไม่เพียงพอสำหรับการสั่งซื้อครั้งนี้')
        #
        #     await interaction.respond(content='Continue for PURCHASE a cars')



def setup(bot):
    bot.add_cog(StoreButtonEventCommand(bot))
