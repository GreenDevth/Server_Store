import discord
import requests
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

        if server_btn == 'bankstatement':
            await interaction.respond(content='show bank statement to player')

        if server_btn == 'dailypack':
            await interaction.respond(content='show dailypack statement to player')

        if server_btn == 'server':
            await interaction.respond(content='show server statement to player')

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
