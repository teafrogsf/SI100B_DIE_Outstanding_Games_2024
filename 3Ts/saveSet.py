import json
import pygame as pg
from Img import Img
from Card import Card
from Character import Character


def loadCard(cardData: dict, cardSize: tuple = (75, 75), cardPos: tuple = (0, 0)):
    """
    Get the card information from the file.
    """

    effects = [effect for effect in cardData["effects"]]
    return Card(
        ID=cardData["ID"],
        title=cardData["title"],
        description=cardData["description"],
        gate=cardData["gate"],
        type=cardData["type"] == "True",
        level=cardData["level"],
        effects=effects,
        img=Img(
            pg.image.load(cardData["imgLocation"]).convert_alpha(), cardSize, cardPos
        ),
    )


def friendSettings(location: str = "./save/friends.json", picPosition: tuple = (0, 0)):
    """
    Read player's character settings from the file.
    Return the friend units.
    """

    with open(location, "r", encoding="utf-8") as file:
        settings = json.load(file)
    friendDatas = settings["Friends"]
    friends = []
    for frData in friendDatas:
        friend = Character(
            ID=frData["ID"],
            name=frData["name"],
            HP=frData["HP"],
            SP=frData["SP"],
            SPHeal=frData["SPHeal"],
            maxHP=frData["maxHP"],
            maxSP=frData["maxSP"],
            cards=[loadCard(card) for card in frData["cards"]],
            img=Img(
                pg.image.load(frData["imgLocation"] + ".png").convert_alpha(),
                frData["imgSize"],
                picPosition,
            ),
            imgDash=Img(
                pg.image.load(frData["imgLocation"] + "-dash.png").convert_alpha(),
                frData["imgDashSize"],
                picPosition,
            ),
            imgAttackYang=Img(
                pg.image.load(
                    frData["imgLocation"] + "-attack-yang.png"
                ).convert_alpha(),
                frData["imgAttackSize"],
                picPosition,
            ),
            imgAttackYin=Img(
                pg.image.load(
                    frData["imgLocation"] + "-attack-yin.png"
                ).convert_alpha(),
                frData["imgAttackSize"],
                picPosition,
            ),
        )
        friends.append(friend)
    return friends


def readLevel(location="./save/level0.json", picPosition: tuple = (0, 0)):
    """
    Read the level settings from the file.
    Return the background image and the enemies.
    Different from the friend, the enemies have strategies.
    """

    with open(location, "r", encoding="utf-8") as file:
        settings = json.load(file)
    bgImgLocation = settings["Background"]
    yOff = settings["yOffset"]
    enemyDatas = settings["Enemies"]
    enemies = []
    for enData in enemyDatas:
        enemy = None
        posXoff = enData["posXoffset"]
        posYoff = enData["posYoffset"] + yOff
        if enData["type"] == "normal":
            picPos = (picPosition[0] + posXoff, picPosition[1] + posYoff)
            enemy = Character(
                ID=enData["ID"],
                name=enData["name"],
                HP=enData["HP"],
                maxHP=enData["maxHP"],
                maxSP=enData["maxSP"],
                SP=enData["SP"],
                SPHeal=enData["SPHeal"],
                cards=[loadCard(card) for card in enData["cards"]],
                img=Img(
                    pg.image.load(enData["imgLocation"] + ".png").convert_alpha(),
                    tuple(enData["imgSize"]),
                    picPos,
                ),
                imgDash=Img(
                    pg.image.load(enData["imgLocation"] + "-dash.png").convert_alpha(),
                    tuple(enData["imgDashSize"]),
                    picPos,
                ),
                imgAttackYang=Img(
                    pg.image.load(
                        enData["imgLocation"] + "-attack-yang.png"
                    ).convert_alpha(),
                    tuple(enData["imgAttackSize"]),
                    picPos,
                ),
                imgAttackYin=Img(
                    pg.image.load(
                        enData["imgLocation"] + "-attack-yin.png"
                    ).convert_alpha(),
                    tuple(enData["imgAttackSize"]),
                    picPos,
                ),
            )
        else:
            from battleController import gSet

            bossPos = (gSet["screenWidth"] // 2 + posXoff, picPosition[1] + posYoff)
            enemy = Character(
                ID=enData["ID"],
                name=enData["name"] + "(boss)",
                HP=enData["HP"],
                maxHP=enData["maxHP"],
                maxSP=enData["maxSP"],
                SP=enData["SP"],
                SPHeal=enData["SPHeal"],
                cards=[loadCard(card) for card in enData["cards"]],
                img=Img(
                    pg.image.load(enData["imgLocation"] + ".png").convert_alpha(),
                    tuple(enData["imgSize"]),
                    bossPos,
                ),
                imgDash=Img(
                    pg.image.load(enData["imgLocation"] + ".png").convert_alpha(),
                    tuple(enData["imgDashSize"]),
                    bossPos,
                ),
                imgAttackYang=Img(
                    pg.image.load(
                        enData["imgLocation"] + "-attack-yang.png"
                    ).convert_alpha(),
                    tuple(enData["imgAttackSize"]),
                    bossPos,
                ),
                imgAttackYin=Img(
                    pg.image.load(
                        enData["imgLocation"] + "-attack-yin.png"
                    ).convert_alpha(),
                    tuple(enData["imgAttackSize"]),
                    bossPos,
                ),
            )
        enemies.append((enemy, enData["strategy"], enData["specialStrategy"]))
    return bgImgLocation, yOff, enemies
