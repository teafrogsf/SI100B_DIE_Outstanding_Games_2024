import json
from ReceptionSystem.Page import Page
from ReceptionSystem.PageBuff import PageBuff
from ReceptionSystem.Dice import Dice
from ReceptionSystem.DiceBuff import DiceBuff
import ReceptionSystem.DiceBuff,ReceptionSystem.PageBuff
def GenerateJsonDict(page):
    dit_card = {
        "cardName":page.name,
        "mana":page.lightCost,
        "pageType":page.pageType,
        "cardImg":"testcard.png",
        "cardQuality":page.quality,
        "pageDesq":{
            "overall_desq":{
                "condition":"Use",#"Use","Start","None"
                "effect":"Light",#"Light","Page",    "GetBuffs","ExertBuffs"
                "count":1
                #"buffs":["Burn","Bleed"]
                #"counts":[3,2]
                #"isNext":
            },
            "list":[]
        }
    }
    st=page.pageBuff.__class__.__name__
    dit_card["pageDesq"]["overall_desq"]["condition"]="Special"
    dit_card["pageDesq"]["overall_desq"]["effect"]=st
    dit_card["pageDesq"]["overall_desq"]["para"]=page.pageBuff.para
    for dice in page.dices:
        dit_dice={
            "diceType":dice.attackType,
            "minDice":dice.dicePointL,
            "maxDice":dice.dicePointR,
            "isCounter":False,
            "desq":{
                "condition":"Special",#"Hit","Win","Lose","None"
                "effect":"Light",#"Light","Page","Damage","StaggerDamage","Recover","RecoverStagger",    "GetBuffs","ExertBuffs"
                "count":1
                #"buffs":["Burn","Bleed"]
                #"counts":[3,2]
                #"para":[]
            }
        }
        dit_dice["desq"]["effect"]=dice.diceBuff.__class__.__name__
        dit_dice["desq"]["para"]=dice.diceBuff.para
        dit_card["pageDesq"]["list"].append(dit_dice)
    for dice in page.counterDices:
        dit_dice={
            "diceType":dice.attackType,
            "minDice":dice.dicePointL,
            "maxDice":dice.dicePointR,
            "isCounter":True,
            "desq":{
                "condition":"None"
            }
        }
        dit_card["pageDesq"]["list"].append(dit_dice)
    return dit_card
    with open(page.name+'.json', 'w') as f:
        json.dump(dit_card, f)

def ReadCardJson(name):
    #print(name)
    with open(name, 'r',encoding="utf-8") as f:
        dits = json.load(f)
    lis = []
    for dit in dits.values():
        lis.append(ReadCardDict(name,dit))
    return lis
def ReadCardDict(file,dit):
    cdit={"green":"Green","blue":"Blue","purple":"Purple","gold":"Gold",
          "Green":"Green","Blue":"Blue","Purple":"Purple","Gold":"Gold"}
    if not "pageType" in dit.keys():
        dit["pageType"] = "Melee"
    page=Page(dit["cardName"],dit["pageType"],[],dit["mana"],None,0,cdit[dit["cardQuality"]])
    if dit["pageDesq"]["overall_desq"]["condition"]=="None":
        page.AddPageBuff(PageBuff())
    elif dit["pageDesq"]["overall_desq"]["condition"]=="Special":
        st=dit["pageDesq"]["overall_desq"]["effect"]
        if hasattr(ReceptionSystem.PageBuff,st):
            cls=getattr(ReceptionSystem.PageBuff,st)
            page.AddPageBuff(cls(*dit["pageDesq"]["overall_desq"]["para"]))
        else:
            print("Unknown PageBuff:",st, "in",dit["cardName"]," ",file)
    else:
        cd=dit["pageDesq"]["overall_desq"]["condition"]
        st=dit["pageDesq"]["overall_desq"]["effect"]
        if hasattr(ReceptionSystem.PageBuff,cd+st):
            cls=getattr(ReceptionSystem.PageBuff,cd+st)
            if st=="GetBuffs" or st=="ExertBuffs":
                page.AddPageBuff(cls(dit["pageDesq"]["overall_desq"]["buffs"],dit["pageDesq"]["overall_desq"]["counts"],dit["pageDesq"]["overall_desq"]["isNext"]))
            else:
                page.AddPageBuff(cls(dit["pageDesq"]["overall_desq"]["count"]))
        else:
            print("Unknown PageBuff:",cd+st, "in",dit["cardName"]," ",file)    
        
    atdt={"Slash":"Attack","Pierce":"Attack","Blunt":"Attack","Block":"Block","Evade":"Evade"}
    for dic in dit["pageDesq"]["list"]:
        dice=Dice(dic["minDice"],dic["maxDice"],atdt[dic["diceType"]],dic["diceType"],None,None,dic["isCounter"])
        if dic["desq"]["condition"]=="None":
            dice.AddDiceBuff(DiceBuff())
        elif dic["desq"]["condition"]=="Special":
            st=dic["desq"]["effect"]
            if hasattr(ReceptionSystem.DiceBuff,st):
                cls=getattr(ReceptionSystem.DiceBuff,st)
                dice.AddDiceBuff(cls(*dic["desq"]["para"]))
            else:
                print("Unknown DiceBuff:",st, "in",dit["cardName"]," ",file)
        else:
            cd=dic["desq"]["condition"]
            st=dic["desq"]["effect"]
            if hasattr(ReceptionSystem.DiceBuff,cd+st):
                cls=getattr(ReceptionSystem.DiceBuff,cd+st)
                if st=="GetBuffs" or st=="ExertBuffs":
                    dice.AddDiceBuff(cls(dic["desq"]["buffs"],dic["desq"]["counts"],dic["desq"]["isNext"]))
                else:
                    dice.AddDiceBuff(cls(dic["desq"]["count"]))
            else:
                print("Unknown DiceBuff:",cd+st, "in",dit["cardName"]," ",file)
        if dic["isCounter"]:
            page.AddCounterDice(dice)
        else:
            page.AddDice(dice)
    return page