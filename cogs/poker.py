import discord
from discord.ext import commands, tasks
import json
from asyncio import sleep
from random import shuffle, randrange
from itertools import cycle
from settings import Config
from data import uData
from io import BytesIO
from images import image
from base64 import b64decode


class Card:
    def __init__(self, string):
        if len(string) > 2:
            self.value = string[:2]
            self.suit = string[2]
        else:
            self.value = string[0]
            self.suit = string[1]
        figs = ["J", "Q", "K", "A"]
        if self.value in figs:
            for i in range(len(figs)):
                if self.value == figs[i]:
                    self.value = i + 11
                    self.name = figs[i]
        else:
            self.name = self.value
            self.value = int(self.value)


class Poker(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.hands = "https://www.onlinepokeramerica.com/wp-content/uploads/2019/06/poker-hands-ranking-guide.png.webp"
        self.cardNames = Config.bot["suits"]
        self.cUrl = Config.bot["cards"]
        self.cards = ["2C","2D","2H","2S","3C","3D","3H","3S","4C","4D","4H","4S","5C","5D","5H","5S","6C","6D","6H","6S","7C","7D","7H","7S","8C","8D","8H","8S","9C","9D","9H","9S","10C","10D","10H","10S","JC","JD","JH","JS","QC","QD","QH","QS","KC","KD","KH","KS","AC","AD","AH","AS"]
        self.tables = {}
        #self.pms = {}
        #self.comMsgs = {}
        self.playerInfo = {}
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
                    self.playerInfo[player.id] = {}
                    self.playerInfo[player.id]["cards"] = [Card(inplay.pop(randrange(len(inplay)))) for i in range(2)]
                    self.playerInfo[player.id]["cards"].sort(key=lambda c: c.value, reverse=True)
                    #playerCards = cycle(self.playerInfo[player.id]["cards"])

                    #embed = discord.Embed(title="Suas cartas", description="Reaja para ver sua outra carta", colour=discord.Color.blue())
                    #embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
                    #card = next(playerCards)
                    #embed.set_image(url=self.cUrl[str(card.value)][card.suit])

                    #self.pms[player.id] = await player.send(embed=embed)
                    #await self.pms[player.id].add_reaction(u"\U0001F346")
                    #self.pms[player.id] = self.pms[player.id].id

                    img64 = image.joinImages([c.name + c.suit for c in self.playerInfo[player.id]["cards"]])
                    self.playerInfo[player.id]["hImg"] = img64

                    await pokerCh.send(f"{player.mention} pagou a aposta obrigatória de 100.")
                    self.tables[ctx.guild.id]["pot"] += 100
                    uData.currGet(player.id, "Chips", 100)
                    
                    await player.send(file=discord.File(BytesIO(b64decode(img64)), f"{player.id}.png"))
                    

                lookT = 15
                lookMsg = await pokerCh.send(f"Vocês têm {lookT} segundos para olharem suas cartas!")
                while lookT > 0:
                    await sleep(1)
                    lookT -= 1
                    await lookMsg.edit(content=f"Vocês têm {lookT} segundos para olharem suas cartas!")
            elif i == 2:
                # Flop
                print("Flop")
                self.tables[sID]["comCards"] = [Card(inplay.pop(randrange(len(inplay)))) for i in range(3)]
                self.tables[sID]["listCc"] = self.tables[sID]["comCards"]

                #embed = discord.Embed(title="Cartas comunitárias", description="Reaja para ver as outras cartas, ou veja nos campos abaixo", colour=discord.Color.blue())
                #embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
                #for c in range(3):
                #    card =  self.tables[sID]["listCc"][c]
                #    embed.add_field(name=f"Carta {c+1}", value=f"{card.name} de {self.cardNames[card.suit]}"

                #self.tables[sID]["comCards"] = cycle(self.tables[sID]["comCards"])
                #card = next(self.tables[sID]["comCards"])]
                #embed.set_image(url=self.cUrl[str(card.value)][card.suit])

                img64 = image.joinImages([c.name + c.suit for c in self.tables[sID]["listCc"]])

                await pokerCh.send(file=discord.File(BytesIO(b64decode(img64)), f"{sID}.png"))
                #await comCardsMsg.add_reaction(u"\U0001F346")
                
                #self.comMsgs[sID] = comCardsMsg.id
            elif i % 2 != 0:
                # Round (i = 1,3,5,7)
                print("Round")
                count = 0
                player = self.tables[sID]["players"][count]
                self.tables[sID]["lastRaise"] = self.tables[sID]["players"][-1]
                while player != self.tables[sID]["lastRaise"]:
                    self.tables[sID]["turn"] = player
                    await self.waitPlayerMove(sID)

                    if len(self.tables[sID]["players"]) == 1:
                        winner = self.tables[sID]["players"][0]
                        card = self.playerInfo[winner.id]["cards"][0]

                        if "handName" in self.playerInfo[winner.id]:
                            hand = self.playerInfo[winner.id]["handName"]
                            text = f"{winner.mention} ganhou com {hand}"
                        else:
                            text = f"{winner.mention} ganhou"
                        
                        await pokerCh.send(content=f"Cartas de {winner.mention}")
                        await pokerCh.send(file=discord.File(BytesIO(b64decode(self.playerInfo[winner.id]["hImg"])), f"{winner.id}.png"))
                        await pokerCh.send(content=text)

                        pot = self.tables[ctx.guild.id]["pot"]
                        uData.currGive(winner.id, "Chips", pot)
                        return
                    await sleep(2)    # we have to sleep so the task is properly stopped.

                    count += 1
                    if count < len(self.tables[sID]["players"]):
                        player = self.tables[sID]["players"][count]
                    else:
                        count = 0
                        player = self.tables[sID]["players"][count]
                self.tables[sID]["roundBet"] = 0
            else:
                # Turn and river (i = 4, 6)
                print("Turn/river")
                self.tables[sID]["listCc"].append(Card(inplay.pop(randrange(len(inplay)))))
                self.tables[sID]["comCards"] = cycle(self.tables[sID]["listCc"])


                #embed = discord.Embed(title="Cartas comunitárias", description="Reaja para ver as outras cartas, ou veja nos campos abaixo", colour=discord.Color.blue())
                #embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
                #for c in range(len(self.tables[sID]["listCc"])):
                #    card = self.tables[sID]["listCc"][c]
                #    embed.add_field(name=f"Carta {c+1}", value=f"{card.name} de {self.cardNames[card.suit]}"
                #
                #card = next(self.tables[sID]["comCards"])
                #embed.set_image(url=self.cUrl[str(card.value)][card.suit])]

                img64 = image.joinImages([c.name + c.suit for c in self.tables[sID]["listCc"]])

                comCardsMsg = await pokerCh.send(file=discord.File(BytesIO(b64decode(img64)), f"{sID}.png"))
                #await comCardsMsg.add_reaction(u"\U0001F346")
                
                #self.comMsgs[sID] = comCardsMsg.id

        await self.evaluatePlayersHands(sID)

        for player in self.tables[sID]["players"]:
            await pokerCh.send(content=f"Cartas de {player.mention}")
            await pokerCh.send(file=discord.File(BytesIO(b64decode(self.playerInfo[player.id]["hImg"])), f"{player.id}.png"))

        ties = []
        winner = self.tables[sID]["players"][0]
        ties.append(winner)
        strongestHand = self.playerInfo[winner.id]["strenght"]
        pList = self.tables[sID]["players"][1:]
        for player in pList:
            if self.playerInfo[player.id]["strenght"] > strongestHand:
                winner = player
                strongestHand = self.playerInfo[winner.id]["strenght"]
            elif self.playerInfo[player.id]["strenght"] == strongestHand:
                ties.append(player)

        print(f"Ties before: {ties}")
        pot = self.tables[sID]["pot"]
        if len(ties) == 0:
            hand = self.playerInfo[winner.id]["handName"]
            await pokerCh.send(f"{winner.mention} ganhou com {hand}")
            uData.currGive(winner.id, "Chips", pot)
        else:
            kicker = self.playerInfo[winner.id]["cards"][0]
            for player in pList:
                if self.playerInfo[player.id]["cards"][0].value > kicker.value:
                    kicker = self.playerInfo[player.id]["cards"][0]
                    if winner in ties:
                        ties.remove(winner)
                    winner = player
                elif self.playerInfo[player.id]["cards"][0].value < kicker.value:
                    ties.remove(player)
            
            print(f"Ties after: {ties}")
            card = self.playerInfo[winner.id]["cards"][0]
            hand = self.playerInfo[winner.id]["handName"]
            if len(ties) > 1:
                pot = pot/len(ties)
                mentions = ""
                for player in ties:
                    uData.currGive(player.id, "Chips", pot)
                    mentions += player.mention
                await pokerCh.send(f"{mentions} ganharam com {hand} e kicker {card.name}")
            else:
                await pokerCh.send(f"{winner.mention} ganhou com {hand} e kicker {card.name}")
                uData.currGive(winner.id, "Chips", pot)



    async def evaluatePlayersHands(self, sID):
        for player in self.tables[sID]["players"]:
            pCards = self.playerInfo[player.id]["cards"]
            pCards.extend(self.tables[sID]["listCc"])
            pCards.sort(key=lambda card: card.value, reverse=True)
            cValues = {}
            cSuits = {}

            for card in pCards:
                if not card.value in cValues.keys():
                    cValues[card.value] = 1
                else:
                    cValues[card.value] += 1
                if not card.suit in cSuits.keys():
                    cSuits[card.suit] = 1
                else:
                    cSuits[card.suit] += 1
            
            valCount = {}       # Count of each card value
            for val in cValues.values():
                if not val in valCount:
                    valCount[val] = 1
                else:
                    valCount[val] += 1
            
            suitsCount = {}     # Count of each card suit
            for suit in cSuits.values():
                if not suit in suitsCount:
                    suitsCount[suit] = 1
                else:
                    suitsCount[suit] += 1

            valKeys = list(cValues.keys())
            valKeys.sort(reverse=True)
            
            flush = self.checkFlush(cSuits)
            straight, seq = self.checkStraight(valKeys)
            pair, twoPairs, threeOfValue, fourOfValue = self.check2Pair(valCount)

            if straight and flush and 14 in list(cValues.keys()):   
                self.playerInfo[player.id]["strenght"] = 9
                self.playerInfo[player.id]["handName"] = "um Royal Flush" 
            elif straight and flush:                                
                self.playerInfo[player.id]["strenght"] = 8
                self.playerInfo[player.id]["handName"] = "um Straight Flush" 
            elif fourOfValue:                                       
                self.playerInfo[player.id]["strenght"] = 7
                self.playerInfo[player.id]["handName"] = "uma Quadra" 
            elif pair and threeOfValue:                            
                self.playerInfo[player.id]["strenght"] = 6
                self.playerInfo[player.id]["handName"] = "um Fullhouse" 
            elif flush:                                             
                self.playerInfo[player.id]["strenght"] = 5
                self.playerInfo[player.id]["handName"] = "um Flush" 
            elif straight:                                          
                self.playerInfo[player.id]["strenght"] = 4
                self.playerInfo[player.id]["handName"] = "um Straight" 
            elif threeOfValue:                                      
                self.playerInfo[player.id]["strenght"] = 3
                self.playerInfo[player.id]["handName"] = "uma Trinca" 
            elif twoPairs:                                          
                self.playerInfo[player.id]["strenght"] = 2
                self.playerInfo[player.id]["handName"] = "dois Pares" 
            elif pair:                                             
                self.playerInfo[player.id]["strenght"] = 1
                self.playerInfo[player.id]["handName"] = "um Par" 
            else:                                                   
                self.playerInfo[player.id]["strenght"] = 0
                self.playerInfo[player.id]["handName"] = "uma Carta Alta" 


    def checkFlush(self, cSuits):
        if len(list(cSuits.keys())) <= 3:
            values = list(cSuits.values())
            return any(x >= 5 for x in values)
        else:
            return False
        

    def checkStraight(self, valKeys):
        if len(valKeys) >= 5:
                #possible straight
                iVals = iter(valKeys[1:])
                seq = []
                for n in valKeys[:-1]:
                    current = next(iVals)
                    if n - current == 1:
                        seq.append(n)
                        if len(seq) == 4:
                            seq.append(current)
                    else:
                        seq.clear()
                return len(seq) >= 5, seq
        else:
            return False, seq


    def check2Pair(self, valCount):
        if 4 in list(valCount.keys()):
            return False, False, False, True
        elif 2 in list(valCount.keys()) and 3 in list(valCount.keys()):
            return True, False, True, False
        elif 2 in list(valCount.keys()):
            if valCount[2] > 2:
                return False, True, False, False
            else:
                return True, False, False, False
        elif 3 in list(valCount.keys()):
            return False, False, True, False
        else:
            return False, False, False, False


    @commands.command()
    async def poker(self, ctx):
        sID = ctx.guild.id
        pokerCh = self.client.get_channel(Config.servers[str(sID)]["poker"])
        if uData.data[str(ctx.author.id)]["Chips"] > 100:
            if not sID in self.tables.keys():
                self.tables[sID] = {"players": [ctx.author], "started": False, "pot": 0, "roundBet": 0, "lastRaise": None, "turn": None, "comCards": [], "listCc": []}
                await pokerCh.send(f"{ctx.author.mention}, sua mesa foi criada! Para começar, use .pstart")
            elif not self.tables[sID]["started"]:
                if not ctx.author in self.tables[sID]["players"]:
                    self.tables[sID]["players"].append(ctx.author)
                    await pokerCh.send(f"{ctx.author.mention} entrou na mesa atual!")
        else:
            await pokerCh.send(f"{ctx.author.mention} você não tem o minimo de fichas para jogar (> 100)!")
            

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

    # Total pot message

    @commands.command()
    async def check(self, ctx):
        player = self.tables[ctx.guild.id]["turn"]
        sID = ctx.guild.id
        pokerCh = self.client.get_channel(Config.servers[str(sID)]["poker"])
        if player == ctx.author and player == self.tables[sID]["players"][0]:
            self.tables[sID]["lastRaise"] = player

    @commands.command()
    async def bet(self, ctx, amount=500):
        player = self.tables[ctx.guild.id]["turn"]
        sID = ctx.guild.id
        pokerCh = self.client.get_channel(Config.servers[str(sID)]["poker"])
        if player == ctx.author and self.tables[sID]["roundBet"] == 0:
            amount = int(amount)
            if uData.currGet(player.id, "Chips", amount):
                self.tables[ctx.guild.id]["pot"] += amount
                self.tables[ctx.guild.id]["roundBet"] = amount
                self.tables[sID]["lastRaise"] = player
                await pokerCh.send(f"{player.mention} apostou {str(amount)}!")
            else:
                await pokerCh.send(f"{player.mention} você não tem tudo isso!")
        elif self.tables[sID]["roundBet"] != 0:
            await pokerCh.send(f"{player.mention} você não pode apostar, apenas aumentar!")
    
    @commands.command(aliases=["raise"])
    async def _raise(self, ctx, amount=500):
        player = self.tables[ctx.guild.id]["turn"]
        sID = ctx.guild.id
        pokerCh = self.client.get_channel(Config.servers[str(sID)]["poker"])
        if player == ctx.author and self.tables[sID]["roundBet"] != 0:

            call = self.tables[ctx.guild.id]["roundBet"]
            amount = int(amount)
            total = amount + call

            if uData.currGet(player.id, "Chips", total):
                self.tables[ctx.guild.id]["pot"] += total
                self.tables[ctx.guild.id]["roundBet"] += amount
                self.tables[sID]["lastRaise"] = player
                await pokerCh.send(f"{player.mention} aumentou {str(amount)}, totalizando {str(total)}!")
            else:
                await pokerCh.send(f"{player.mention} você não tem tudo isso!")
        elif self.tables[sID]["roundBet"] == 0:
            await pokerCh.send(f"{player.mention} você não pode aumentar, apenas apostar!")

    @commands.command()
    async def fold(self, ctx):
        player = self.tables[ctx.guild.id]["turn"]
        sID = ctx.guild.id
        pokerCh = self.client.get_channel(Config.servers[str(sID)]["poker"])
        if player == ctx.author:
            self.tables[sID]["players"].remove(ctx.author)
            self.playerInfo.pop(ctx.author.id)
            
            await pokerCh.send(f"{player.mention} deu fold!")
    
    @commands.command()
    async def call(self, ctx):
        player = self.tables[ctx.guild.id]["turn"]
        sID = ctx.guild.id
        pokerCh = self.client.get_channel(Config.servers[str(sID)]["poker"])
        if player == ctx.author:

            amount = self.tables[ctx.guild.id]["roundBet"]

            if uData.currGet(player.id, "Chips", amount):
                self.tables[ctx.guild.id]["pot"] += amount
                await pokerCh.send(f"{player.mention} pagou {str(amount)}!")
            else:
                amount = uData.data[str(player.id)]["Chips"]
                self.tables[ctx.guild.id]["pot"] += amount

                await pokerCh.send(f"{player.mention} pagou {str(amount)} e está All-In!")



    
    #@commands.Cog.listener()
    #async def on_reaction_add(self, reaction, user):
    #    if not self.client.user == user:
    #        if reaction.message.id == self.pms[user.id]:
    #            if reaction.emoji == u"\U0001F346":
    #                # Do I really need to do this for and check for user???
    #                for server in self.tables:
    #                    if user in self.tables[server]["players"]:
    #                        playerCards = cycle(self.playerInfo[user.id]["cards"])
    #                        embed = discord.Embed(title="Suas cartas", description="Reaja para ver sua outra carta", colour=discord.Color.blue())
    #                        embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
    #                        card = next(playerCards)
    #                        embed.set_image(url=self.cUrl[str(card.value)][card.suit]) 
    #                        await reaction.message.edit(embed=embed)
    #        
    #        elif reaction.message.id == self.comMsgs[reaction.message.guild.id]:
    #            embed = discord.Embed(title="Cartas comunitárias", description="Reaja para ver as outras cartas, ou veja nos campos abaixo", colour=discord.Color.blue())
    #            embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)

    #            for c in range(len(self.tables[reaction.message.guild.id]["listCc"])):
    #                card = self.tables[reaction.message.guild.id]["listCc"][c]
    #                embed.add_field(name=f"Carta {c+1}", value=f"{card.name} de {self.cardNames[card.suit]}")

    #            card = next(self.tables[reaction.message.guild.id]["comCards"])
    #            embed.set_image(url=self.cUrl[str(card.value)][card.suit])
    #            await reaction.message.edit(embed=embed)
    #            await reaction.remove(user)


    async def waitPlayerMove(self, sID):
        pokerCh = self.client.get_channel(Config.servers[str(sID)]["poker"])
        player = self.tables[sID]["turn"]

        def isCmd(msg):
            cmds = [".check", ".bet", ".raise", ".fold", ".call"]
            for cmd in cmds:
                if msg.content.startswith(cmd) and msg.author == player:
                    if cmd == ".bet" and self.tables[sID]["roundBet"] != 0:
                        return False
                    elif cmd == ".raise" and self.tables[sID]["roundBet"] == 0:
                        return False
                    return True
            return False

        self.roundT = 30
        roundMsg = await pokerCh.send(f"{player.mention} é a sua vez! você tem {self.roundT} segundos para decidir sua jogada.")
        self.roundTimer.start(ch=pokerCh, player=player, msg=roundMsg)

        try:
            await self.client.wait_for("message", check=isCmd, timeout=30)
        except Exception as e:
            await pokerCh.send(f"{player.mention} seu tempo acabou, portanto você deu fold!")
            self.tables[sID]["players"].remove(ctx.author)
            self.playerInfo.pop(ctx.author.id)
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