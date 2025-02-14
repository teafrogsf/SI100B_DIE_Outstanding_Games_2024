import sys
from Img import Img
from Character import Character, copyCharacter
from Animation import Sleep, moveAnimation, fadeAnimation
from mouseSelect import mouseLeftButton, mouseMove
import pygame as pg
import screenPainter as scpt
from Clash import Done, clashState1, clashState2, clashState3, clashState4, clashState5

gSet = sys.modules["__main__"].__dict__


def mainInit():
    """
    Initialize the important datas
    - gSet['screen']
        - sizes
        - window
        - FPS
        - title
    - Sizes
        - button
            - turn end
            - draw & undo
        - card
        - character
    - colors
        - font color
        - HP
        - SP
        - card border
    - fonts
    """

    # screen
    gSet["screenWidth"] = 1000
    gSet["screenHeight"] = 650
    gSet["screenSize"] = gSet["screenWidth"], gSet["screenHeight"]
    gSet["fps"] = 60
    gSet["screen"] = pg.display.set_mode(gSet["screenSize"])

    # button sizes
    gSet["endTurnButtonWidth"] = 75
    gSet["endTurnButtonHeight"] = 75
    gSet["endTurnButtonSize"] = gSet["endTurnButtonWidth"], gSet["endTurnButtonHeight"]
    gSet["draw&undoButtonWidth"] = 180
    gSet["draw&undoButtonHeight"] = 75
    gSet["draw&undoButtonSize"] = (
        gSet["draw&undoButtonWidth"],
        gSet["draw&undoButtonHeight"],
    )
    gSet["cardWidth"] = 75
    gSet["cardHeight"] = 75
    gSet["cardSize"] = gSet["cardWidth"], gSet["cardHeight"]

    # character sizes
    gSet["unitWidth"] = 40
    gSet["unitHeight"] = 80
    gSet["unitSize"] = gSet["unitWidth"], gSet["unitHeight"]

    # colors
    def rgb(r: int, g: int, b: int):
        return r, g, b

    gSet["--font-color-light"] = rgb(242, 253, 255)
    gSet["--font-color-yellow"] = rgb(255, 250, 205)
    gSet["--font-color-grey"] = rgb(180, 180, 180)
    gSet["--HP-ground"] = rgb(0, 99, 29)
    gSet["--HP-front"] = rgb(0, 205, 102)
    gSet["--HP-third"] = rgb(192, 255, 62)
    gSet["--SP-ground"] = rgb(25, 25, 112)
    gSet["--SP-front"] = rgb(65, 105, 225)
    gSet["--SP-third"] = rgb(120, 169, 255)
    gSet["--Enemy-number-ground"] = rgb(72, 61, 139)
    gSet["--Enemy-number-front"] = rgb(132, 112, 255)
    gSet["--select-card"] = rgb(252, 243, 207)
    gSet["--selected-card"] = rgb(245, 183, 177)
    gSet["--card-info-ground"] = rgb(31, 30, 51)

    # fonts
    gSet["font-battleInfo"] = pg.font.Font("./assets/font/NotoSansCJKsc-Bold.otf", 20)
    gSet["font-cardDetail"] = pg.font.Font("./assets/font/STKAITI.TTF", 24)
    gSet["font-clashInfo-card"] = pg.font.Font(
        "./assets/font/SourceHanSansSC-Regular-2.otf", 18
    )
    gSet["font-clashInfo-number"] = pg.font.Font("./assets/font/Exo-SemiBold.ttf", 32)
    gSet["font-bossName"] = pg.font.Font(
        "./assets/font/SourceHanSerifCN-Regular-1.otf", 80
    )

    # others
    gSet["cardSpace"] = 0
    gSet["friendClashInfo"] = None
    gSet["enemyClashInfo"] = None


