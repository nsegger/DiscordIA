from itertools import cycle

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
        else:
            self.value = int(self.value)


def main():
    pCards = ["AH", "QH"]
    table = ["AH", "JH", "10H", "3D", "5C"]
    pCards.extend(table)
    pCards = [Card(cStr) for cStr in pCards]

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


    
    valCount = {}
    for val in cValues.keys():
        if not val in valCount:
            valCount[val] = 1
        else:
            valCount[val] += 1

    suitsCount = {}
    for suit in cSuits.values():
        if not suit in suitsCount:
            suitsCount[suit] = 1
        else:
            suitsCount[suit] += 1

    valCount = list(valCount.keys())
    valCount.sort(reverse=True)
    #print(valCount)
   

    flush = checkFlush(cSuits)
    straight = checkStraight(valCount)
    if straight and flush:
        print("Straight flush")
    elif straight:
        print("Straight")
    else:
        print("Flush")


def checkFlush(cSuits):
    if len(list(cSuits.keys())) <= 3:
        values = list(cSuits.values())
        return any(x >= 5 for x in values)
    else:
        return False
        
def checkStraight(valCount):
    if len(valCount) >= 5:
            #possible straight
            iVals = iter(valCount[1:])
            print(valCount[1:])
            print(valCount)
            seq = []
            for n in valCount[:-1]:
                current = next(iVals)
                if n - current == 1:
                    seq.append(n)
                    if len(seq) == 4:
                        seq.append(current)
            print(seq)
            return len(seq) >= 5

if __name__ == "__main__":
    main()