import discord
import requests
import json
from datetime import datetime
from discord.ext import commands
from discord_components import Button, ButtonStyle
from database.battlemetric import battlemetric
from database.Players import players

token = str(battlemetric(2))
url = str(battlemetric(3))
auth = f"{token}"
head = {'Authorization': 'Brarer' + auth}


class ServerStore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
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
            if time < shop_open:
                await interaction.respond(
                    content='ตอนนี้ ร้านค้ายังไม่เปิดทำการ กรุณามาใหม่ในช่วงเวลา 6 โมงเย็น ถึง เที่ยงคืน '
                            'ขออภัยในความไม่สะดวก')
            await interaction.respond(content='show dailypack statement to player')

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
                    return 'Disabled'
                if player[7] == 0:
                    return 'Enabled'
            await interaction.respond(
                content=f'Discord Name : {player[1]} '
                        f'\nBank ID : {player[4]} '
                        f'\nCoins : {coin} '
                        f'\nExp : {player[8]} '
                        f'\nLevel : {player[6]} '
                        f'\nNewbie : {newbie_status()}'
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
