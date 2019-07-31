import discord
from discord.ext import commands, tasks
import json
from asyncio import sleep
from random import shuffle, choice
from itertools import cycle
from settings import Config



class Poker(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.hands = "https://www.onlinepokeramerica.com/wp-content/uploads/2019/06/poker-hands-ranking-guide.png.webp"
        self.cards = {"2C": "https://i.imgur.com/YE6Y0xi.png","2D": "https://i.imgur.com/rlqtbq6.png","2H": "https://i.imgur.com/E2I0mke.png","2S": "https://i.imgur.com/PBP09Ou.png","3C": "https://i.imgur.com/W8bWQxL.png","3D": "https://i.imgur.com/WZaFIo7.png","3H": "https://i.imgur.com/HMaCf2g.png","3S": "https://i.imgur.com/IVmxIZ3.png","4C": "https://i.imgur.com/QLtZdFQ.png","4D": "https://i.imgur.com/bIxtsOR.png","4H": "https://i.imgur.com/6InSYk8.png","4S": "https://i.imgur.com/iMQE2j5.png","5C": "https://i.imgur.com/rkJb8py.png","5D": "https://i.imgur.com/aluVr0k.png","5H": "https://i.imgur.com/A2JLueg.png","5S": "https://i.imgur.com/fsHq7dk.png","6C": "https://i.imgur.com/DNXUPS1.png","6D": "https://i.imgur.com/xgHZDiG.png","6H": "https://i.imgur.com/GUElC4n.png","6S": "https://i.imgur.com/Tq3xaAE.png","7C": "https://i.imgur.com/umKAYfw.png","7D": "https://i.imgur.com/EfFLsN5.png","7H": "https://i.imgur.com/vMBUvTn.png","7S": "https://i.imgur.com/JnyQ25e.png","8C": "https://i.imgur.com/BMNl6up.png","8D": "https://i.imgur.com/TlPswHp.png","8H": "https://i.imgur.com/TZmMuvY.png","8S": "https://i.imgur.com/uYL3xba.png","9C": "https://i.imgur.com/hbtPGRO.png","9D": "https://i.imgur.com/YvIKVwe.png","9H": "https://i.imgur.com/b8cMp6V.png","9S": "https://i.imgur.com/8Dh4D81.png","10C": "https://i.imgur.com/4t9tpHQ.png","10D": "https://i.imgur.com/JMHzLnz.png","10H": "https://i.imgur.com/NNDQWK1.png","10S": "https://i.imgur.com/ktpnJNn.png","AC": "https://i.imgur.com/8y7L0rW.png","AD": "https://i.imgur.com/F7cFzgO.png","AH": "https://i.imgur.com/1xbTnpb.png","AS": "https://i.imgur.com/lXNters.png","JC": "https://i.imgur.com/vavnltw.png","JD": "https://i.imgur.com/a69jZih.png","JH": "","JS": "","QC": "https://i.imgur.com/d5LHM36.png","QD": "https://i.imgur.com/au5jk1d.png","QH": "https://i.imgur.com/5B1jZLZ.png","QS": "https://i.imgur.com/34CtenH.png","KC": "https://i.imgur.com/Ywfdxbo.png","KD": "https://i.imgur.com/MaiasTy.png","KH": "https://i.imgur.com/v5Ud3Wb.png","KS": "https://i.imgur.com/khs4yiY.png"}
        self.tables = {}
        self.pms = {}
        #self.turn = {}
        
    def checkPokerCmds(self, ctx):
        return self.tables[ctx.guild.id]["turn"] == ctx.author

    def checkStarted(self, ctx):
        return not self.tables[ctx.guild.id]["started"]

    async def setupRounds(self, ctx):
        sID = ctx.guild.id
        pokerCh = self.client.get_channel(Config.servers[str(sID)]["poker"])
        inplay = self.cards
        for i in range(3):
            if i == 0:   
                for player in self.tables[sID]["players"]:
                    pCards = player.cards
                    pCards = cycle([inplay.pop(choice(inplay.keys)), inplay.pop(choice(inplay.keys))])
                    
                    embed = discord.Embed(title="Suas cartas", description="Reaja para ver sua outra carta", colour=discord.Color.blue)
                    embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
                    embed.set_image(url=self.cards[next(pCards)])

                    self.pms[player.id] = await player.send(embed=embed)
                    await self.pms[player.id].add_reaction("eggplant")
                    


    @commands.command()
    @commands.check(checkStarted)
    async def poker(self, ctx):
        sID = ctx.guild.id
        pokerCh = self.client.get_channel(Config.servers[str(sID)]["poker"])
        if not self.tables[sID]:
            self.tables[sID] = {"players": [ctx.author], "started": False, "bet": 0, "turn": None}
            await pokerCh.send(f"{ctx.author.mention}, sua mesa foi criada! Esperando outros jogadores...")
        else:
            self.tables[sID]["players"].append(ctx.author)
            mentions = f""
            for user in self.tables[sID]["players"]:
                mentions += f"{user.mention} "
            await pokerCh.send(f"{mentions}, a rodada irá começar em 45 segundos! Suas cartas serão entregues no privado. GL HF :)")
            # task to edit timer
            await sleep(45)
            shuffle(self.tables[sID]["players"])
            self.tables[sID]["started"] = True
            await self.setupRounds(ctx)
            # permitir uso dos comandos de "check", "bet", "raise" e "fold", utilizando um custom check.

    @commands.command()
    @commands.check(checkPokerCmds)
    async def check(self, ctx):
        sID = ctx.guild.id
        pokerCh = self.client.get_channel(Config.servers[str(sID)]["poker"])

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if not reaction.me:
            if reaction.message in self.pms:
                if reaction.emoji.name == "eggplant":
                    for player in self.tables[reaction.message.guild.id]["players"]:
                        if player == user:
                            pCards = player.cards
                            embed = discord.Embed(title="Suas cartas", description="Reaja para ver sua outra carta", colour=discord.Color.blue)
                            embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
                            embed.set_image(url=self.cards[next(pCards)]) 
                            await reaction.message.edit(embed=embed)
                            await reaction.remove(user)


    async def waitPlayerMove(self, ctx):
        sID = ctx.guild.id
        pokerCh = self.client.get_channel(Config.servers[str(sID)]["poker"])
        player = self.tables[sID]["turn"]

        def isCmd(msg):
            cmds = [".check", ".bet", ".raise", ".fold"]
            for cmd in cmds:
                if msg.content.startswith(cmd):
                    return True
            return False
        try:
            await self.client.wait_for("message", check=isCmd, timeout=30)
        except Exception as e:
            if isinstance(e, TimeoutError):
                await pokerCh.send(f"{player.mention} seu tempo acabou, portanto você deu fold!")
                # Force fold


                
            



def setup(client):
    client.add_cog(Poker(client))
    print("Poker being loaded!")

def teardown(client):
    print("Poker being unloaded!")