# So we can test the hand evaluation process :))


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

class Player:
    def __init__(self, string):
        self.id = string
        if string == "1":
            self.mention = "IamN5"
        else:
            self.mention = "CarlosFunk"


def main():
    sID = "server"
    tables = {}
    tables[sID] = {}
    tables[sID]["players"] = [Player("1"), Player("2")]
    playerInfo = {}
    playerInfo["1"] = {}
    playerInfo["1"]["cards"] = [Card("QD"), Card("8S")]
    playerInfo["2"] = {}
    playerInfo["2"]["cards"] = [Card("QH"), Card("8H")]
    tables[sID]["listCc"] = [Card("6H"), Card("7C"), Card("3D"), Card("4C"), Card("2D")]

    p1 = tables[sID]["players"][0]
    p2 = tables[sID]["players"][1]
    print(f"Player 1: {p1}\nPlayer 2: {p2}")

    evaluatePlayersHands(sID, tables, playerInfo)

    ties = []
    winner = tables[sID]["players"][0]
    ties.append(winner)
    strongestHand = playerInfo[winner.id]["strenght"]
    pList = tables[sID]["players"][1:]
    for player in pList:
        force = playerInfo[player.id]["strenght"]
        print(f"força {force} vs mais forte = {strongestHand}")
        if playerInfo[player.id]["strenght"] > strongestHand:
            print("maior")
            winner = player
            strongestHand = playerInfo[winner.id]["strenght"]
        elif playerInfo[player.id]["strenght"] == strongestHand:
            print("igual")
            ties.append(player)
    
    print(f"Ties before: {ties}")
    if len(ties) == 0:
        hand = playerInfo[winner.id]["handName"]
        print(f"{winner.mention} ganhou com {hand}")
    else:
        kicker = playerInfo[winner.id]["cards"][0]
        for player in pList:
            if playerInfo[player.id]["cards"][0].value > kicker.value:
                kicker = playerInfo[player.id]["cards"][0]
                if winner in ties:
                    ties.remove(winner)
                winner = player
            elif playerInfo[player.id]["cards"][0].value < kicker.value:
                ties.remove(player)
        
        print(f"Ties after: {ties}")
        card = playerInfo[winner.id]["cards"][0]
        hand = playerInfo[winner.id]["handName"]
        if len(ties) > 1:
            mentions = ""
            for player in ties:
                mentions += player.mention
            print(f"{mentions} ganharam com {hand} e kicker {card.name}")
        else:
            print(f"{winner.mention} ganhou com {hand} e kicker {card.name}")



def evaluatePlayersHands(sID, tables, playerInfo):
    for player in tables[sID]["players"]:
        pCards = playerInfo[player.id]["cards"]
        pCards.extend(tables[sID]["listCc"])
        pCards.sort(key=lambda card: card.value, reverse=True)
        cValues = {}
        cSuits = {}
    
    # Keep only the values so we can untie the game
    #playerInfo[player.id]["cards"] = [c.value for c in pCards]

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

        flush = checkFlush(cSuits)
        straight, seq = checkStraight(valKeys)
        pair, twoPairs, threeOfValue, fourOfValue = check2Pair(valCount)

        if straight and flush and 14 in list(cValues.keys()):   
                playerInfo[player.id]["strenght"] = 9
                playerInfo[player.id]["handName"] = "um Royal Flush" 
        elif straight and flush:                                
            playerInfo[player.id]["strenght"] = 8
            playerInfo[player.id]["handName"] = "um Straight Flush" 
        elif fourOfValue:                                       
            playerInfo[player.id]["strenght"] = 7
            playerInfo[player.id]["handName"] = "uma Quadra" 
        elif pair and threeOfValue:                            
            playerInfo[player.id]["strenght"] = 6
            playerInfo[player.id]["handName"] = "um Fullhouse" 
        elif flush:                                             
            playerInfo[player.id]["strenght"] = 5
            playerInfo[player.id]["handName"] = "um Flush" 
        elif straight:                                          
            playerInfo[player.id]["strenght"] = 4
            playerInfo[player.id]["handName"] = "um Straight" 
        elif threeOfValue:                                      
            playerInfo[player.id]["strenght"] = 3
            playerInfo[player.id]["handName"] = "uma Trinca" 
        elif twoPairs:                                          
            playerInfo[player.id]["strenght"] = 2
            playerInfo[player.id]["handName"] = "dois Pares" 
        elif pair:                                             
            playerInfo[player.id]["strenght"] = 1
            playerInfo[player.id]["handName"] = "um Par" 
        else:                                         
            playerInfo[player.id]["strenght"] = 0
            playerInfo[player.id]["handName"] = "uma Carta Alta" 
        force = playerInfo[player.id]["strenght"]
        print(f"Setei força {force} na mão do {player.id}\n")


def checkFlush(cSuits):
 if len(list(cSuits.keys())) <= 3:
     values = list(cSuits.values())
     return any(x >= 5 for x in values)
 else:
     return False
    
def checkStraight(valKeys):
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

def check2Pair(valCount):
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


if __name__ == "__main__":
    main()