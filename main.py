import discord
from discord.ext import commands
import os
import config

client = commands.Bot(command_prefix=".")
path = config.path

# Cogs management commands
@client.command()
@commands.has_permissions(administrator=True)
async def reload(ctx, ext):
    if ext is None:
        await ctx.send("Você esqueceu do parametro 'extensão'!")
    else:
        client.reload_extension(f'cogs.{ext}')
@client.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, ext):
    if ext is None:
        await ctx.send("Você esqueceu do parametro 'extensão'!")
    else:
        client.unload_extension(f'cogs.{ext}')
@client.command()
@commands.has_permissions(administrator=True)
async def load(ctx, ext):
    if ext is None:
        await ctx.send("Você esqueceu do parametro 'extensão'!")
    else:
        client.load_extension(f'cogs.{ext}')


# Load cogs automatically
if os.path.exists(path):
    for filename in os.listdir(path):
        if filename.endswith('.py'):
            client.load_extension(f'{path}.{filename[:-3]}')

# Start client with token
client.run(config.token)