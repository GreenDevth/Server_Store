from discord.ext import commands


class StoreButtonEventCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        store_btn = interaction.component.custom_id

        if store_btn == 'atv_blue':
            print(f'{member.name} clicked.')
            await interaction.respond(content=f'{member.name} click the button {store_btn}')


def setup(bot):
    bot.add_cog(StoreButtonEventCommand(bot))
