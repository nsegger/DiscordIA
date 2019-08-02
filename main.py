import discord
from discord.ext import commands
import os
import json
from settings import Config

client = commands.Bot(command_prefix=".")
path = Config.bot["path"]
token = Config.bot["token"]

client.remove_command('help')

# Cogs management commands
@client.command()
@commands.has_permissions(administrator=True)
async def reload(ctx, ext):
        client.reload_extension(f'{path}.{ext}')
@client.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, ext):
        client.unload_extension(f'{path}.{ext}')
@client.command()
@commands.has_permissions(administrator=True)
async def load(ctx, ext):
        client.load_extension(f'{path}.{ext}')

# Load cogs automatically
if os.path.exists(path):
    for filename in os.listdir(path):
        if filename.endswith('.py'):
            client.load_extension(f'{path}.{filename[:-3]}')

# Start client with token
client.run(token)