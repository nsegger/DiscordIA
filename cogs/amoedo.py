import discord
from discord.ext import commands
from io import BytesIO
from amoedogen.Generator import Generator
import requests


class Amoedo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def amoedo(self, ctx, *, text):
        gen = Generator()
        gen.write(text, color="blue", rect=True, base_64=True)
        img64 = gen.result
        
        await ctx.send(file=discord.File(BytesIO(img64)))

def setup(client):
    client.add_cog(Amoedo(client))
    print("Amoedo loaded!")

def teardown(client):
    print("Amoedo unloaded!")