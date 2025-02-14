from Character import Character
from Img import Img
from Animation import Sleep, moveAnimation, fadeAnimation
import pygame as pg

done = 0  # number of done units


def Done():
    """
    One unit is done
    If all units are done, return True
    """

    global done

    done += 1
    if done == 2:
        return True
    return False


friendOriginPos = None
enemyOriginPos = None


def cardInfoSurface(unit: Character, type: bool, color: tuple):
    """
    Create a surface displaying the card information for the given unit.
    """

    from battleController import gSet

    width, height = 200, 0

    total = sum(
        card.level
        for card in unit.onHandCards
        if (card.type == type and "defence" not in card.effects)
    )
    textTotal = gSet["font-clashInfo-number"].render(f"Total: {total}", True, color)

    defence = sum(
        card.level
        for card in unit.onHandCards
        if (card.type == type and "defence" in card.effects)
    )
    textDefenceContent = ""
    if defence > 0:
        textDefenceContent = f" +({defence})"
    textDefence = gSet["font-clashInfo-number"].render(
        textDefenceContent, True, gSet["--font-color-light"]
    )

    width = max(width, textTotal.get_width() + textDefence.get_width())
    height = textTotal.get_height() + 5

    textCards = []
    for card in unit.onHandCards:
        if card.type == type and "defence" not in card.effects:
            text = gSet["font-clashInfo-card"].render(
                f"{card.title}: {card.level}", True, gSet["--font-color-light"]
            )
            textCards.append(text)
            width = max(width, text.get_width())
            height += text.get_height()
        elif card.type == type:
            text = gSet["font-clashInfo-card"].render(
                f"{card.title}: {card.level} (防御)", True, gSet["--font-color-light"]
            )
            textCards.append(text)
            width = max(width, text.get_width())
            height += text.get_height()

    width += 20
    height += 20
    surface = pg.Surface((width, height), pg.SRCALPHA)
    surface.fill((0, 0, 0, 0))
    bgColor = gSet["--card-info-ground"]
    bgColor = (*bgColor, int(0.7 * 255))
    pg.draw.rect(surface, bgColor, (0, 0, width, height))

    surface.blit(textTotal, (10, 10))
    surface.blit(textDefence, (10 + textTotal.get_width(), 10))
    yOffset = textTotal.get_height() + 5
    for text in textCards:
        surface.blit(text, (10, yOffset))
        yOffset += text.get_height()

    return surface


