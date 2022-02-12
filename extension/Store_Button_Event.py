import asyncio

from discord.ext import commands
from database.Store import get_command


class StoreButtonEventCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        store_btn = interaction.component.custom_id

        if store_btn == 'atv_blue':
            print(f'{member.name} clicked.')
            package = get_command('mk18_full_set')
            package_cmd = package.split(",")
            await interaction.respond(content=f'{member.name} click the button {store_btn}')
            while True:
                pack = []
                if pack in package_cmd:
                    await interaction.channel.send(f'{pack}')
                    await asyncio.sleep(1)


def setup(bot):
    bot.add_cog(StoreButtonEventCommand(bot))
