import discord
from discord.ext import commands, tasks
from config import status

class Util(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Events decorator
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(status=discord.Status.online)
        self.updateActivity.start()
        print(f"Bot is ready! Logged as {self.client.user}")
    
    # Commands decorator
    @commands.command()
    async def ping(self, ctx):
       await ctx.send(f'{round(self.client.latency * 1000)} ms')
    #@commands.command()
    #async def fping(self, ctx):
    #    await ctx.send(f'{self.client.latency}')
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount=2):
        await ctx.channel.purge(limit=amount+1)

    # Tasks decorator
    @tasks.loop(seconds=3)
    async def updateActivity(self):
        await self.client.change_presence(activity=discord.Game(next(status)))



def setup(client):
    client.add_cog(Util(client))
    print("Util loaded!")

def teardown(client):
    print("Util unloaded!")