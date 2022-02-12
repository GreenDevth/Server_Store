import discord
from discord.ext import commands
from discord_components import DiscordComponents
from config.auth import get_token, config_cogs

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents)
DiscordComponents(bot)
token = get_token(8)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(type=discord.ActivityType.watching, name='Discord Store.')
    )


config_cogs(bot)

bot.run(token)
