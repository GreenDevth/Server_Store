import discord
import requests
import json
import random
from datetime import datetime
from discord.ext import commands
from discord_components import Button, ButtonStyle
from database.battlemetric import battlemetric
from database.Players import players, daily_status, update_daily_pack
from database.Store import *
from config.auth import get_token

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
        member = interaction.author
        server_btn = interaction.component.custom_id
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
        player = players(member.id)
        coin = "${:,d}".format(player[5])
        # current dateTime
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        print(time)
        shop_open = "18:00:00"
        if server_btn == 'bankstatement':
            await interaction.respond(
                content=f"Name : '{player[1]}' "
                        f"\nBank ID : {player[4]} "
                        f"\nTotal : {coin}"
            )

        if server_btn == 'dailypack':
            code = random.randint(9, 999999)
            order_number = f'order{code}'
            if time < shop_open:
                await interaction.respond(
                    content='ตอนนี้ ร้านค้ายังไม่เปิดทำการ กรุณามาใหม่ในช่วงเวลา 6 โมงเย็น ถึง เที่ยงคืน '
                            'ขออภัยในความไม่สะดวก')
            check = daily_status(member.id)
            if shop_open< time and check == 0:
                add_to_cart(member.id, member.name, player[3], order_number, server_btn)
                queue = check_queue()
                order = in_order(member.id)
                update_daily_pack(member.id)
                await interaction.respond(content='โปรดรอสักครู่ระบบกำลังดำเนินจัดส่งสินค้าให้คุณ')
                await cmd_channel.send(
                    f'{member.mention} '
                    f'```คำสั่งซื้อหมายเลข {order_number} กำลังเตรียมการจัดส่งจากทั้งหมด {order}/{queue}```'
                )
                await run_cmd_channel.send('!checkout {}'.format(order_number))
            await interaction.respond(content='คุณได้ใช้สิทธิ์ในการรับ Daily Pack สำหรับวันนี้ไปแล้ว ')
        if server_btn == 'server':
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

        if server_btn == 'status':
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
