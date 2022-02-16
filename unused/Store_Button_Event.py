import json
import random
import requests
from datetime import datetime

from discord.ext import commands

from config.auth import get_token
from database.Players import players_exists, players, players_update_coin, players_newbie_update, daily_status, \
    update_daily_pack
from database.Store import shop_is_open, get_price, newbie_get_price, add_to_cart, check_queue, in_order

shop = shop_is_open("18:00:00")
token = get_token(2)
url = get_token(3)

auth = f"{token}"
head = {'Authorization': 'Brarer' + auth}


def who_click(member_name, member_id, click_btn):
    # Open the file in append & read mode ('a+')
    with open("./txt/who_click.txt", "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        name = str(member_name)
        discord_id = str(f"Discord ID: {member_id}")
        msg = f"{date_time} {discord_id} {name} {click_btn}"
        file_object.write("{}".format(msg.strip()))


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

        price = get_price(store_btn)
        newbie_price = newbie_get_price(f'{store_btn}_newbie')
        code = random.randint(9, 999999)
        order_number = f'order{code}'
        print(f'{member.name} clicked.')
        who_click(member.name, member.id, store_btn)

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

        if shop != 1:
            print(f'Shop is closed. {shop}')
            await interaction.respond(
                content='ตอนนี้ ร้านค้ายังไม่เปิดทำการ กรุณามาใหม่ในช่วงเวลา 6 โมงเย็น ถึง เที่ยงคืน '
                        'ขออภัยในความไม่สะดวก')
        else:
            if store_btn == 'dailypack':
                check = daily_status(member.id)
                if check == 0:
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
                if check == 1:
                    await interaction.respond(content='คุณได้ใช้สิทธิ์ในการรับ Daily Pack สำหรับวันนี้ไปแล้ว')

            """ Command Event For ATV """

            if store_btn == 'atv_blue':
                if check_player == 0:
                    await interaction.respond(content=f'{member.name} ไม่พบข้อมูล Steam id ของคุณในระบบ')
                else:
                    player = players(member.id)
                    if player[7] == 0:
                        await interaction.respond(
                            content='คุณได้รับสิทธิ์ในการสั่งซื้อรถในราคาผู้เล่นใหม่ '
                                    f'คำสั่งหมายเลข {order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                        pay = player[5] - newbie_price
                        players_update_coin(member.id, pay)
                        add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                        queue = check_queue()
                        order = in_order(member.id)
                        players_newbie_update(member.id)
                        await cmd_channel.send(f'{member.mention}'
                                               f'```{order_number} กำลังดำเนินจัดส่ง '
                                               f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                        await run_cmd_channel.send('!checkout {}'.format(order_number))
                    else:
                        if player[5] < price:
                            await interaction.respond(content='ยอดเงินของคุณไม่เพียงพอสำหรับการสั่งซื้อ')
                        else:
                            await interaction.respond(content=f'โปรดรอสักครู่ คำสั่งซื้อหมายเลข '
                                                              f'{order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                            pay = player[5] - price
                            players_update_coin(member.id, pay)
                            add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                            queue = check_queue()
                            order = in_order(member.id)

                            await cmd_channel.send(f'{member.mention}'
                                                   f'```{order_number} กำลังดำเนินจัดส่ง '
                                                   f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                            await run_cmd_channel.send('!checkout {}'.format(order_number))

            if store_btn == 'atv_camo':
                if check_player == 0:
                    await interaction.respond(content=f'{member.name} ไม่พบข้อมูล Steam id ของคุณในระบบ')
                else:
                    player = players(member.id)
                    if player[7] == 0:
                        await interaction.respond(
                            content='คุณได้รับสิทธิ์ในการสั่งซื้อรถในราคาผู้เล่นใหม่ '
                                    f'คำสั่งหมายเลข {order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                        pay = player[5] - newbie_price
                        players_update_coin(member.id, pay)
                        add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                        queue = check_queue()
                        order = in_order(member.id)
                        players_newbie_update(member.id)
                        await cmd_channel.send(f'{member.mention}'
                                               f'```{order_number} กำลังดำเนินจัดส่ง '
                                               f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                        await run_cmd_channel.send('!checkout {}'.format(order_number))
                    else:
                        if player[5] < price:
                            await interaction.respond(content='ยอดเงินของคุณไม่เพียงพอสำหรับการสั่งซื้อ')
                        else:
                            await interaction.respond(content=f'โปรดรอสักครู่ คำสั่งซื้อหมายเลข '
                                                              f'{order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                            pay = player[5] - price
                            players_update_coin(member.id, pay)
                            add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                            queue = check_queue()
                            order = in_order(member.id)

                            await cmd_channel.send(f'{member.mention}'
                                                   f'```{order_number} กำลังดำเนินจัดส่ง '
                                                   f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                            await run_cmd_channel.send('!checkout {}'.format(order_number))

            if store_btn == 'atv_red':
                if check_player == 0:
                    await interaction.respond(content=f'{member.name} ไม่พบข้อมูล Steam id ของคุณในระบบ')
                else:
                    player = players(member.id)
                    if player[7] == 0:
                        await interaction.respond(
                            content='คุณได้รับสิทธิ์ในการสั่งซื้อรถในราคาผู้เล่นใหม่ '
                                    f'คำสั่งหมายเลข {order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                        pay = player[5] - newbie_price
                        players_update_coin(member.id, pay)
                        add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                        queue = check_queue()
                        order = in_order(member.id)
                        players_newbie_update(member.id)
                        await cmd_channel.send(f'{member.mention}'
                                               f'```{order_number} กำลังดำเนินจัดส่ง '
                                               f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                        await run_cmd_channel.send('!checkout {}'.format(order_number))
                    else:
                        if player[5] < price:
                            await interaction.respond(content='ยอดเงินของคุณไม่เพียงพอสำหรับการสั่งซื้อ')
                        else:
                            await interaction.respond(content=f'โปรดรอสักครู่ คำสั่งซื้อหมายเลข '
                                                              f'{order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                            pay = player[5] - price
                            players_update_coin(member.id, pay)
                            add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                            queue = check_queue()
                            order = in_order(member.id)

                            await cmd_channel.send(f'{member.mention}'
                                                   f'```{order_number} กำลังดำเนินจัดส่ง '
                                                   f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                            await run_cmd_channel.send('!checkout {}'.format(order_number))

            if store_btn == 'atv_yellow':
                if check_player == 0:
                    await interaction.respond(content=f'{member.name} ไม่พบข้อมูล Steam id ของคุณในระบบ')
                else:
                    player = players(member.id)
                    if player[7] == 0:
                        await interaction.respond(
                            content='คุณได้รับสิทธิ์ในการสั่งซื้อรถในราคาผู้เล่นใหม่ '
                                    f'คำสั่งหมายเลข {order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                        pay = player[5] - newbie_price
                        players_update_coin(member.id, pay)
                        add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                        queue = check_queue()
                        order = in_order(member.id)
                        players_newbie_update(member.id)
                        await cmd_channel.send(f'{member.mention}'
                                               f'```{order_number} กำลังดำเนินจัดส่ง '
                                               f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                        await run_cmd_channel.send('!checkout {}'.format(order_number))
                    else:
                        if player[5] < price:
                            await interaction.respond(content='ยอดเงินของคุณไม่เพียงพอสำหรับการสั่งซื้อ')
                        else:
                            await interaction.respond(content=f'โปรดรอสักครู่ คำสั่งซื้อหมายเลข '
                                                              f'{order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                            pay = player[5] - price
                            players_update_coin(member.id, pay)
                            add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                            queue = check_queue()
                            order = in_order(member.id)
                            await cmd_channel.send(f'{member.mention}'
                                                   f'```{order_number} กำลังดำเนินจัดส่ง '
                                                   f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                            await run_cmd_channel.send('!checkout {}'.format(order_number))

            """ End Command Event For ATV """

            """ Start command for pickup """

            if store_btn == 'pickup_black':
                if check_player == 0:
                    await interaction.respond(content=f'{member.name} ไม่พบข้อมูล Steam id ของคุณในระบบ')
                else:
                    player = players(member.id)
                    if player[7] == 0:
                        await interaction.respond(
                            content='คุณได้รับสิทธิ์ในการสั่งซื้อรถในราคาผู้เล่นใหม่ '
                                    f'คำสั่งหมายเลข {order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                        pay = player[5] - newbie_price
                        players_update_coin(member.id, pay)
                        add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                        queue = check_queue()
                        order = in_order(member.id)
                        players_newbie_update(member.id)
                        await cmd_channel.send(f'{member.mention}'
                                               f'```{order_number} กำลังดำเนินจัดส่ง '
                                               f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                        await run_cmd_channel.send('!checkout {}'.format(order_number))
                    else:
                        if player[5] < price:
                            await interaction.respond(content='ยอดเงินของคุณไม่เพียงพอสำหรับการสั่งซื้อ')
                        else:
                            await interaction.respond(content=f'โปรดรอสักครู่ คำสั่งซื้อหมายเลข '
                                                              f'{order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                            pay = player[5] - price
                            players_update_coin(member.id, pay)
                            add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                            queue = check_queue()
                            order = in_order(member.id)

                            await cmd_channel.send(f'{member.mention}'
                                                   f'```{order_number} กำลังดำเนินจัดส่ง '
                                                   f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                            await run_cmd_channel.send('!checkout {}'.format(order_number))

            if store_btn == 'pickup_hell':
                if check_player == 0:
                    await interaction.respond(content=f'{member.name} ไม่พบข้อมูล Steam id ของคุณในระบบ')
                else:
                    player = players(member.id)
                    if player[7] == 0:
                        await interaction.respond(
                            content='คุณได้รับสิทธิ์ในการสั่งซื้อรถในราคาผู้เล่นใหม่ '
                                    f'คำสั่งหมายเลข {order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                        pay = player[5] - newbie_price
                        players_update_coin(member.id, pay)
                        add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                        queue = check_queue()
                        order = in_order(member.id)
                        players_newbie_update(member.id)
                        await cmd_channel.send(f'{member.mention}'
                                               f'```{order_number} กำลังดำเนินจัดส่ง '
                                               f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                        await run_cmd_channel.send('!checkout {}'.format(order_number))
                    else:
                        if player[5] < price:
                            await interaction.respond(content='ยอดเงินของคุณไม่เพียงพอสำหรับการสั่งซื้อ')
                        else:
                            await interaction.respond(content=f'โปรดรอสักครู่ คำสั่งซื้อหมายเลข '
                                                              f'{order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                            pay = player[5] - price
                            players_update_coin(member.id, pay)
                            add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                            queue = check_queue()
                            order = in_order(member.id)

                            await cmd_channel.send(f'{member.mention}'
                                                   f'```{order_number} กำลังดำเนินจัดส่ง '
                                                   f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                            await run_cmd_channel.send('!checkout {}'.format(order_number))

            if store_btn == 'pickup_camo':
                if check_player == 0:
                    await interaction.respond(content=f'{member.name} ไม่พบข้อมูล Steam id ของคุณในระบบ')
                else:
                    player = players(member.id)
                    if player[7] == 0:
                        await interaction.respond(
                            content='คุณได้รับสิทธิ์ในการสั่งซื้อรถในราคาผู้เล่นใหม่ '
                                    f'คำสั่งหมายเลข {order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                        pay = player[5] - newbie_price
                        players_update_coin(member.id, pay)
                        add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                        queue = check_queue()
                        order = in_order(member.id)
                        players_newbie_update(member.id)
                        await cmd_channel.send(f'{member.mention}'
                                               f'```{order_number} กำลังดำเนินจัดส่ง '
                                               f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                        await run_cmd_channel.send('!checkout {}'.format(order_number))
                    else:
                        if player[5] < price:
                            await interaction.respond(content='ยอดเงินของคุณไม่เพียงพอสำหรับการสั่งซื้อ')
                        else:
                            await interaction.respond(content=f'โปรดรอสักครู่ คำสั่งซื้อหมายเลข '
                                                              f'{order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                            pay = player[5] - price
                            players_update_coin(member.id, pay)
                            add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                            queue = check_queue()
                            order = in_order(member.id)

                            await cmd_channel.send(f'{member.mention}'
                                                   f'```{order_number} กำลังดำเนินจัดส่ง '
                                                   f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                            await run_cmd_channel.send('!checkout {}'.format(order_number))

            if store_btn == 'pickup_blue':
                if check_player == 0:
                    await interaction.respond(content=f'{member.name} ไม่พบข้อมูล Steam id ของคุณในระบบ')
                else:
                    player = players(member.id)
                    if player[7] == 0:
                        await interaction.respond(
                            content='คุณได้รับสิทธิ์ในการสั่งซื้อรถในราคาผู้เล่นใหม่ '
                                    f'คำสั่งหมายเลข {order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                        pay = player[5] - newbie_price
                        players_update_coin(member.id, pay)
                        add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                        queue = check_queue()
                        order = in_order(member.id)
                        players_newbie_update(member.id)
                        await cmd_channel.send(f'{member.mention}'
                                               f'```{order_number} กำลังดำเนินจัดส่ง '
                                               f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                        await run_cmd_channel.send('!checkout {}'.format(order_number))
                    else:
                        if player[5] < price:
                            await interaction.respond(content='ยอดเงินของคุณไม่เพียงพอสำหรับการสั่งซื้อ')
                        else:
                            await interaction.respond(content=f'โปรดรอสักครู่ คำสั่งซื้อหมายเลข '
                                                              f'{order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                            pay = player[5] - price
                            players_update_coin(member.id, pay)
                            add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                            queue = check_queue()
                            order = in_order(member.id)

                            await cmd_channel.send(f'{member.mention}'
                                                   f'```{order_number} กำลังดำเนินจัดส่ง '
                                                   f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                            await run_cmd_channel.send('!checkout {}'.format(order_number))

            if store_btn == 'pickup_red_white':
                if check_player == 0:
                    await interaction.respond(content=f'{member.name} ไม่พบข้อมูล Steam id ของคุณในระบบ')
                else:
                    player = players(member.id)
                    if player[7] == 0:
                        await interaction.respond(
                            content='คุณได้รับสิทธิ์ในการสั่งซื้อรถในราคาผู้เล่นใหม่ '
                                    f'คำสั่งหมายเลข {order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                        pay = player[5] - newbie_price
                        players_update_coin(member.id, pay)
                        add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                        queue = check_queue()
                        order = in_order(member.id)
                        players_newbie_update(member.id)
                        await cmd_channel.send(f'{member.mention}'
                                               f'```{order_number} กำลังดำเนินจัดส่ง '
                                               f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                        await run_cmd_channel.send('!checkout {}'.format(order_number))
                    else:
                        if player[5] < price:
                            await interaction.respond(content='ยอดเงินของคุณไม่เพียงพอสำหรับการสั่งซื้อ')
                        else:
                            await interaction.respond(content=f'โปรดรอสักครู่ คำสั่งซื้อหมายเลข '
                                                              f'{order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                            pay = player[5] - price
                            players_update_coin(member.id, pay)
                            add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                            queue = check_queue()
                            order = in_order(member.id)

                            await cmd_channel.send(f'{member.mention}'
                                                   f'```{order_number} กำลังดำเนินจัดส่ง '
                                                   f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                            await run_cmd_channel.send('!checkout {}'.format(order_number))

            if store_btn == 'pickup_white':
                if check_player == 0:
                    await interaction.respond(content=f'{member.name} ไม่พบข้อมูล Steam id ของคุณในระบบ')
                else:
                    player = players(member.id)
                    if player[7] == 0:
                        await interaction.respond(
                            content='คุณได้รับสิทธิ์ในการสั่งซื้อรถในราคาผู้เล่นใหม่ '
                                    f'คำสั่งหมายเลข {order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                        pay = player[5] - newbie_price
                        players_update_coin(member.id, pay)
                        add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                        queue = check_queue()
                        order = in_order(member.id)
                        players_newbie_update(member.id)
                        await cmd_channel.send(f'{member.mention}'
                                               f'```{order_number} กำลังดำเนินจัดส่ง '
                                               f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                        await run_cmd_channel.send('!checkout {}'.format(order_number))
                    else:
                        if player[5] < price:
                            await interaction.respond(content='ยอดเงินของคุณไม่เพียงพอสำหรับการสั่งซื้อ')
                        else:
                            await interaction.respond(content=f'โปรดรอสักครู่ คำสั่งซื้อหมายเลข '
                                                              f'{order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                            pay = player[5] - price
                            players_update_coin(member.id, pay)
                            add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                            queue = check_queue()
                            order = in_order(member.id)

                            await cmd_channel.send(f'{member.mention}'
                                                   f'```{order_number} กำลังดำเนินจัดส่ง '
                                                   f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                            await run_cmd_channel.send('!checkout {}'.format(order_number))

            if store_btn == 'pickup_red':
                if check_player == 0:
                    await interaction.respond(content=f'{member.name} ไม่พบข้อมูล Steam id ของคุณในระบบ')
                else:
                    player = players(member.id)
                    if player[7] == 0:
                        await interaction.respond(
                            content='คุณได้รับสิทธิ์ในการสั่งซื้อรถในราคาผู้เล่นใหม่ '
                                    f'คำสั่งหมายเลข {order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                        pay = player[5] - newbie_price
                        players_update_coin(member.id, pay)
                        add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                        queue = check_queue()
                        order = in_order(member.id)
                        players_newbie_update(member.id)
                        await cmd_channel.send(f'{member.mention}'
                                               f'```{order_number} กำลังดำเนินจัดส่ง '
                                               f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                        await run_cmd_channel.send('!checkout {}'.format(order_number))
                    else:
                        if player[5] < price:
                            await interaction.respond(content='ยอดเงินของคุณไม่เพียงพอสำหรับการสั่งซื้อ')
                        else:
                            await interaction.respond(content=f'โปรดรอสักครู่ คำสั่งซื้อหมายเลข '
                                                              f'{order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                            pay = player[5] - price
                            players_update_coin(member.id, pay)
                            add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                            queue = check_queue()
                            order = in_order(member.id)

                            await cmd_channel.send(f'{member.mention}'
                                                   f'```{order_number} กำลังดำเนินจัดส่ง '
                                                   f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                            await run_cmd_channel.send('!checkout {}'.format(order_number))

            if store_btn == 'pickup_orange':
                if check_player == 0:
                    await interaction.respond(content=f'{member.name} ไม่พบข้อมูล Steam id ของคุณในระบบ')
                else:
                    player = players(member.id)
                    if player[7] == 0:
                        await interaction.respond(
                            content='คุณได้รับสิทธิ์ในการสั่งซื้อรถในราคาผู้เล่นใหม่ '
                                    f'คำสั่งหมายเลข {order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                        pay = player[5] - newbie_price
                        players_update_coin(member.id, pay)
                        add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                        queue = check_queue()
                        order = in_order(member.id)
                        players_newbie_update(member.id)
                        await cmd_channel.send(f'{member.mention}'
                                               f'```{order_number} กำลังดำเนินจัดส่ง '
                                               f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                        await run_cmd_channel.send('!checkout {}'.format(order_number))
                    else:
                        if player[5] < price:
                            await interaction.respond(content='ยอดเงินของคุณไม่เพียงพอสำหรับการสั่งซื้อ')
                        else:
                            await interaction.respond(content=f'โปรดรอสักครู่ คำสั่งซื้อหมายเลข '
                                                              f'{order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                            pay = player[5] - price
                            players_update_coin(member.id, pay)
                            add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                            queue = check_queue()
                            order = in_order(member.id)

                            await cmd_channel.send(f'{member.mention}'
                                                   f'```{order_number} กำลังดำเนินจัดส่ง '
                                                   f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                            await run_cmd_channel.send('!checkout {}'.format(order_number))

            """ End command for pickup """

            """ Start command for suv """

            if store_btn == 'suv_orange':
                if check_player == 0:
                    await interaction.respond(content=f'{member.name} ไม่พบข้อมูล Steam id ของคุณในระบบ')
                else:
                    player = players(member.id)
                    if player[7] == 0:
                        await interaction.respond(
                            content='คุณได้รับสิทธิ์ในการสั่งซื้อรถในราคาผู้เล่นใหม่ '
                                    f'คำสั่งหมายเลข {order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                        pay = player[5] - newbie_price
                        players_update_coin(member.id, pay)
                        add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                        queue = check_queue()
                        order = in_order(member.id)
                        players_newbie_update(member.id)
                        await cmd_channel.send(f'{member.mention}'
                                               f'```{order_number} กำลังดำเนินจัดส่ง '
                                               f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                        await run_cmd_channel.send('!checkout {}'.format(order_number))
                    else:
                        if player[5] < price:
                            await interaction.respond(content='ยอดเงินของคุณไม่เพียงพอสำหรับการสั่งซื้อ')
                        else:
                            await interaction.respond(content=f'โปรดรอสักครู่ คำสั่งซื้อหมายเลข '
                                                              f'{order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                            pay = player[5] - price
                            players_update_coin(member.id, pay)
                            add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                            queue = check_queue()
                            order = in_order(member.id)

                            await cmd_channel.send(f'{member.mention}'
                                                   f'```{order_number} กำลังดำเนินจัดส่ง '
                                                   f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                            await run_cmd_channel.send('!checkout {}'.format(order_number))

            if store_btn == 'suv_blue':
                if check_player == 0:
                    await interaction.respond(content=f'{member.name} ไม่พบข้อมูล Steam id ของคุณในระบบ')
                else:
                    player = players(member.id)
                    if player[7] == 0:
                        await interaction.respond(
                            content='คุณได้รับสิทธิ์ในการสั่งซื้อรถในราคาผู้เล่นใหม่ '
                                    f'คำสั่งหมายเลข {order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                        pay = player[5] - newbie_price
                        players_update_coin(member.id, pay)
                        add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                        queue = check_queue()
                        order = in_order(member.id)
                        players_newbie_update(member.id)
                        await cmd_channel.send(f'{member.mention}'
                                               f'```{order_number} กำลังดำเนินจัดส่ง '
                                               f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                        await run_cmd_channel.send('!checkout {}'.format(order_number))
                    else:
                        if player[5] < price:
                            await interaction.respond(content='ยอดเงินของคุณไม่เพียงพอสำหรับการสั่งซื้อ')
                        else:
                            await interaction.respond(content=f'โปรดรอสักครู่ คำสั่งซื้อหมายเลข '
                                                              f'{order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                            pay = player[5] - price
                            players_update_coin(member.id, pay)
                            add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                            queue = check_queue()
                            order = in_order(member.id)

                            await cmd_channel.send(f'{member.mention}'
                                                   f'```{order_number} กำลังดำเนินจัดส่ง '
                                                   f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                            await run_cmd_channel.send('!checkout {}'.format(order_number))

            if store_btn == 'suv_black':
                if check_player == 0:
                    await interaction.respond(content=f'{member.name} ไม่พบข้อมูล Steam id ของคุณในระบบ')
                else:
                    player = players(member.id)
                    if player[7] == 0:
                        await interaction.respond(
                            content='คุณได้รับสิทธิ์ในการสั่งซื้อรถในราคาผู้เล่นใหม่ '
                                    f'คำสั่งหมายเลข {order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                        pay = player[5] - newbie_price
                        players_update_coin(member.id, pay)
                        add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                        queue = check_queue()
                        order = in_order(member.id)
                        players_newbie_update(member.id)
                        await cmd_channel.send(f'{member.mention}'
                                               f'```{order_number} กำลังดำเนินจัดส่ง '
                                               f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                        await run_cmd_channel.send('!checkout {}'.format(order_number))
                    else:
                        if player[5] < price:
                            await interaction.respond(content='ยอดเงินของคุณไม่เพียงพอสำหรับการสั่งซื้อ')
                        else:
                            await interaction.respond(content=f'โปรดรอสักครู่ คำสั่งซื้อหมายเลข '
                                                              f'{order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                            pay = player[5] - price
                            players_update_coin(member.id, pay)
                            add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                            queue = check_queue()
                            order = in_order(member.id)

                            await cmd_channel.send(f'{member.mention}'
                                                   f'```{order_number} กำลังดำเนินจัดส่ง '
                                                   f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                            await run_cmd_channel.send('!checkout {}'.format(order_number))

            if store_btn == 'suv_police_two':
                if check_player == 0:
                    await interaction.respond(content=f'{member.name} ไม่พบข้อมูล Steam id ของคุณในระบบ')
                else:
                    player = players(member.id)
                    if player[7] == 0:
                        await interaction.respond(
                            content='คุณได้รับสิทธิ์ในการสั่งซื้อรถในราคาผู้เล่นใหม่ '
                                    f'คำสั่งหมายเลข {order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                        pay = player[5] - newbie_price
                        players_update_coin(member.id, pay)
                        add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                        queue = check_queue()
                        order = in_order(member.id)
                        players_newbie_update(member.id)
                        await cmd_channel.send(f'{member.mention}'
                                               f'```{order_number} กำลังดำเนินจัดส่ง '
                                               f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                        await run_cmd_channel.send('!checkout {}'.format(order_number))
                    else:
                        if player[5] < price:
                            await interaction.respond(content='ยอดเงินของคุณไม่เพียงพอสำหรับการสั่งซื้อ')
                        else:
                            await interaction.respond(content=f'โปรดรอสักครู่ คำสั่งซื้อหมายเลข '
                                                              f'{order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                            pay = player[5] - price
                            players_update_coin(member.id, pay)
                            add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                            queue = check_queue()
                            order = in_order(member.id)

                            await cmd_channel.send(f'{member.mention}'
                                                   f'```{order_number} กำลังดำเนินจัดส่ง '
                                                   f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                            await run_cmd_channel.send('!checkout {}'.format(order_number))

            """ End command for suv """

            """ Start command for cruiser bike """

            if store_btn == 'cruiser_black':
                if check_player == 0:
                    await interaction.respond(content=f'{member.name} ไม่พบข้อมูล Steam id ของคุณในระบบ')
                else:
                    player = players(member.id)
                    if player[7] == 0:
                        await interaction.respond(
                            content='คุณได้รับสิทธิ์ในการสั่งซื้อรถในราคาผู้เล่นใหม่ '
                                    f'คำสั่งหมายเลข {order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                        pay = player[5] - newbie_price
                        players_update_coin(member.id, pay)
                        add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                        queue = check_queue()
                        order = in_order(member.id)
                        players_newbie_update(member.id)
                        await cmd_channel.send(f'{member.mention}'
                                               f'```{order_number} กำลังดำเนินจัดส่ง '
                                               f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                        await run_cmd_channel.send('!checkout {}'.format(order_number))
                    else:
                        if player[5] < price:
                            await interaction.respond(content='ยอดเงินของคุณไม่เพียงพอสำหรับการสั่งซื้อ')
                        else:
                            await interaction.respond(content=f'โปรดรอสักครู่ คำสั่งซื้อหมายเลข '
                                                              f'{order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                            pay = player[5] - price
                            players_update_coin(member.id, pay)
                            add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                            queue = check_queue()
                            order = in_order(member.id)

                            await cmd_channel.send(f'{member.mention}'
                                                   f'```{order_number} กำลังดำเนินจัดส่ง '
                                                   f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                            await run_cmd_channel.send('!checkout {}'.format(order_number))

            if store_btn == 'cruiser_red':
                if check_player == 0:
                    await interaction.respond(content=f'{member.name} ไม่พบข้อมูล Steam id ของคุณในระบบ')
                else:
                    player = players(member.id)
                    if player[7] == 0:
                        await interaction.respond(
                            content='คุณได้รับสิทธิ์ในการสั่งซื้อรถในราคาผู้เล่นใหม่ '
                                    f'คำสั่งหมายเลข {order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                        pay = player[5] - newbie_price
                        players_update_coin(member.id, pay)
                        add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                        queue = check_queue()
                        order = in_order(member.id)
                        players_newbie_update(member.id)
                        await cmd_channel.send(f'{member.mention}'
                                               f'```{order_number} กำลังดำเนินจัดส่ง '
                                               f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                        await run_cmd_channel.send('!checkout {}'.format(order_number))
                    else:
                        if player[5] < price:
                            await interaction.respond(content='ยอดเงินของคุณไม่เพียงพอสำหรับการสั่งซื้อ')
                        else:
                            await interaction.respond(content=f'โปรดรอสักครู่ คำสั่งซื้อหมายเลข '
                                                              f'{order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                            pay = player[5] - price
                            players_update_coin(member.id, pay)
                            add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                            queue = check_queue()
                            order = in_order(member.id)

                            await cmd_channel.send(f'{member.mention}'
                                                   f'```{order_number} กำลังดำเนินจัดส่ง '
                                                   f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                            await run_cmd_channel.send('!checkout {}'.format(order_number))

            if store_btn == 'cruiser_green':
                if check_player == 0:
                    await interaction.respond(content=f'{member.name} ไม่พบข้อมูล Steam id ของคุณในระบบ')
                else:
                    player = players(member.id)
                    if player[7] == 0:
                        await interaction.respond(
                            content='คุณได้รับสิทธิ์ในการสั่งซื้อรถในราคาผู้เล่นใหม่ '
                                    f'คำสั่งหมายเลข {order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                        pay = player[5] - newbie_price
                        players_update_coin(member.id, pay)
                        add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                        queue = check_queue()
                        order = in_order(member.id)
                        players_newbie_update(member.id)
                        await cmd_channel.send(f'{member.mention}'
                                               f'```{order_number} กำลังดำเนินจัดส่ง '
                                               f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                        await run_cmd_channel.send('!checkout {}'.format(order_number))
                    else:
                        if player[5] < price:
                            await interaction.respond(content='ยอดเงินของคุณไม่เพียงพอสำหรับการสั่งซื้อ')
                        else:
                            await interaction.respond(content=f'โปรดรอสักครู่ คำสั่งซื้อหมายเลข '
                                                              f'{order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                            pay = player[5] - price
                            players_update_coin(member.id, pay)
                            add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                            queue = check_queue()
                            order = in_order(member.id)

                            await cmd_channel.send(f'{member.mention}'
                                                   f'```{order_number} กำลังดำเนินจัดส่ง '
                                                   f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                            await run_cmd_channel.send('!checkout {}'.format(order_number))

            if store_btn == 'cruiser_blue':
                if check_player == 0:
                    await interaction.respond(content=f'{member.name} ไม่พบข้อมูล Steam id ของคุณในระบบ')
                else:
                    player = players(member.id)
                    if player[7] == 0:
                        await interaction.respond(
                            content='คุณได้รับสิทธิ์ในการสั่งซื้อรถในราคาผู้เล่นใหม่ '
                                    f'คำสั่งหมายเลข {order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                        pay = player[5] - newbie_price
                        players_update_coin(member.id, pay)
                        add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                        queue = check_queue()
                        order = in_order(member.id)
                        players_newbie_update(member.id)
                        await cmd_channel.send(f'{member.mention}'
                                               f'```{order_number} กำลังดำเนินจัดส่ง '
                                               f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                        await run_cmd_channel.send('!checkout {}'.format(order_number))
                    else:
                        if player[5] < price:
                            await interaction.respond(content='ยอดเงินของคุณไม่เพียงพอสำหรับการสั่งซื้อ')
                        else:
                            await interaction.respond(content=f'โปรดรอสักครู่ คำสั่งซื้อหมายเลข '
                                                              f'{order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                            pay = player[5] - price
                            players_update_coin(member.id, pay)
                            add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                            queue = check_queue()
                            order = in_order(member.id)

                            await cmd_channel.send(f'{member.mention}'
                                                   f'```{order_number} กำลังดำเนินจัดส่ง '
                                                   f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                            await run_cmd_channel.send('!checkout {}'.format(order_number))

            if store_btn == 'cruiser_violet':
                if check_player == 0:
                    await interaction.respond(content=f'{member.name} ไม่พบข้อมูล Steam id ของคุณในระบบ')
                else:
                    player = players(member.id)
                    if player[7] == 0:
                        await interaction.respond(
                            content='คุณได้รับสิทธิ์ในการสั่งซื้อรถในราคาผู้เล่นใหม่ '
                                    f'คำสั่งหมายเลข {order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                        pay = player[5] - newbie_price
                        players_update_coin(member.id, pay)
                        add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                        queue = check_queue()
                        order = in_order(member.id)
                        players_newbie_update(member.id)
                        await cmd_channel.send(f'{member.mention}'
                                               f'```{order_number} กำลังดำเนินจัดส่ง '
                                               f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                        await run_cmd_channel.send('!checkout {}'.format(order_number))
                    else:
                        if player[5] < price:
                            await interaction.respond(content='ยอดเงินของคุณไม่เพียงพอสำหรับการสั่งซื้อ')
                        else:
                            await interaction.respond(content=f'โปรดรอสักครู่ คำสั่งซื้อหมายเลข '
                                                              f'{order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                            pay = player[5] - price
                            players_update_coin(member.id, pay)
                            add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                            queue = check_queue()
                            order = in_order(member.id)

                            await cmd_channel.send(f'{member.mention}'
                                                   f'```{order_number} กำลังดำเนินจัดส่ง '
                                                   f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                            await run_cmd_channel.send('!checkout {}'.format(order_number))

            """ End command for cruiser bike """

            """ Start command for bike """

            if store_btn == 'bike_black':
                if check_player == 0:
                    await interaction.respond(content=f'{member.name} ไม่พบข้อมูล Steam id ของคุณในระบบ')
                else:
                    player = players(member.id)
                    if player[7] == 0:
                        await interaction.respond(
                            content='คุณได้รับสิทธิ์ในการสั่งซื้อรถในราคาผู้เล่นใหม่ '
                                    f'คำสั่งหมายเลข {order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                        pay = player[5] - newbie_price
                        players_update_coin(member.id, pay)
                        add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                        queue = check_queue()
                        order = in_order(member.id)
                        players_newbie_update(member.id)
                        await cmd_channel.send(f'{member.mention}'
                                               f'```{order_number} กำลังดำเนินจัดส่ง '
                                               f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                        await run_cmd_channel.send('!checkout {}'.format(order_number))
                    else:
                        if player[5] < price:
                            await interaction.respond(content='ยอดเงินของคุณไม่เพียงพอสำหรับการสั่งซื้อ')
                        else:
                            await interaction.respond(content=f'โปรดรอสักครู่ คำสั่งซื้อหมายเลข '
                                                              f'{order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                            pay = player[5] - price
                            players_update_coin(member.id, pay)
                            add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                            queue = check_queue()
                            order = in_order(member.id)

                            await cmd_channel.send(f'{member.mention}'
                                                   f'```{order_number} กำลังดำเนินจัดส่ง '
                                                   f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                            await run_cmd_channel.send('!checkout {}'.format(order_number))

            if store_btn == 'bike_hell':
                if check_player == 0:
                    await interaction.respond(content=f'{member.name} ไม่พบข้อมูล Steam id ของคุณในระบบ')
                else:
                    player = players(member.id)
                    if player[7] == 0:
                        await interaction.respond(
                            content='คุณได้รับสิทธิ์ในการสั่งซื้อรถในราคาผู้เล่นใหม่ '
                                    f'คำสั่งหมายเลข {order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                        pay = player[5] - newbie_price
                        players_update_coin(member.id, pay)
                        add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                        queue = check_queue()
                        order = in_order(member.id)
                        players_newbie_update(member.id)
                        await cmd_channel.send(f'{member.mention}'
                                               f'```{order_number} กำลังดำเนินจัดส่ง '
                                               f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                        await run_cmd_channel.send('!checkout {}'.format(order_number))
                    else:
                        if player[5] < price:
                            await interaction.respond(content='ยอดเงินของคุณไม่เพียงพอสำหรับการสั่งซื้อ')
                        else:
                            await interaction.respond(content=f'โปรดรอสักครู่ คำสั่งซื้อหมายเลข '
                                                              f'{order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                            pay = player[5] - price
                            players_update_coin(member.id, pay)
                            add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                            queue = check_queue()
                            order = in_order(member.id)

                            await cmd_channel.send(f'{member.mention}'
                                                   f'```{order_number} กำลังดำเนินจัดส่ง '
                                                   f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                            await run_cmd_channel.send('!checkout {}'.format(order_number))

            if store_btn == 'bike_yellow':
                if check_player == 0:
                    await interaction.respond(content=f'{member.name} ไม่พบข้อมูล Steam id ของคุณในระบบ')
                else:
                    player = players(member.id)
                    if player[7] == 0:
                        await interaction.respond(
                            content='คุณได้รับสิทธิ์ในการสั่งซื้อรถในราคาผู้เล่นใหม่ '
                                    f'คำสั่งหมายเลข {order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                        pay = player[5] - newbie_price
                        players_update_coin(member.id, pay)
                        add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                        queue = check_queue()
                        order = in_order(member.id)
                        players_newbie_update(member.id)
                        await cmd_channel.send(f'{member.mention}'
                                               f'```{order_number} กำลังดำเนินจัดส่ง '
                                               f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                        await run_cmd_channel.send('!checkout {}'.format(order_number))
                    else:
                        if player[5] < price:
                            await interaction.respond(content='ยอดเงินของคุณไม่เพียงพอสำหรับการสั่งซื้อ')
                        else:
                            await interaction.respond(content=f'โปรดรอสักครู่ คำสั่งซื้อหมายเลข '
                                                              f'{order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                            pay = player[5] - price
                            players_update_coin(member.id, pay)
                            add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                            queue = check_queue()
                            order = in_order(member.id)

                            await cmd_channel.send(f'{member.mention}'
                                                   f'```{order_number} กำลังดำเนินจัดส่ง '
                                                   f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                            await run_cmd_channel.send('!checkout {}'.format(order_number))

            if store_btn == 'bike_white':
                if check_player == 0:
                    await interaction.respond(content=f'{member.name} ไม่พบข้อมูล Steam id ของคุณในระบบ')
                else:
                    player = players(member.id)
                    if player[7] == 0:
                        await interaction.respond(
                            content='คุณได้รับสิทธิ์ในการสั่งซื้อรถในราคาผู้เล่นใหม่ '
                                    f'คำสั่งหมายเลข {order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                        pay = player[5] - newbie_price
                        players_update_coin(member.id, pay)
                        add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                        queue = check_queue()
                        order = in_order(member.id)
                        players_newbie_update(member.id)
                        await cmd_channel.send(f'{member.mention}'
                                               f'```{order_number} กำลังดำเนินจัดส่ง '
                                               f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                        await run_cmd_channel.send('!checkout {}'.format(order_number))
                    else:
                        if player[5] < price:
                            await interaction.respond(content='ยอดเงินของคุณไม่เพียงพอสำหรับการสั่งซื้อ')
                        else:
                            await interaction.respond(content=f'โปรดรอสักครู่ คำสั่งซื้อหมายเลข '
                                                              f'{order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                            pay = player[5] - price
                            players_update_coin(member.id, pay)
                            add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                            queue = check_queue()
                            order = in_order(member.id)

                            await cmd_channel.send(f'{member.mention}'
                                                   f'```{order_number} กำลังดำเนินจัดส่ง '
                                                   f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                            await run_cmd_channel.send('!checkout {}'.format(order_number))

            if store_btn == 'bike_blue':
                if check_player == 0:
                    await interaction.respond(content=f'{member.name} ไม่พบข้อมูล Steam id ของคุณในระบบ')
                else:
                    player = players(member.id)
                    if player[7] == 0:
                        await interaction.respond(
                            content='คุณได้รับสิทธิ์ในการสั่งซื้อรถในราคาผู้เล่นใหม่ '
                                    f'คำสั่งหมายเลข {order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                        pay = player[5] - newbie_price
                        players_update_coin(member.id, pay)
                        add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                        queue = check_queue()
                        order = in_order(member.id)
                        players_newbie_update(member.id)
                        await cmd_channel.send(f'{member.mention}'
                                               f'```{order_number} กำลังดำเนินจัดส่ง '
                                               f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                        await run_cmd_channel.send('!checkout {}'.format(order_number))
                    else:
                        if player[5] < price:
                            await interaction.respond(content='ยอดเงินของคุณไม่เพียงพอสำหรับการสั่งซื้อ')
                        else:
                            await interaction.respond(content=f'โปรดรอสักครู่ คำสั่งซื้อหมายเลข '
                                                              f'{order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                            pay = player[5] - price
                            players_update_coin(member.id, pay)
                            add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                            queue = check_queue()
                            order = in_order(member.id)

                            await cmd_channel.send(f'{member.mention}'
                                                   f'```{order_number} กำลังดำเนินจัดส่ง '
                                                   f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                            await run_cmd_channel.send('!checkout {}'.format(order_number))

            if store_btn == 'bike_green':
                if check_player == 0:
                    await interaction.respond(content=f'{member.name} ไม่พบข้อมูล Steam id ของคุณในระบบ')
                else:
                    player = players(member.id)
                    if player[7] == 0:
                        await interaction.respond(
                            content='คุณได้รับสิทธิ์ในการสั่งซื้อรถในราคาผู้เล่นใหม่ '
                                    f'คำสั่งหมายเลข {order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                        pay = player[5] - newbie_price
                        players_update_coin(member.id, pay)
                        add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                        queue = check_queue()
                        order = in_order(member.id)
                        players_newbie_update(member.id)
                        await cmd_channel.send(f'{member.mention}'
                                               f'```{order_number} กำลังดำเนินจัดส่ง '
                                               f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                        await run_cmd_channel.send('!checkout {}'.format(order_number))
                    else:
                        if player[5] < price:
                            await interaction.respond(content='ยอดเงินของคุณไม่เพียงพอสำหรับการสั่งซื้อ')
                        else:
                            await interaction.respond(content=f'โปรดรอสักครู่ คำสั่งซื้อหมายเลข '
                                                              f'{order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                            pay = player[5] - price
                            players_update_coin(member.id, pay)
                            add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                            queue = check_queue()
                            order = in_order(member.id)

                            await cmd_channel.send(f'{member.mention}'
                                                   f'```{order_number} กำลังดำเนินจัดส่ง '
                                                   f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                            await run_cmd_channel.send('!checkout {}'.format(order_number))

            if store_btn == 'bike_red':
                if check_player == 0:
                    await interaction.respond(content=f'{member.name} ไม่พบข้อมูล Steam id ของคุณในระบบ')
                else:
                    player = players(member.id)
                    if player[7] == 0:
                        await interaction.respond(
                            content='คุณได้รับสิทธิ์ในการสั่งซื้อรถในราคาผู้เล่นใหม่ '
                                    f'คำสั่งหมายเลข {order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                        pay = player[5] - newbie_price
                        players_update_coin(member.id, pay)
                        add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                        queue = check_queue()
                        order = in_order(member.id)
                        players_newbie_update(member.id)
                        await cmd_channel.send(f'{member.mention}'
                                               f'```{order_number} กำลังดำเนินจัดส่ง '
                                               f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                        await run_cmd_channel.send('!checkout {}'.format(order_number))
                    else:
                        if player[5] < price:
                            await interaction.respond(content='ยอดเงินของคุณไม่เพียงพอสำหรับการสั่งซื้อ')
                        else:
                            await interaction.respond(content=f'โปรดรอสักครู่ คำสั่งซื้อหมายเลข '
                                                              f'{order_number} กำลังดำเนินการจัดส่งไปยังตำแหน่งของคุณ')
                            pay = player[5] - price
                            players_update_coin(member.id, pay)
                            add_to_cart(member.id, member.name, player[3], order_number, store_btn)
                            queue = check_queue()
                            order = in_order(member.id)

                            await cmd_channel.send(f'{member.mention}'
                                                   f'```{order_number} กำลังดำเนินจัดส่ง '
                                                   f'จากรายการสั่งซื้อทั้งหมด {order}/{queue}```')
                            await run_cmd_channel.send('!checkout {}'.format(order_number))

            """ End command for  bike """


def setup(bot):
    bot.add_cog(StoreButtonEventCommand(bot))
