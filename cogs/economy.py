import discord
from discord.ext import commands, tasks
from data import uData

def verify_me(ctx):
    if ctx.author.id == 210563549200777216:
        return True
    else:
        return False

class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def bank(self, ctx):
        embed = discord.Embed(title="Banco", description="Aqui você pode ver todas as moedas, e quanto tem de cada uma!", colour=discord.Color.gold())
        embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
        for currency in uData.currs:
            embed.add_field(name=f"**{currency}**", value=f"***{uData.data[str(ctx.author.id)][currency]}***")
        
        await ctx.send(embed=embed)

    @commands.command()
    async def chips(self, ctx, amount):
        player = ctx.author
        amount = int(amount)
        if uData.currGet(player.id, "Niobium Oshit", amount):
            uData.currGive(player.id, "Chips", amount*10)
        
        await ctx.send(content=f"{player.mention} você trocou {str(amount)} NO's por {str(amount*10)} fichas de poker.")
    
    @commands.command()
    async def c2n(self, ctx, amount):
        player = ctx.author
        amount = int(amount)
        if uData.currGet(player.id, "Chips", amount):
            uData.currGive(player.id, "Niobium Oshit", amount/10)
        
        await ctx.send(content=f"{player.mention} você trocou {str(amount)} fichas por {str(amount/10)} NO's.")


    @commands.command()
    @commands.check(verify_me)
    async def give(self, ctx, userID, curr, amount):
        amount = int(amount)
        uData.currGive(userID, curr, amount)


def setup(client):
    client.add_cog(Economy(client))
    print("Economy being loaded!")

def teardown(client):
    print("Economy being unloaded!")