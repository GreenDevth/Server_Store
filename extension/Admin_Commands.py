from discord.ext import commands


#
# def read_click_file():
#     latest_line = None
#     file = open('./txt/who_click.txt', 'rt')
#     while True:
#         line = file.readline()
#         if not line:
#             break
#         print(line)
#         latest_line = line
#     while True:
#         with open('./txt/who_click.txt', 'r') as f:
#             lines = f.readline()
#             if lines[-1] != latest_line:
#                 latest_line = lines[-1]
#                 print(lines[-1])
#                 return lines[-1]
#

class AdminCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    #
    # @commands.Cog.listener()
    # async def on_ready(self):
    #     user_click = read_click_file()
    #     log_channel = self.bot.get_channel(942361402134396979)
    #     schedule.every(5).seconds.do(read_click_file)
    #     await log_channel.send(f'{user_click}')
    #     while True:
    #         schedule.run_pending()
    #         time.sleep(1)

    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, error):
    #     pass


def setup(bot):
    bot.add_cog(AdminCommand(bot))
