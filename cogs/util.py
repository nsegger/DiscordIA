import discord
from discord.ext import commands, tasks
import json
from itertools import cycle
from settings import Config
from data import uData

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
            for member in guild.members:
                if not(str(member.id) in uData.data):
                    uData.data[str(member.id)] = {}
                    for currency in uData.currs:
                        uData.data[str(member.id)][currency] = 0
                    uData.data[str(member.id)]["Niobium Oshit"] = 1000
        


    # Commands decorator
    @commands.command()
    async def ping(self, ctx):
       await ctx.send(f'```{round(self.client.latency * 1000)} ms```')

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="Comandos", description="Aqui você pode ver todos os comandos, e o que fazem!", colour=discord.Color.blue())
        embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
        embed.add_field(name=f".config", value=f"Configura os canais usados, opções: **logs/welcome/amsht/poker**", inline=False)
        embed.add_field(name=f".purge", value=f"Apaga o número de mensagens especificado", inline=False)
        embed.add_field(name=f".amoedo", value=f"Gera uma imagem do Amoedo com a frase especificada", inline=False)
        embed.add_field(name=f".poker", value=f"Cria/entra em uma mesa de poker **(use .phelp p/ ajuda em poker)**", inline=False)
        embed.add_field(name=f".bank", value=f"Mostra todas as moedas e quanto você tem de cada", inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command()
    async def phelp(self, ctx):
        embed = discord.Embed(title="Comandos do Poker", description="Aqui você pode ver todos os comandos do Poker, e o que fazem!", colour=discord.Color.red())
        embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
        embed.add_field(name=f".chips", value=f"Compra fichas utilizando o valor de Niobium especificado", inline=False)
        embed.add_field(name=f".c2n", value=f"Vende quantidade fichas especificada de fichas", inline=False)
        embed.add_field(name=f".pstart", value=f"Inicia uma mesa de poker", inline=False)
        embed.add_field(name=f".check", value=f"Passa a vez", inline=False)
        embed.add_field(name=f".bet", value=f"Aposta", inline=False)
        embed.add_field(name=f".raise", value=f"Aumenta a aposta", inline=False)
        embed.add_field(name=f".fold", value=f"Desiste da mão", inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def pnc(self, ctx):
       await ctx.send(f'Pau no cu do first')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount=2):
        await ctx.channel.purge(limit=amount+1)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def config(self, ctx, option, chName):
        guild = ctx.guild
        channels = guild.text_channels
        options = ["logs", "welcome", "amsht", "poker"]
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
    uData.saveData()
    print("Util being unloaded!")