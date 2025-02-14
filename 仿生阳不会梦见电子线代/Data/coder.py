def decodeDiceIdInfo(dice):
    #team,charId
    return ((dice//100000)%10,(dice//1000)%1000,dice)

def encodeDiceIdInfo(team,charId,diceIndex):
    return team*10000+charId*100+diceIndex

def decodeCharIdInfo(char):
    return char//100