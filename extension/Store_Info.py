import discord
from discord.ext import commands


class StoreInformationCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='store_info')
    async def store_info_command(self, ctx):
        await ctx.send(
            file=discord.File('./img/line.png')
        )
        await ctx.send(
            '📔 **คู่มือการใช้งาน Discord Store** '
            '\n\n🛒 **Discord Store** '
            '\nDiscord Store คือระบบซื้อขายไอเอมภายในเซิร์ฟโดยใช้ '
            'เหรียญที่ผู้เล่นสะสมได้จากการทำภารกิจ การแลกเปลี่ยน '
            'SCUM Money และการจ้างวานหรือแลกเปลี่ยนไอเทม '
            'ระหว่างผู้เล่นด้วยกัน ซึ่งการซื้อขายไอเทมของเซิร์ฟจะถูก '
            'จำกัดสิทธิ์ด้วยระบบ Level ซึ่งอาจมีการเปลี่ยนแปลงได้ '
            'ในอนาคต และในการใช้งาน Discord Store ผู้เล่นจะ '
            'ต้องลงทะเบียนรับ Bank ID โดยการใช้ Steam ID ที่ห้อง'
            ' <#918381749833171005>'
        )
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(StoreInformationCommand(bot))
