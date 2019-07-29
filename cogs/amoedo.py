import discord
from discord.ext import commands
from io import BytesIO
from base64 import b64decode
from amoedogen.Generator import Generator
import requests


class Amoedo(commands.Cog):
    def __init__(self, client):
        self.client = client

    def __genAmoedo(self, text):
        gen = Generator()
        gen.write(text, color="blue", rect=True, base_64=True)
        img64 = gen.result
        return img64

    @commands.command()
    async def amoedo(self, ctx, member: discord.Member, *, text):
        text = text.replace("\\n", "\n")
        text = f'{member.nick} {text}'
        img64 = self.__genAmoedo(text)
        await ctx.send(file=discord.File(BytesIO(b64decode(img64)), f"a{ctx.author}.jpeg"))
    async def pera(self, ctx):
        text = "Pera,\no homem mais forte\ndo universo"
        img64 = self.__genAmoedo(text)
        Pera = self.client.get_user(277915595184406529)
        await ctx.send(content=Pera.mention, file=discord.File(BytesIO(b64decode(img64)), f"a{ctx.author}.jpeg"))

def setup(client):
    client.add_cog(Amoedo(client))
    print("Amoedo loaded!")

def teardown(client):
    print("Amoedo unloaded!")