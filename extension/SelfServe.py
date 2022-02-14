from discord.ext import commands
from discord_components import Button, ButtonStyle


class ServerStore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