def pictureInit():
    """
    Initialize the pictures:
    - Button
        - turn end
        - draw
        - undo
    """

    gSet["turnButton"] = Img(
        img=pg.image.load("./assets/img/turn_end.png").convert_alpha(),
        size=gSet["endTurnButtonSize"],
        pos=(gSet["screenWidth"] // 2 - gSet["endTurnButtonWidth"] // 2, 10),
    )
    gSet["drawButton"] = Img(
        img=pg.image.load("./assets/img/draw_button.png").convert_alpha(),
        size=gSet["draw&undoButtonSize"],
        pos=(
            gSet["screenWidth"] // 2 - gSet["draw&undoButtonWidth"] // 2 - 90,
            gSet["screenHeight"] - gSet["draw&undoButtonHeight"] - 10,
        ),
    )
    gSet["undoButton"] = Img(
        img=pg.image.load("./assets/img/undo_button.png").convert_alpha(),
        size=gSet["draw&undoButtonSize"],
        pos=(
            gSet["screenWidth"] // 2 - gSet["draw&undoButtonWidth"] // 2 + 90,
            gSet["screenHeight"] - gSet["draw&undoButtonHeight"] - 10,
        ),
    )


def friendInit(friendID: str):
    """
    Initialize friend data
    """

    from saveSet import friendSettings

    Friends = friendSettings(
        location="./save/friends.json",
        picPosition=(gSet["screenWidth"] // 5, gSet["screenHeight"] // 7 * 5),
    )

    gSet["friendUnit"] = Friends[0]
    for friend in Friends:
        if len(friend.onHandCards) > 4:  # At most 4 cards on hand at the beginning
            import random

            onHd = random.sample(friend.onHandCards, 4)
            for card in friend.cards:
                if card not in onHd:
                    friend.unusedCards.append(card)
            friend.onHandCards = onHd
        if friend.ID == friendID:
            friend.img.setPos((friend.img.x, friend.img.y - friend.img.height))
            friend.imgDash.setPos(friend.img.pos)
            friend.imgAttackYang.setPos(friend.img.pos)
            friend.imgAttackYin.setPos(friend.img.pos)
            gSet["friendUnit"] = friend
            break


def reloadEnemyCards(enemyUnit: Character, strategies: list, specials: list):
    cards = []
    useNormal = True
    for special in specials:
        if special in gSet["enemyUseSpecial"]:
            useNormal = False
            gSet["enemyUseSpecial"].remove(special)
            if special == "counterAttack":
                for card in enemyUnit.cards:
                    if card.ID in gSet["enemySpecialStrategy"]["counterAttack"]:
                        cards.append(card)
                enemyUnit.directLoad(cards=cards)
    if useNormal:
        import random

        strategy = random.choice(strategies)
        for card in enemyUnit.cards:
            if card.ID in strategy:
                cards.append(card)
        random.shuffle(cards)
        enemyUnit.directLoad(cards=cards)


def loadLevel(level: int):
    """
    Load level file. Get enemy data and BG
    """

    from saveSet import readLevel

    bgImgLocation, yOff, Enemies = readLevel(
        location=f"./save/level{level}.json",
        picPosition=(gSet["screenWidth"] // 5 * 4, gSet["screenHeight"] // 7 * 5),
    )

    gSet["background"] = Img(
        img=pg.image.load(bgImgLocation), size=gSet["screenSize"], pos=(0, 0)
    )
    gSet["enemyUnits"] = []
    for enemy in Enemies:
        if "(boss)" in enemy[0].name:
            enemy[0].img.setPos((enemy[0].img.x, enemy[0].img.y - enemy[0].img.height))
        else:
            enemy[0].img.setPos(
                (
                    enemy[0].img.x - enemy[0].img.width,
                    enemy[0].img.y - enemy[0].img.height,
                )
            )
        enemy[0].imgDash.setPos(enemy[0].img.pos)
        enemy[0].imgAttackYang.setPos(enemy[0].img.pos)
        enemy[0].imgAttackYin.setPos(enemy[0].img.pos)
        gSet["enemyUnits"].append(enemy)

    # fix the position of friend unit
    gSet["friendUnit"].img.setPos(
        (gSet["friendUnit"].img.x, gSet["friendUnit"].img.y + yOff)
    )
    gSet["friendUnit"].imgDash.setPos(gSet["friendUnit"].img.pos)
    gSet["friendUnit"].imgAttackYang.setPos(gSet["friendUnit"].img.pos)
    gSet["friendUnit"].imgAttackYin.setPos(gSet["friendUnit"].img.pos)

    gSet["enemyUnit"] = Enemies[0][0]
    gSet["enemyStrategy"] = Enemies[0][1]
    gSet["enemySpecialStrategy"] = Enemies[0][2]
    gSet["enemyUnitID"] = 0
    gSet["enemyUseSpecial"] = []
    reloadEnemyCards(
        enemyUnit=gSet["enemyUnit"],
        strategies=gSet["enemyStrategy"],
        specials=gSet["enemySpecialStrategy"],
    )


recordedTurnState = None


def recordTurnState(friendUnit: Character, enemyUnit: Character):
    """
    Record the state when a turn start.
    """

    import copy

    global recordedTurnState
    recordedTurnState = copy.deepcopy([friendUnit, enemyUnit])


def undoTurn():
    """
    When the player uses Undo, roll the recorded state back.
    """

    global recordedTurnState
    return copyCharacter(recordedTurnState[0]), copyCharacter(recordedTurnState[1])


def endTurn(friendUnit: Character, enemyUnit: Character):
    """
    Deal with the things when a turn end despite clash.
    Mainly to clear the state
    """

    # Clear the attack time
    from mouseSelect import attackClear

    attackClear()

    # Clear the cards that are used or cancelled this turn
    friendUnit.SP -= friendUnit.SPlossThisTurn()
    enemyUnit.SP -= enemyUnit.SPlossThisTurn()
    friendUnit.useThisTurn.clear()
    enemyUnit.useThisTurn.clear()
    friendUnit.getThisTurn.clear()
    enemyUnit.getThisTurn.clear()
    friendUnit.lostThisTurn.clear()
    enemyUnit.lostThisTurn.clear()

    # Heal SP
    friendUnit.SP += friendUnit.SPHeal
    if friendUnit.SP > friendUnit.maxSP:
        friendUnit.SP = friendUnit.maxSP


def cardInfoDeal(friendUnit: Character, enemyUnit: Character):
    from mouseSelect import data

    selectedCards = data("selectedCards")
    hoveredCards = data("hoveredCards")
    hoveredCardPos = data("hoveredCardPos")
    selectedFriendCard = data("selectedFriendCard")

    scpt.drawCardBorders(
        friendUnit=friendUnit,
        enemyUnit=enemyUnit,
        selectedCards=selectedCards,
        hoveredCards=hoveredCards,
    )
    if hoveredCards is not None:
        cardFrom = True if hoveredCardPos[0] < gSet["screenWidth"] // 2 else False
        scpt.drawCardDetail(card=hoveredCards, cardFrom=cardFrom)
        if not cardFrom and selectedFriendCard is not None:
            scpt.drawCardDetail(card=selectedFriendCard, cardFrom=True)
    elif selectedFriendCard is not None:
        scpt.drawCardDetail(card=selectedFriendCard, cardFrom=True)


Animations = []


def main(Level: int = 0, FriendID: str = "fr1"):
    pg.init()
    mainInit()

    pictureInit()
    friendInit(friendID=FriendID)
    loadLevel(level=Level)
    FriendUnit = copyCharacter(gSet["friendUnit"])
    EnemyUnit = copyCharacter(gSet["enemyUnit"])

    bossEntrance = False

    global Animations
    if "(boss)" in EnemyUnit.name:
        bossName = EnemyUnit.name.removesuffix("(boss)")
        bossEntranceSurface = pg.Surface((gSet["screenWidth"], gSet["screenHeight"]))
        bossEntranceSurface.fill((255, 255, 255))
        bossNameText = gSet["font-bossName"].render(bossName, True, (0, 0, 0))
        textRect = bossNameText.get_rect(
            center=(gSet["screenWidth"] // 2, gSet["screenHeight"] // 2)
        )
        bossEntranceSurface.blit(bossNameText, textRect.topleft)
        bossEntrance = True
        gSet["bossEntrance"] = Img(
            img=bossEntranceSurface,
            size=(gSet["screenWidth"], gSet["screenHeight"]),
            pos=(0, 0),
            alpha=255,
        )
        Animations.append(
            fadeAnimation(
                object=gSet["bossEntrance"],
                animateSeconds=0.1,
                nowAlpha=0,
                endAlpha=255,
                name="bossEntranceFadeIn",
            )
        )
    else:
        Animations.append(
            moveAnimation(
                object=FriendUnit.imgDash,
                animateSeconds=0.3,
                nowPos=(-FriendUnit.img.width, FriendUnit.img.y),
                endPos=(
                    FriendUnit.img.x
                    + (FriendUnit.img.width - FriendUnit.imgDash.width),
                    FriendUnit.img.y,
                ),
                name="FriendUnitIn",
            )
        )
        Animations.append(
            moveAnimation(
                object=EnemyUnit.imgDash,
                animateSeconds=0.3,
                nowPos=(gSet["screenWidth"], EnemyUnit.img.y),
                endPos=EnemyUnit.img.pos,
                name="EnemyUnitIn",
            )
        )

    recordTurnState(FriendUnit, EnemyUnit)
    clock = pg.time.Clock()
    clock.tick(gSet["fps"])

    if "(boss)" not in EnemyUnit.name:
        FriendUnit.showImg = FriendUnit.imgDash
        EnemyUnit.showImg = EnemyUnit.imgDash

    inClash = False
    clashDoneThisFrame = False

    while True:
        for animation in Animations:
            if animation.update():
                Animations.remove(animation)
                # Battle Start
                if animation.name == "FriendUnitIn":
                    FriendUnit.showImg = FriendUnit.img
                elif animation.name == "EnemyUnitIn":
                    EnemyUnit.showImg = EnemyUnit.img

                # Clash
                elif animation.name == "FriendClash1":
                    FriendUnit.showImg = FriendUnit.img
                    if Done():
                        clashState2(
                            Animations=Animations,
                            friendUnit=FriendUnit,
                            enemyUnit=EnemyUnit,
                        )
                elif animation.name == "EnemyClash1":
                    EnemyUnit.showImg = EnemyUnit.img
                    if Done():
                        clashState2(
                            Animations=Animations,
                            friendUnit=FriendUnit,
                            enemyUnit=EnemyUnit,
                        )
                elif animation.name == "friendClash2InfoFadeIn":
                    if Done():
                        Animations.append(Sleep(seconds=0.5, name="Clash2"))
                elif animation.name == "enemyClash2InfoFadeIn":
                    if Done():
                        Animations.append(Sleep(seconds=0.5, name="Clash2"))
                elif animation.name == "Clash2":
                    gSet["friendClashInfo"] = None
                    gSet["enemyClashInfo"] = None
                    clashState3(
                        Animations=Animations,
                        friendUnit=FriendUnit,
                        enemyUnit=EnemyUnit,
                    )
                elif animation.name == "Clash3":
                    clashState4(
                        Animations=Animations,
                        friendUnit=FriendUnit,
                        enemyUnit=EnemyUnit,
                    )
                elif animation.name == "friendClash4InfoFadeIn":
                    if Done():
                        Animations.append(Sleep(seconds=0.5, name="Clash4"))
                elif animation.name == "enemyClash4InfoFadeIn":
                    if Done():
                        Animations.append(Sleep(seconds=0.5, name="Clash4"))
                elif animation.name == "Clash4":
                    gSet["friendClashInfo"] = None
                    gSet["enemyClashInfo"] = None
                    clashState5(
                        Animations=Animations,
                        friendUnit=FriendUnit,
                        enemyUnit=EnemyUnit,
                    )
                elif animation.name == "FriendClash5":
                    FriendUnit.showImg = FriendUnit.img
                    if Done():
                        clashDoneThisFrame = True
                elif animation.name == "EnemyClash5":
                    EnemyUnit.showImg = EnemyUnit.img
                    if Done():
                        clashDoneThisFrame = True
                elif animation.name == "deadEnemyUnitOut":
                    if gSet["enemyUnitID"] == len(gSet["enemyUnits"]):
                        print("You defeated the enemy.")
                        return "Win"
                    else:
                        gSet["enemyUnit"] = gSet["enemyUnits"][gSet["enemyUnitID"]][0]
                        gSet["enemyStrategy"] = gSet["enemyUnits"][gSet["enemyUnitID"]][
                            1
                        ]
                        gSet["enemySpecialStrategy"] = gSet["enemyUnits"][
                            gSet["enemyUnitID"]
                        ][2]
                        gSet["enemyUseSpecial"] = []
                        reloadEnemyCards(
                            enemyUnit=gSet["enemyUnit"],
                            strategies=gSet["enemyStrategy"],
                            specials=gSet["enemySpecialStrategy"],
                        )
                        EnemyUnit = gSet["enemyUnit"]
                        EnemyUnit.showImg = EnemyUnit.imgDash
                        Animations.append(
                            moveAnimation(
                                object=EnemyUnit.imgDash,
                                animateSeconds=0.3,
                                nowPos=(gSet["screenWidth"], EnemyUnit.img.y),
                                endPos=EnemyUnit.img.pos,
                                name="newEnemyUnitIn",
                            )
                        )
                elif animation.name == "newEnemyUnitIn":
                    EnemyUnit.showImg = EnemyUnit.img
                    recordTurnState(FriendUnit, EnemyUnit)
                elif animation.name == "bossEntranceFadeIn":
                    Animations.append(Sleep(seconds=2.0, name="bossEntranceSleep"))
                elif animation.name == "bossEntranceSleep":
                    Animations.append(
                        fadeAnimation(
                            object=gSet["bossEntrance"],
                            animateSeconds=1,
                            nowAlpha=255,
                            endAlpha=0,
                            name="bossEntranceFadeOut",
                        )
                    )
                elif animation.name == "bossEntranceFadeOut":
                    bossEntrance = False

        if clashDoneThisFrame:
            inClash = False
            clashDoneThisFrame = False
            FriendUnit.HP -= FriendUnit.HPlossThisTurn
            FriendUnit.HPlossThisTurn = 0
            if FriendUnit.HP < 0:
                FriendUnit.HP = 0
            EnemyUnit.HP -= EnemyUnit.HPlossThisTurn
            EnemyUnit.HPlossThisTurn = 0
            if EnemyUnit.HP < 0:
                EnemyUnit.HP = 0
            for card in EnemyUnit.onHandCards:
                for effect in card.effects:
                    if "HPheal" in effect:
                        eff = effect.split("_")
                        val = int(eff[eff.index("HPheal") + 1])
                        EnemyUnit.HP = min(EnemyUnit.HP + val, EnemyUnit.maxHP)
            if FriendUnit.HP == 0:
                print("You are defeated.")
                return "Lose"
            elif EnemyUnit.HP == 0:
                gSet["enemyUnitID"] += 1
                if "(boss)" in EnemyUnit.name:
                    Animations.append(
                        fadeAnimation(
                            object=EnemyUnit.img,
                            animateSeconds=0.5,
                            nowAlpha=255,
                            endAlpha=0,
                            name="deadEnemyUnitOut",
                        )
                    )
                else:
                    Animations.append(
                        moveAnimation(
                            object=EnemyUnit.img,
                            animateSeconds=0.3,
                            nowPos=EnemyUnit.img.pos,
                            endPos=(gSet["screenWidth"] + 10, EnemyUnit.img.y),
                            name="deadEnemyUnitOut",
                        )
                    )
            else:
                reloadEnemyCards(
                    enemyUnit=EnemyUnit,
                    strategies=gSet["enemyStrategy"],
                    specials=gSet["enemySpecialStrategy"],
                )
                recordTurnState(FriendUnit, EnemyUnit)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif (event.type == pg.KEYDOWN) and (event.key == pg.K_ESCAPE):
                return "Lose"
            elif not inClash:
                if event.type == pg.MOUSEMOTION:
                    mouseMove(event=event, friendUnit=FriendUnit, enemyUnit=EnemyUnit)
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        button = mouseLeftButton(
                            event=event, friendUnit=FriendUnit, enemyUnit=EnemyUnit
                        )
                        if button == "":
                            pass
                        elif button == "End":
                            endTurn(friendUnit=FriendUnit, enemyUnit=EnemyUnit)
                            inClash = True
                            clashState1(
                                Animations=Animations,
                                friendUnit=FriendUnit,
                                enemyUnit=EnemyUnit,
                            )
                        elif button == "Draw":
                            FriendUnit.getCard()
                        elif button == "Undo":
                            FriendUnit, EnemyUnit = undoTurn()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        endTurn(friendUnit=FriendUnit, enemyUnit=EnemyUnit)
                        inClash = True
                        clashState1(
                            Animations=Animations,
                            friendUnit=FriendUnit,
                            enemyUnit=EnemyUnit,
                        )

        gSet["screen"].blit(gSet["background"].img, gSet["background"].pos)
        scpt.drawBattleInfo(
            friendUnit=FriendUnit,
            enemyUnit=EnemyUnit,
            enemyID=gSet["enemyUnitID"],
            enemyNumber=len(gSet["enemyUnits"]),
        )
        scpt.drawUnits(friend=FriendUnit.showImg, enemy=EnemyUnit.showImg)
        scpt.drawCards(friendUnit=FriendUnit, enemyUnit=EnemyUnit)
        cardInfoDeal(friendUnit=FriendUnit, enemyUnit=EnemyUnit)
        if inClash:
            if gSet["friendClashInfo"] is not None:
                gSet["screen"].blit(
                    gSet["friendClashInfo"].img, gSet["friendClashInfo"].pos
                )
            if gSet["enemyClashInfo"] is not None:
                gSet["screen"].blit(
                    gSet["enemyClashInfo"].img, gSet["enemyClashInfo"].pos
                )
        if bossEntrance:
            gSet["screen"].blit(gSet["bossEntrance"].img, gSet["bossEntrance"].pos)

        pg.display.flip()
        clock.tick(gSet["fps"])


if __name__ == "__main__":
    main(Level=2, FriendID="fr1")
