import discord
import os
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='^', intents=intents)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('your mom'))
    print('coconuts.')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run('ODQyNjk5NzQzMTcxMTgyNjIz.YJ5HSw.T2wAPLy1_4We7QSRfbgZ_1RUU9c')
