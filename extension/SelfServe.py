import json
import random
from datetime import datetime

import requests
from discord.ext import commands
from discord_components import Button, ButtonStyle

from config.auth import get_token
from database.Players import players_exists, players, daily_status, \
    update_daily_pack
from database.Store import shop_is_open, get_price, newbie_get_price, add_to_cart, check_queue, in_order

shop = shop_is_open("18:00:00")
token = get_token(2)
url = get_token(3)

auth = f"{token}"
head = {'Authorization': 'Brarer' + auth}


class ServerStore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        cmd_channel = self.bot.get_channel(925559937323659274)
        run_cmd_channel = self.bot.get_channel(927796274676260944)
        store_btn = interaction.component.custom_id
        member = interaction.author
        check_player = players_exists(member.id)

        price = get_price(store_btn)
        newbie_price = newbie_get_price(f'{store_btn}_newbie')
        code = random.randint(9, 999999)
        order_number = f'order{code}'
        print(f'{member.name} clicked.')

        if store_btn == 'bankstatement':
            if check_player == 0:
                await interaction.respond(content=f'{member.name} ไม่พบข้อมูล Steam id ของคุณในระบบ')
            else:
                player = players(member.id)
                coin = "${:,d}".format(player[5])
                await interaction.respond(
                    content=f"Name : {player[1]} "
                            f"\nBank ID : {player[4]} "
                            f"\nTotal : {coin}"
                )

        if store_btn == 'server':
            response = requests.get("https://api.battlemetrics.com/servers/13458708", headers=head)
            res_text = response.text
            json.loads(res_text)
            json_obj = response.json()
            scum_server = json_obj['data']['attributes']['name']
            scum_ip = json_obj['data']['attributes']['ip']
            scum_port = json_obj['data']['attributes']['port']
            scum_player = json_obj['data']['attributes']['players']
            scum_player_max = json_obj['data']['attributes']['maxPlayers']
            scum_rank = json_obj['data']['attributes']['rank']
            scum_status = json_obj['data']['attributes']['status']
            scum_time = json_obj['data']['attributes']['details']['time']
            scum_version = json_obj['data']['attributes']['details']['version']
            await interaction.respond(
                content=f"```\nServer: {scum_server} "
                        f"\nIP: {scum_ip}:{scum_port} "
                        f"\nStatus: {scum_status} "
                        f"\nTime in Game: {scum_time} "
                        f"\nPlayers: {scum_player}/{scum_player_max} "
                        f"\nRanking: #{scum_rank} "
                        f"\nGame version: {scum_version}\n "
                        f"\nServer Restarts Every 6 hours "
                        f"\nDay 3.8 hours, Night 1 hours\n```",
            )

        if store_btn == 'status':
            if check_player == 0:
                await interaction.respond(content=f'{member.name} ไม่พบข้อมูล Steam id ของคุณในระบบ')
            else:
                player = players(member.id)
                coin = "${:,d}".format(player[5])

                def newbie_status():
                    if player[7] == 1:
                        return 'Already used.'
                    if player[7] == 0:
                        return 'Has been used.'

                await interaction.respond(
                    content=f'Discord Name : {player[1]} '
                            f'\nBank ID : {player[4]} '
                            f'\nCoins : {coin} '
                            f'\nExp : {player[8]} '
                            f'\nLevel : {player[6]} '
                            f'\nVehicle Specail Price : {newbie_status()}'
                )
        if store_btn == 'dailypack':
            shop_open = "18:00:00"
            now = datetime.now()
            time = now.strftime("%H:%M:%S")

            check = daily_status(member.id)
            if check == 0 and shop_open <= time:
                player = players(member.id)
                await interaction.respond(content='โปรดรอสักครู่ระบบกำลังดำเนินจัดส่งสินค้าให้คุณ')
                add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                queue = check_queue()
                order = in_order(member.id)
                update_daily_pack(member.id)
                await cmd_channel.send(
                    f'{member.mention} '
                    f'```คำสั่งซื้อหมายเลข {order_number} กำลังเตรียมการจัดส่งจากทั้งหมด {order}/{queue}```'
                )
                await run_cmd_channel.send('!checkout {}'.format(order_number))
                return
            elif check == 1:
                await interaction.respond(content='คุณได้ใช้สิทธิ์ในการรับ Daily Pack สำหรับวันนี้ไปแล้ว')
                return
            else:
                await interaction.respond(
                    content='ตอนนี้ ร้านค้ายังไม่เปิดทำการ กรุณามาใหม่ในช่วงเวลา 6 โมงเย็น ถึง เที่ยงคืน '
                            'ขออภัยในความไม่สะดวก')

    @commands.command(name='selfserve')
    async def selfserve_command(self, ctx):
        await ctx.send(
            "ปุ่มจัดการธุรกรรมด้วยตนเอง",
            components=[
                [
                    Button(style=ButtonStyle.gray, label='Bank Statement', emoji='🏦', custom_id='bankstatement'),
                    Button(style=ButtonStyle.gray, label='Daily Pack', emoji='🍔', custom_id='dailypack'),
                    Button(style=ButtonStyle.gray, label='Sever Status', emoji='🌐', custom_id='server'),
                    Button(style=ButtonStyle.gray, label='Player Status', emoji='⚙', custom_id='status')
                ]
            ]
        )


def setup(bot):
    bot.add_cog(ServerStore(bot))
