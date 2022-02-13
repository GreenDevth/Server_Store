import discord
import random
from discord.ext import commands
from database.Store import *
from database.Players import players_exists, players
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
        check_player = players_exists(member.id)
        player = players(member.id)
        price = get_price(store_btn)
        if shop == 'Close':
            print('Shop is closed.')
            await interaction.respond(
                    content='ตอนนี้ ร้านค้ายังไม่เปิดทำการ กรุณามาใหม่ในช่วงเวลา 6 โมงเย็น ถึง เที่ยงคืน '
                            'ขออภัยในความไม่สะดวก')
        if store_btn == 'atv_blue':
            if check_player == 0:
                await interaction.respond(content=f'{member.name} ไม่พบข้อมูล Steam id ของคุณในระบบ')
            else:
                if player[7] == 0:
                    await interaction.respond(content='คุณได้รับสิทธิ์ในการสั่งซื้อรถในราคาผู้เล่นใหม่')
                else:
                    await interaction.respond(content='คุณได้ใช้สิทธิ์ในการสั่งซื้อครั้งแรกไปแล้ว')




def setup(bot):
    bot.add_cog(StoreButtonEventCommand(bot))
