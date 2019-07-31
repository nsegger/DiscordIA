import discord
from discord.ext import commands, tasks
import json
from asyncio import sleep
from random import shuffle, randrange
from itertools import cycle
from settings import Config



class Poker(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.hands = "https://www.onlinepokeramerica.com/wp-content/uploads/2019/06/poker-hands-ranking-guide.png.webp"
        self.cardNames = {"2C": "2 de paus","2D": "2 de ouros","2H": "2 de copas","2S": "2 de espadas","3C": "3 de paus","3D": "3 de ouros","3H": "3 de copas","3S": "3 de espadas","4C": "4 de paus","4D": "4 de ouros","4H": "4 de copas","4S": "4 de espadas","5C": "5 de paus","5D": "5 de ouros","5H": "5 de copas","5S": "5 de espadas","6C": "6 de paus","6D": "6 de ouros","6H": "6 de copas","6S": "6 de espadas","7C": "7 de paus","7D": "7 de ouros","7H": "7 de copas","7S": "7 de espadas","8C": "8 de paus","8D": "8 de ouros","8H": "8 de copas","8S": "8 de espadas","9C": "9 de paus","9D": "9 de ouros","9H": "9 de copas","9S": "9 de espadas","10C": "10 de paus","10D": "10 de ouros","10H": "10 de copas","10S": "10 de espadas","JC": "Valete de paus","JD": "Valete de ouros","JH": "Valete de copas","JS": "Valete de espadas","QC": "Dama de paus","QD": "Dama de ouros","QH": "Dama de copas","QS": "Dama de espadas","KC": "Rei de paus","KD": "Rei de ouros","KH": "Rei de copas","KS": "Rei de espadas","AC": "Ás de paus","AD": "Ás de ouros","AH": "Ás de copas","AS": "Ás de espadas"}
        self.cUrl = {"2C": "https://i.imgur.com/YE6Y0xi.png","2D": "https://i.imgur.com/rlqtbq6.png","2H": "https://i.imgur.com/E2I0mke.png","2S": "https://i.imgur.com/PBP09Ou.png","3C": "https://i.imgur.com/W8bWQxL.png","3D": "https://i.imgur.com/WZaFIo7.png","3H": "https://i.imgur.com/HMaCf2g.png","3S": "https://i.imgur.com/IVmxIZ3.png","4C": "https://i.imgur.com/QLtZdFQ.png","4D": "https://i.imgur.com/bIxtsOR.png","4H": "https://i.imgur.com/6InSYk8.png","4S": "https://i.imgur.com/iMQE2j5.png","5C": "https://i.imgur.com/rkJb8py.png","5D": "https://i.imgur.com/aluVr0k.png","5H": "https://i.imgur.com/A2JLueg.png","5S": "https://i.imgur.com/fsHq7dk.png","6C": "https://i.imgur.com/DNXUPS1.png","6D": "https://i.imgur.com/xgHZDiG.png","6H": "https://i.imgur.com/GUElC4n.png","6S": "https://i.imgur.com/Tq3xaAE.png","7C": "https://i.imgur.com/umKAYfw.png","7D": "https://i.imgur.com/EfFLsN5.png","7H": "https://i.imgur.com/vMBUvTn.png","7S": "https://i.imgur.com/JnyQ25e.png","8C": "https://i.imgur.com/BMNl6up.png","8D": "https://i.imgur.com/TlPswHp.png","8H": "https://i.imgur.com/TZmMuvY.png","8S": "https://i.imgur.com/uYL3xba.png","9C": "https://i.imgur.com/hbtPGRO.png","9D": "https://i.imgur.com/YvIKVwe.png","9H": "https://i.imgur.com/b8cMp6V.png","9S": "https://i.imgur.com/8Dh4D81.png","10C": "https://i.imgur.com/4t9tpHQ.png","10D": "https://i.imgur.com/JMHzLnz.png","10H": "https://i.imgur.com/NNDQWK1.png","10S": "https://i.imgur.com/ktpnJNn.png","AC": "https://i.imgur.com/8y7L0rW.png","AD": "https://i.imgur.com/F7cFzgO.png","AH": "https://i.imgur.com/1xbTnpb.png","AS": "https://i.imgur.com/lXNters.png","JC": "https://i.imgur.com/vavnltw.png","JD": "https://i.imgur.com/a69jZih.png","JH": "https://i.imgur.com/CQomEkc.png","JS": "https://i.imgur.com/7DBmXyY.png","QC": "https://i.imgur.com/d5LHM36.png","QD": "https://i.imgur.com/au5jk1d.png","QH": "https://i.imgur.com/5B1jZLZ.png","QS": "https://i.imgur.com/34CtenH.png","KC": "https://i.imgur.com/Ywfdxbo.png","KD": "https://i.imgur.com/MaiasTy.png","KH": "https://i.imgur.com/v5Ud3Wb.png","KS": "https://i.imgur.com/khs4yiY.png"}
        self.cards = ["2C","2D","2H","2S","3C","3D","3H","3S","4C","4D","4H","4S","5C","5D","5H","5S","6C","6D","6H","6S","7C","7D","7H","7S","8C","8D","8H","8S","9C","9D","9H","9S","10C","10D","10H","10S","JC","JD","JH","JS","QC","QD","QH","QS","KC","KD","KH","KS","AC","AD","AH","AS"]
        self.tables = {}
        self.pms = {}
        self.comMsgs = {}
        self.playerCards = {}
        self.msgT = 10
        self.roundT = 30
        

    async def setupRounds(self, ctx):
        sID = ctx.guild.id
        pokerCh = self.client.get_channel(Config.servers[str(sID)]["poker"])
        inplay = self.cards
        for i in range(8):
            if i == 0:  
                # Dealing
                print("Dealing")
                for player in self.tables[sID]["players"]:
                    cArray = [inplay.pop(randrange(len(inplay))), inplay.pop(randrange(len(inplay)))]
                    self.playerCards[player.id] = cycle(cArray)
                    playerCards = self.playerCards[player.id]

                    embed = discord.Embed(title="Suas cartas", description="Reaja para ver sua outra carta", colour=discord.Color.blue())
                    embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
                    embed.set_image(url=self.cUrl[next(playerCards)])

                    self.pms[player.id] = await player.send(embed=embed)
                    await self.pms[player.id].add_reaction(u"\U0001F346")
                    self.pms[player.id] = self.pms[player.id].id

                lookT = 15
                lookMsg = await pokerCh.send(f"Vocês têm {lookT} segundos para olharem suas cartas!")
                while lookT > 0:
                    await sleep(1)
                    lookT -= 1
                    await lookMsg.edit(content=f"Vocês têm {lookT} segundos para olharem suas cartas!")
            elif i == 2:
                # Flop
                print("Flop")
                self.tables[sID]["comCards"] = [inplay.pop(randrange(len(inplay))), inplay.pop(randrange(len(inplay))), inplay.pop(randrange(len(inplay)))]
                self.tables[sID]["listCc"] = self.tables[sID]["comCards"]

                embed = discord.Embed(title="Cartas comunitárias", description="Reaja para ver as outras cartas, ou veja nos campos abaixo", colour=discord.Color.blue())
                embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
                for c in range(3):
                    embed.add_field(name=f"Carta {c+1}", value=self.cardNames[self.tables[sID]["comCards"][c]])

                self.tables[sID]["comCards"] = cycle(self.tables[sID]["comCards"])
                embed.set_image(url=self.cUrl[next(self.tables[sID]["comCards"])])

                comCardsMsg = await pokerCh.send(embed=embed)
                await comCardsMsg.add_reaction(u"\U0001F346")
                
                self.comMsgs[sID] = comCardsMsg.id
            elif i % 2 != 0:
                # Round (i = 1,3,5,7)
                print("Round")
                for player in self.tables[sID]["players"]:
                    self.tables[sID]["turn"] = player
                    await self.waitPlayerMove(sID)
                    await sleep(2)    # we have to sleep so the task is properly stopped.
            else:
                # Turn and river (i = 4, 6)
                print("Turn/river")
                self.tables[sID]["listCc"].append(inplay.pop(randrange(len(inplay))))
                self.tables[sID]["comCards"] = cycle(self.tables[sID]["listCc"])


                embed = discord.Embed(title="Cartas comunitárias", description="Reaja para ver as outras cartas, ou veja nos campos abaixo", colour=discord.Color.blue())
                embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
                for c in range(len(self.tables[sID]["listCc"])):
                    embed.add_field(name=f"Carta {c+1}", value=self.cardNames[self.tables[sID]["listCc"][c]])
                embed.set_image(url=self.cUrl[next(self.tables[sID]["comCards"])])

                comCardsMsg = await pokerCh.send(embed=embed)
                await comCardsMsg.add_reaction(u"\U0001F346")

                self.comMsgs[sID] = comCardsMsg.id

            


    @commands.command()
    async def poker(self, ctx):
        sID = ctx.guild.id
        pokerCh = self.client.get_channel(Config.servers[str(sID)]["poker"])
        if not sID in self.tables.keys():
            self.tables[sID] = {"players": [ctx.author], "started": False, "bet": 0, "turn": None, "comCards": [], "listCc": []}
            await pokerCh.send(f"{ctx.author.mention}, sua mesa foi criada! Para começar, use .pstart")
        elif not self.tables[sID]["started"]:
            if not ctx.author in self.tables[sID]["players"]:
                self.tables[sID]["players"].append(ctx.author)
                await pokerCh.send(f"{ctx.author.mention} entrou na mesa atual!")
            

    @commands.command()
    async def pstart(self, ctx):
        sID = ctx.guild.id
        pokerCh = self.client.get_channel(Config.servers[str(sID)]["poker"])
        parray = self.tables[sID]["players"]
        if len(parray) > 1:
            mentions = f""
            for user in self.tables[sID]["players"]:
                mentions += f"{user.mention} "
            msgStart = await pokerCh.send(f"{mentions}, a rodada irá começar em {str(self.msgT)} segundos! Suas cartas serão entregues no privado. GL HF :)")

            while self.msgT > 0:
                await sleep(1)
                self.msgT -= 1
                await msgStart.edit(content=f"{mentions}, a rodada irá começar em {str(self.msgT)} segundos! Suas cartas serão entregues no privado. GL HF :)")

            self.tables[sID]["started"] = True
            shuffle(self.tables[sID]["players"])
            await self.setupRounds(ctx)
            print("Mesa finalizada")
            # permitir uso dos comandos de "check", "bet", "raise" e "fold", utilizando um custom check.
        else:
            await pokerCh.send(f"Ai pessoal, o {ctx.author.mention} tá querendo jogar poker sozinho! Alguém dá 10 de QI pra esse cara, por favor.")

    @commands.command()
    async def check(self, ctx):
        player = self.tables[ctx.guild.id]["turn"]
        if player == ctx.author:
            sID = ctx.guild.id
            pokerCh = self.client.get_channel(Config.servers[str(sID)]["poker"])

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if not self.client.user == user:
            if reaction.message.id == self.pms[user.id]:
                if reaction.emoji == u"\U0001F346":
                    # Do I really need to do this for and check for user???
                    for server in self.tables:
                        if user in self.tables[server]["players"]:
                            playerCards = self.playerCards[user.id]
                            embed = discord.Embed(title="Suas cartas", description="Reaja para ver sua outra carta", colour=discord.Color.blue())
                            embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
                            embed.set_image(url=self.cUrl[next(playerCards)]) 
                            await reaction.message.edit(embed=embed)
            
            elif reaction.message.id == self.comMsgs[reaction.message.guild.id]:
                embed = discord.Embed(title="Cartas comunitárias", description="Reaja para ver as outras cartas, ou veja nos campos abaixo", colour=discord.Color.blue())
                embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)

                for c in range(len(self.tables[reaction.message.guild.id]["listCc"])):
                    embed.add_field(name=f"Carta {c+1}", value=self.cardNames[self.tables[reaction.message.guild.id]["listCc"][c]])

                embed.set_image(url=self.cUrl[next(self.tables[reaction.message.guild.id]["comCards"])])
                await reaction.message.edit(embed=embed)
                await reaction.remove(user)


    async def waitPlayerMove(self, sID):
        pokerCh = self.client.get_channel(Config.servers[str(sID)]["poker"])
        player = self.tables[sID]["turn"]

        def isCmd(msg):
            cmds = [".check", ".bet", ".raise", ".fold"]
            for cmd in cmds:
                if msg.content.startswith(cmd) and msg.author == player:
                    return True
            return False

        self.roundT = 30
        roundMsg = await pokerCh.send(f"{player.mention} é a sua vez! você tem {self.roundT} segundos para decidir sua jogada.")
        self.roundTimer.start(ch=pokerCh, player=player, msg=roundMsg)

        try:
            await self.client.wait_for("message", check=isCmd, timeout=30)
        except Exception as e:
            if isinstance(e, TimeoutError):
                await pokerCh.send(f"{player.mention} seu tempo acabou, portanto você deu fold!")
                # Force fold
        
        self.roundTimer.stop()

    @tasks.loop(count=30)
    async def roundTimer(self, ch, player, msg):
        await sleep(1)
        self.roundT -= 1
        await msg.edit(content=f"{player.mention} é a sua vez! você tem {self.roundT} segundos para decidir sua jogada.")
            



def setup(client):
    client.add_cog(Poker(client))
    print("Poker being loaded!")

def teardown(client):
    print("Poker being unloaded!")