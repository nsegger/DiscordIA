import discord
from discord.ext import commands, tasks
import json
from itertools import cycle
from settings import Config

class Util(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cfg = {}
        self.cfg["status"] = cycle(Config.bot["status"])

    # Events decorator
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(status=discord.Status.online)
        self.updateActivity.start()
        print(f"Bot is ready! Logged as {self.client.user}")

        for guild in self.client.guilds:
            channel = guild.text_channels[0]
            await Config.cfgServerCreate(guild.id, channel)

    # Commands decorator
    @commands.command()
    async def ping(self, ctx):
       await ctx.send(f'```{round(self.client.latency * 1000)} ms```')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount=2):
        await ctx.channel.purge(limit=amount+1)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def config(self, ctx, option, chName):
        guild = ctx.guild
        channels = guild.text_channels
        options = ["logs", "welcome", "amsht"]
        if option in options:
            for channel in channels:
                if channel.name == chName:
                    Config.servers[str(guild.id)][option] = channel.id
                    await ctx.send(f"***```{option} configurado com sucesso!```***")
        else:
            await ctx.send(f"***```{option} inexistente!```***")
        

    # Tasks decorator
    @tasks.loop(seconds=5)
    async def updateActivity(self):
        await self.client.change_presence(activity=discord.Game(next(self.cfg["status"])))



def setup(client):
    client.add_cog(Util(client))
    print("Util being loaded!")

def teardown(client):
    Config.saveCfg()
    print("Util being unloaded!")