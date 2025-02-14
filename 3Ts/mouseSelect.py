from Card import cardAttack
from Character import Character
import pygame as pg

selectedCards = set()
hoveredCards = None
hoveredCardPos = None
selectedFriendCard = None

cardAttacktime = 0


def data(name: str):
    if name == "selectedCards":
        return selectedCards
    elif name == "hoveredCards":
        return hoveredCards
    elif name == "hoveredCardPos":
        return hoveredCardPos
    elif name == "selectedFriendCard":
        return selectedFriendCard


def attackClear():
    global cardAttacktime
    cardAttacktime = 0


def checkCardSelection(friendUnit: Character, enemyUnit: Character):
    """
    Check if the player chooses enough card. If so, do such a card-attack.
    """

    global selectedFriendCard, selectedCards, cardAttacktime
    if selectedFriendCard is None:
        return

    cardAttacktime += 1
    gate = selectedFriendCard.gate
    if gate == "not" and len(selectedCards) == 2:
        enemyCard = next(card for card in selectedCards if card != selectedFriendCard)
        newCard = cardAttack(
            gate=gate,
            card0=selectedFriendCard,
            card1=enemyCard,
            card2=None,
            time=cardAttacktime,
        )
        enemyUnit.onHandCards.append(newCard)
        friendUnit.useCard(selectedFriendCard)
        enemyUnit.lostCard(enemyCard)
        selectedCards.clear()
        selectedFriendCard = None
    elif (
        gate in ["and", "or", "xor", "nand", "nor", "xnor"] and len(selectedCards) == 3
    ):
        enemyCards = [card for card in selectedCards if card != selectedFriendCard]
        newCard = cardAttack(
            gate=gate,
            card0=selectedFriendCard,
            card1=enemyCards[0],
            card2=enemyCards[1],
            time=cardAttacktime,
        )
        enemyUnit.onHandCards.append(newCard)
        friendUnit.useCard(selectedFriendCard)
        enemyUnit.lostCard(enemyCards[0])
        enemyUnit.lostCard(enemyCards[1])
        selectedCards.clear()
        selectedFriendCard = None


def cardHover(mousePos: tuple, friendUnit: Character, enemyUnit: Character):
    """
    Check if the player uses mouse to hover over a card
    """

    from battleController import gSet

    global hoveredCards, hoveredCardPos

    hoveredCards = None
    hoveredCardPos = None
    cardSpacing = gSet["cardSpace"]

    for card in friendUnit.onHandCards + enemyUnit.onHandCards:
        x = None
        y = None
        maxCardsPerRow = max(
            (gSet["screenWidth"] // 2 - 180) // (gSet["cardWidth"] + cardSpacing), 1
        )
        if card in friendUnit.onHandCards:
            index = friendUnit.onHandCards.index(card)
            row = index // maxCardsPerRow
            col = index % maxCardsPerRow
            x = 10 + col * (gSet["cardWidth"] + cardSpacing)
            y = (
                gSet["screenHeight"]
                - gSet["cardHeight"]
                - 10
                - row * (gSet["cardHeight"] + cardSpacing)
            )
        else:
            index = enemyUnit.onHandCards.index(card)
            row = index // maxCardsPerRow
            col = index % maxCardsPerRow
            x = gSet["screenWidth"] - (col + 1) * (gSet["cardWidth"] + cardSpacing)
            y = (
                gSet["screenHeight"]
                - gSet["cardHeight"]
                - 10
                - row * (gSet["cardHeight"] + cardSpacing)
            )

        card_rect = pg.Rect(x, y, gSet["cardWidth"], gSet["cardHeight"])
        if card_rect.collidepoint(mousePos):
            mask = pg.mask.from_surface(card.img.img)
            local_pos = mousePos[0] - x, mousePos[1] - y
            if mask.get_at(local_pos):
                hoveredCards = card
                hoveredCardPos = (x, y)
                break


def cardSelect(friendUnit: Character, enemyUnit: Character):
    """
    Check if the player select a card
    The player cannot select a card which has effect "selectProhibit"
    """

    global hoveredCards, selectedFriendCard

    if hoveredCards:
        if hoveredCards in selectedCards:
            selectedCards.remove(hoveredCards)
            if selectedFriendCard == hoveredCards:
                selectedFriendCard = None
        else:
            if hoveredCards in friendUnit.onHandCards:
                if selectedFriendCard is None:
                    selectedFriendCard = hoveredCards
                    selectedCards.add(hoveredCards)
                else:
                    selectedCards.remove(selectedFriendCard)
                    selectedFriendCard = hoveredCards
                    selectedCards.add(hoveredCards)
            elif (
                selectedFriendCard is not None
                and hoveredCards in enemyUnit.onHandCards
                and "selectProhibit" not in hoveredCards.effects
            ):
                if selectedFriendCard.gate == "not" and len(selectedCards) == 1:
                    selectedCards.add(hoveredCards)
                    checkCardSelection(friendUnit, enemyUnit)
                elif (
                    selectedFriendCard.gate
                    in ["and", "or", "xor", "nand", "nor", "xnor"]
                    and len(selectedCards) < 3
                ):
                    selectedCards.add(hoveredCards)
                    if len(selectedCards) == 3:
                        checkCardSelection(friendUnit, enemyUnit)


def turnEndPress():
    """
    Check if the player presses the end turn button
    """

    from battleController import gSet

    turnEndImgRect = pg.Rect(
        gSet["turnButton"].x,
        gSet["turnButton"].y,
        gSet["endTurnButtonWidth"],
        gSet["endTurnButtonHeight"],
    )
    if turnEndImgRect.collidepoint(pg.mouse.get_pos()):
        return "End"
    return ""


def drawPress(event: pg.Event):
    """
    Check if the player presses the draw button
    """

    from battleController import gSet

    drawImgRect = pg.Rect(
        gSet["drawButton"].x,
        gSet["drawButton"].y,
        gSet["draw&undoButtonWidth"],
        gSet["draw&undoButtonHeight"],
    )
    if drawImgRect.collidepoint(event.pos):
        return "Draw"
    return ""


def undoTurnPress(event: pg.Event):
    """
    Check if the player presses the undo turn button
    """

    from battleController import gSet

    undoImgRect = pg.Rect(
        gSet["undoButton"].x,
        gSet["undoButton"].y,
        gSet["draw&undoButtonWidth"],
        gSet["draw&undoButtonHeight"],
    )
    if undoImgRect.collidepoint(event.pos):
        attackClear()
        return "Undo"
    return ""


def mouseLeftButton(event: pg.Event, friendUnit: Character, enemyUnit: Character):
    """
    Check the following events:
    - Select a card
    - Press turn end
    - Press draw
    - Press undo
    """

    cardSelect(friendUnit=friendUnit, enemyUnit=enemyUnit)

    buttonState = ""
    buttonState += turnEndPress()
    buttonState += drawPress(event)
    buttonState += undoTurnPress(event)

    return buttonState


def mouseRightButton(event: pg.Event):
    pass


def mouseMiddleButton(event: pg.Event):
    pass


def mouseMove(event: pg.Event, friendUnit: Character, enemyUnit: Character):
    cardHover(mousePos=event.pos, friendUnit=friendUnit, enemyUnit=enemyUnit)
