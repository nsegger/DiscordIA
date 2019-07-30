import discord
from discord.ext import commands
from io import BytesIO
from base64 import b64decode
from amoedogen.Generator import Generator
from settings import Config


class Amoedo(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.peraID = 277915595184406529

    def __genAmoedo(self, text):
        gen = Generator()
        gen.write(text, color="blue", rect=True, base_64=True)
        img64 = gen.result
        return img64

    async def __perinha(self, channel):
        text = "Pera,\no homem mais forte\ndo universo"
        img64 = self.__genAmoedo(text)
        Pera = self.client.get_user(self.peraID)
        await channel.send(content=Pera.mention, file=discord.File(BytesIO(b64decode(img64)), f"a{self.peraID}.jpeg"))

    @commands.Cog.listener()
    async def on_message(self, message):
        mentions = message.mentions
        for user in mentions:
            if user.id == self.peraID and message.author != self.client.user:
                await self.__perinha(message.channel)


    @commands.command()
    async def amoedo(self, ctx, *, text):
        text = text.replace("\\n", "\n")
        img64 = self.__genAmoedo(text)
        chID = Config.servers[str(ctx.guild.id)]["amsht"]
        channel = self.client.get_channel(chID)
        await channel.send(file=discord.File(BytesIO(b64decode(img64)), f"a{ctx.author}.jpeg"))
    @commands.command()
    async def pera(self, ctx):
        await self.__perinha(ctx)
    

def setup(client):
    client.add_cog(Amoedo(client))
    print("Amoedo being loaded!")

def teardown(client):
    print("Amoedo being unloaded!")