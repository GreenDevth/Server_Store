import discord
import requests
import json
from discord.ext import commands
from discord_components import Button, ButtonStyle
from database.battlemetric import battlemetric

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
        jsonObj = response.json()
        scum_server = jsonObj['data']['attributes']['name']
        scum_ip = jsonObj['data']['attributes']['ip']
        scum_port = jsonObj['data']['attributes']['port']
        scum_player = jsonObj['data']['attributes']['players']
        scum_player_max = jsonObj['data']['attributes']['maxPlayers']
        scum_rank = jsonObj['data']['attributes']['rank']
        scum_status = jsonObj['data']['attributes']['status']
        scum_time = jsonObj['data']['attributes']['details']['time']
        scum_version = jsonObj['data']['attributes']['details']['version']
        print(jsonObj['data']['attributes']['players'])

        if server_btn == 'bankstatement':
            await interaction.respond(content='show bank statement to player')

        if server_btn == 'dailypack':
            await interaction.respond(content='show dailypack statement to player')

        if server_btn == 'server':
            await interaction.respond(
                content=f"```\nServer: {scum_server}" +
                        f"\nIP: {scum_ip}:{scum_port}" +
                        f"\nStatus: {scum_status}" +
                        f"\nTime in Game: {scum_time}" +
                        f"\nPlayers: {scum_player}/{scum_player_max}" +
                        f"\nRanking: #{scum_rank}" +
                        f"\nGame version: {scum_version}\n" +
                        f"\nServer Restarts Every 6 hours" +
                        f"\nVehicle 3 days of inactivity will be destroyed" +
                        f"\nDay 3.8 hours, Night 1 hours\n```",
            )

        if server_btn == 'status':
            await interaction.respond(content='show status statement to player')

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
