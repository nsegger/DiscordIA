import discord
from discord.ext import commands
import base64
import requests

amoedoURL = "http://amoedo-generator.herokuapp.com/generate"

class Amoedo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def amoedo(self, ctx, *, text):
        payload = {"text": text}
        img64 = requests.post(amoedoURL, data=payload)
        if img64.status_code == 200:
            imgdata = base64.b64decode(img64)
            filename = f'{ctx.author}.jpg'
            with open(filename, 'wb') as image:
                image.write(imgdata)
                await self.client.send_file(ctx.channel, image)
                image.close()
        else:
            await ctx.send(f'Não pude gerar a imagem:\n```STATUS: {img64.status_code}```')

def setup(client):
    client.add_cog(Amoedo(client))
    print("Amoedo loaded!")

def teardown(client):
    print("Amoedo unloaded!")