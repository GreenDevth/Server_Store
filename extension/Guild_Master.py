from discord.ext import commands
from discord_components import Button, ButtonStyle


class AtGuildMasterCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='guild', invoke_without_command=True)
    @commands.has_role('Admin')
    async def guild_command(self, ctx):
        await ctx.reply('Command for admin only')


def setup(bot):
    bot.add_cog(AtGuildMasterCommand(bot))
