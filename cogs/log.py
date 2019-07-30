import discord
from discord.ext import commands
import json
from itertools import cycle
from settings import Config


class Logs(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        serverID = ctx.guild.id
        author = ctx.author
        channel = self.client.get_channel(Config.servers[str(serverID)]["logs"])
        if isinstance(error, commands.MissingRequiredArgument):
            await channel.send(f"{author.mention} ```Cade seus argumentos, parça?```")
        elif isinstance(error, commands.BadArgument):
            await channel.send(f"{author.mention} ```Argumento errado ae!```")
        elif isinstance(error, commands.CommandNotFound):
            await channel.send(f"{author.mention} ```Comando não existe não, seu tanso.```")
        elif isinstance(error, commands.TooManyArguments):
            await channel.send(f"{author.mention} ```Ta passando mais argumento do que precisa, imbecil.```")
        elif isinstance(error, commands.ExtensionNotFound):
            await channel.send(f"{author.mention} ```Essa porra de extensão nem existe brother.```")
        else:
            await channel.send(f"{author.mention} ```{error}```")


def setup(client):
    client.add_cog(Logs(client))
    print("Log being loaded!")

def teardown(client):
    print("Log being unloaded!")