from discord.ext import commands


class AdminCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        pass


def setup(bot):
    bot.add_cog(AdminCommand(bot))