def clashState1(Animations: list, friendUnit: Character, enemyUnit: Character):
    """
    The characters moved to the x-center of the screen, ready to clash
    """

    global done, friendOriginPos, enemyOriginPos
    from battleController import gSet

    done = 0
    endPosFriend = (
        gSet["screenWidth"] // 2 - friendUnit.imgAttackYang.width + 25,
        friendUnit.img.y,
    )
    endPosEnemy = (gSet["screenWidth"] // 2 - 25, enemyUnit.img.y)
    if "(boss)" in enemyUnit.name:
        endPosEnemy = enemyUnit.img.pos
    friendOriginPos = friendUnit.img.pos
    enemyOriginPos = enemyUnit.img.pos
    friendUnit.showImg = friendUnit.imgDash
    enemyUnit.showImg = enemyUnit.imgDash
    if "(boss)" in enemyUnit.name:
        enemyUnit.showImg = enemyUnit.img
    Animations.append(
        moveAnimation(
            object=friendUnit.imgDash,
            animateSeconds=0.5,
            nowPos=friendUnit.img.pos,
            endPos=endPosFriend,
            name="FriendClash1",
        )
    )
    if "(boss)" in enemyUnit.name:
        Animations.append(
            moveAnimation(
                object=enemyUnit.imgDash,
                animateSeconds=0.5,
                nowPos=enemyUnit.img.pos,
                endPos=enemyUnit.img.pos,
                name="EnemyClash1",
            )
        )
    else:
        Animations.append(
            moveAnimation(
                object=enemyUnit.imgDash,
                animateSeconds=0.5,
                nowPos=enemyUnit.img.pos,
                endPos=(
                    endPosEnemy[0]
                    + (enemyUnit.imgAttackYang.width - enemyUnit.imgDash.width),
                    endPosEnemy[1],
                ),
                name="EnemyClash1",
            )
        )
    friendUnit.img.setPos(endPosFriend)
    friendUnit.imgAttackYang.setPos(endPosFriend)
    friendUnit.imgAttackYin.setPos(endPosFriend)
    if "(boss)" not in enemyUnit.name:
        enemyUnit.img.setPos(
            (
                endPosEnemy[0] + (enemyUnit.imgAttackYang.width - enemyUnit.img.width),
                endPosEnemy[1],
            )
        )
        enemyUnit.imgAttackYang.setPos(endPosEnemy)
        enemyUnit.imgAttackYin.setPos(endPosEnemy)


def clashState2(Animations: list, friendUnit: Character, enemyUnit: Character):
    """
    The characters clashed
    The calculation of yang is done here
    The return value can be:
    - 0: Simply HP, etc changed
    - 1: The enemy died
    - 2: The player died
    """

    global done
    from battleController import gSet

    done = 0
    friendUnit.showImg = friendUnit.imgAttackYang
    enemyUnit.showImg = enemyUnit.imgAttackYang
    friendLevel = sum(
        card.level
        for card in friendUnit.onHandCards
        if (card.type and "defence" not in card.effects)
    )
    enemyLevel = sum(
        card.level
        for card in enemyUnit.onHandCards
        if (card.type and "defence" not in card.effects)
    )

    friendCardInfo = cardInfoSurface(
        friendUnit,
        type=True,
        color=(
            gSet["--font-color-yellow"]
            if friendLevel > enemyLevel
            else gSet["--font-color-grey"]
        ),
    )
    enemyCardInfo = cardInfoSurface(
        enemyUnit,
        type=True,
        color=(
            gSet["--font-color-yellow"]
            if friendLevel < enemyLevel
            else gSet["--font-color-grey"]
        ),
    )

    posY = max(
        min(
            friendUnit.img.y - friendCardInfo.get_height() - 10,
            enemyUnit.img.y - enemyCardInfo.get_height() - 10,
        ),
        100,
    )  # ensure the card info is the same high (maybe more beautiful)
    friendCardInfoPos = (friendUnit.img.x - friendCardInfo.get_width() - 10, posY)
    enemyCardInfoPos = (enemyUnit.img.x + enemyUnit.img.width + 10, posY)

    gSet["friendClashInfo"] = Img(
        img=friendCardInfo, size=friendCardInfo.size, pos=friendCardInfoPos, alpha=0
    )
    gSet["enemyClashInfo"] = Img(
        img=enemyCardInfo, size=enemyCardInfo.size, pos=enemyCardInfoPos, alpha=0
    )

    Animations.append(
        moveAnimation(
            object=gSet["friendClashInfo"],
            animateSeconds=0.2,
            nowPos=(gSet["friendClashInfo"].x - 100, gSet["friendClashInfo"].y),
            endPos=gSet["friendClashInfo"].pos,
            name="friendClash4InfoFadeIn",
        )
    )
    Animations.append(
        moveAnimation(
            object=gSet["enemyClashInfo"],
            animateSeconds=0.2,
            nowPos=(gSet["enemyClashInfo"].x + 50, gSet["enemyClashInfo"].y),
            endPos=(gSet["enemyClashInfo"].x - 50, gSet["enemyClashInfo"].y),
            name="enemyClash4InfoFadeIn",
        )
    )

    Animations.append(
        fadeAnimation(
            object=gSet["friendClashInfo"],
            animateSeconds=0.1,
            nowAlpha=0,
            endAlpha=255,
            name="friendClash2InfoFadeIn",
        )
    )
    Animations.append(
        fadeAnimation(
            object=gSet["enemyClashInfo"],
            animateSeconds=0.1,
            nowAlpha=0,
            endAlpha=255,
            name="enemyClash2InfoFadeIn",
        )
    )

    if friendLevel == enemyLevel:
        pass
    elif friendLevel < enemyLevel:
        damage = enemyLevel - friendLevel
        friendUnit.HPlossThisTurn += damage
    else:
        damage = friendLevel - enemyLevel
        defence = sum(
            card.level
            for card in enemyUnit.onHandCards
            if (card.type and "defence" in card.effects)
        )
        if (
            damage > 0
            and damage - defence <= 0
            and sum(
                1
                for card in enemyUnit.onHandCards
                if (card.type and "hasCounterAttack" in card.effects)
            )
            > 0
        ):
            gSet["enemyUseSpecial"].append("counterAttack")
        else:
            enemyUnit.HPlossThisTurn += damage


def clashState3(Animations: list, friendUnit: Character, enemyUnit: Character):
    """
    Have a break
    """

    friendUnit.showImg = friendUnit.img
    enemyUnit.showImg = enemyUnit.img
    Animations.append(Sleep(seconds=0.3, name="Clash3"))


def clashState4(Animations: list, friendUnit: Character, enemyUnit: Character):
    """
    Calculate the yin level
    """

    global done
    from battleController import gSet

    done = 0
    friendUnit.showImg = friendUnit.imgAttackYin
    enemyUnit.showImg = enemyUnit.imgAttackYin
    friendLevel = sum(
        card.level
        for card in friendUnit.onHandCards
        if (not card.type and "defence" not in card.effects)
    )
    enemyLevel = sum(
        card.level
        for card in enemyUnit.onHandCards
        if (not card.type and "defence" not in card.effects)
    )

    friendCardInfo = cardInfoSurface(
        friendUnit,
        type=False,
        color=(
            gSet["--font-color-yellow"]
            if friendLevel > enemyLevel
            else gSet["--font-color-grey"]
        ),
    )
    enemyCardInfo = cardInfoSurface(
        enemyUnit,
        type=False,
        color=(
            gSet["--font-color-yellow"]
            if friendLevel < enemyLevel
            else gSet["--font-color-grey"]
        ),
    )

    posY = max(
        min(
            friendUnit.img.y - friendCardInfo.get_height() - 10,
            enemyUnit.img.y - enemyCardInfo.get_height() - 10,
        ),
        100,
    )  # ensure the card info is the same high (maybe more beautiful)
    friendCardInfoPos = (friendUnit.img.x - friendCardInfo.get_width() - 10, posY)
    enemyCardInfoPos = (enemyUnit.img.x + enemyUnit.img.width + 10, posY)

    gSet["friendClashInfo"] = Img(
        img=friendCardInfo, size=friendCardInfo.size, pos=friendCardInfoPos, alpha=0
    )
    gSet["enemyClashInfo"] = Img(
        img=enemyCardInfo, size=enemyCardInfo.size, pos=enemyCardInfoPos, alpha=0
    )

    Animations.append(
        moveAnimation(
            object=gSet["friendClashInfo"],
            animateSeconds=0.2,
            nowPos=(gSet["friendClashInfo"].x - 100, gSet["friendClashInfo"].y),
            endPos=gSet["friendClashInfo"].pos,
            name="friendClash4InfoFadeIn",
        )
    )
    Animations.append(
        moveAnimation(
            object=gSet["enemyClashInfo"],
            animateSeconds=0.2,
            nowPos=(gSet["enemyClashInfo"].x + 50, gSet["enemyClashInfo"].y),
            endPos=(gSet["enemyClashInfo"].x - 50, gSet["enemyClashInfo"].y),
            name="enemyClash4InfoFadeIn",
        )
    )

    Animations.append(
        fadeAnimation(
            object=gSet["friendClashInfo"],
            animateSeconds=0.2,
            nowAlpha=0,
            endAlpha=255,
            name="friendClash4InfoFadeIn",
        )
    )
    Animations.append(
        fadeAnimation(
            object=gSet["enemyClashInfo"],
            animateSeconds=0.2,
            nowAlpha=0,
            endAlpha=255,
            name="enemyClash4InfoFadeIn",
        )
    )

    if friendLevel == enemyLevel:
        pass
    elif friendLevel < enemyLevel:
        damage = enemyLevel - friendLevel
        friendUnit.HPlossThisTurn += damage
    else:
        damage = friendLevel - enemyLevel
        defence = sum(
            card.level
            for card in enemyUnit.onHandCards
            if (not card.type and "defence" in card.effects)
        )
        if (
            damage > 0
            and damage - defence <= 0
            and sum(
                1
                for card in enemyUnit.onHandCards
                if (not card.type and "hasCounterAttack" in card.effects)
            )
            > 0
        ):
            gSet["enemyUseSpecial"].append("counterAttack")
        else:
            enemyUnit.HPlossThisTurn += damage


def clashState5(Animations: list, friendUnit: Character, enemyUnit: Character):
    """
    The characters returned to their original positions
    """

    global done

    done = 0
    friendEndPos = friendOriginPos
    enemyEndPos = enemyOriginPos
    friendUnit.showImg = friendUnit.img
    enemyUnit.showImg = enemyUnit.img
    Animations.append(
        moveAnimation(
            object=friendUnit.img,
            animateSeconds=0.1,
            nowPos=friendUnit.img.pos,
            endPos=friendEndPos,
            name="FriendClash5",
        )
    )
    if "(boss)" in enemyUnit.name:
        Animations.append(
            moveAnimation(
                object=enemyUnit.imgDash,
                animateSeconds=0.5,
                nowPos=enemyUnit.img.pos,
                endPos=enemyUnit.img.pos,
                name="EnemyClash5",
            )
        )
    else:
        Animations.append(
            moveAnimation(
                object=enemyUnit.img,
                animateSeconds=0.1,
                nowPos=enemyUnit.img.pos,
                endPos=enemyEndPos,
                name="EnemyClash5",
            )
        )
    friendUnit.imgDash.setPos(friendEndPos)
    friendUnit.imgAttackYang.setPos(friendEndPos)
    friendUnit.imgAttackYin.setPos(friendEndPos)
    enemyUnit.imgAttackYang.setPos(enemyEndPos)
    enemyUnit.imgAttackYin.setPos(enemyEndPos)
