import pygame as pg
from Img import Img
from Card import Card
from Character import Character


def drawBattleInfo(
    friendUnit: Character, enemyUnit: Character, enemyID: int, enemyNumber: int
):
    """
    Battle information includes:
    - HP and SP bars for both friend and enemy units
        - Character unit's HP and SP at the top left corner
        - Enemy unit's HP and SP at the top right corner
    - Buttons for the battle
        - Turn end button at the top center
        - Draw button at the bottom center (slightly left)
        - Undo button at the bottom center (slightly right)
    """

    from battleController import gSet

    barWidth = gSet["screenWidth"] // 3
    barHeight = 20

    # friend's HP and SP bars
    friendHPratio = friendUnit.HP / friendUnit.maxHP
    pg.draw.rect(gSet["screen"], gSet["--HP-ground"], (10, 10, barWidth, barHeight))
    pg.draw.rect(
        gSet["screen"],
        gSet["--HP-front"],
        (10, 10, barWidth * friendHPratio, barHeight),
    )
    if friendUnit.HP > 0 and friendUnit.HPlossThisTurn > 0:
        ratio = min(friendUnit.HPlossThisTurn, friendUnit.HP) / friendUnit.HP
        usedWidth = barWidth * friendHPratio * ratio
        pg.draw.rect(
            gSet["screen"],
            gSet["--HP-third"],
            (10 + barWidth * friendHPratio - usedWidth, 10, usedWidth, barHeight),
        )
    friendSPratio = friendUnit.SP / friendUnit.maxSP
    pg.draw.rect(gSet["screen"], gSet["--SP-ground"], (10, 40, barWidth, barHeight))
    pg.draw.rect(
        gSet["screen"],
        gSet["--SP-front"],
        (10, 40, barWidth * friendSPratio, barHeight),
    )
    if friendUnit.SP > 0 and friendUnit.SPlossThisTurn() > 0:
        ratio = friendUnit.SPlossThisTurn() / friendUnit.SP
        usedWidth = barWidth * friendSPratio * ratio
        pg.draw.rect(
            gSet["screen"],
            gSet["--SP-third"],
            (10 + barWidth * friendSPratio - usedWidth, 40, usedWidth, barHeight),
        )

    # enemy's HP and number bars
    enemyHPratio = enemyUnit.HP / enemyUnit.maxHP
    pg.draw.rect(
        gSet["screen"],
        gSet["--HP-ground"],
        (gSet["screenWidth"] - barWidth - 10, 10, barWidth, barHeight),
    )
    pg.draw.rect(
        gSet["screen"],
        gSet["--HP-front"],
        (gSet["screenWidth"] - barWidth - 10, 10, barWidth * enemyHPratio, barHeight),
    )
    if enemyUnit.HP > 0 and enemyUnit.HPlossThisTurn > 0:
        ratio = min(enemyUnit.HPlossThisTurn, enemyUnit.HP) / enemyUnit.HP
        usedWidth = barWidth * enemyHPratio * ratio
        pg.draw.rect(
            gSet["screen"],
            gSet["--HP-third"],
            (
                gSet["screenWidth"]
                - barWidth
                - 10
                + barWidth * enemyHPratio
                - usedWidth,
                10,
                usedWidth,
                barHeight,
            ),
        )
    enemyNMratio = enemyID / enemyNumber
    pg.draw.rect(
        gSet["screen"],
        gSet["--Enemy-number-ground"],
        (gSet["screenWidth"] - barWidth - 10, 40, barWidth, barHeight),
    )
    pg.draw.rect(
        gSet["screen"],
        gSet["--Enemy-number-front"],
        (gSet["screenWidth"] - barWidth - 10, 40, barWidth * enemyNMratio, barHeight),
    )

    # Display Character unit's HP and SP at the top left corner
    friendHPtextContent = f"HP: {friendUnit.HP}"
    if friendUnit.HPlossThisTurn > 0:
        friendHPtextContent += f" (-{friendUnit.HPlossThisTurn})"
    friendHPtext = gSet["font-battleInfo"].render(
        friendHPtextContent, True, gSet["--font-color-light"]
    )
    friendSPtextContent = f"SP: {friendUnit.SP}"
    if friendUnit.SPlossThisTurn() > 0:
        friendSPtextContent += f" (-{friendUnit.SPlossThisTurn()})"
    friendSPtext = gSet["font-battleInfo"].render(
        friendSPtextContent, True, gSet["--font-color-light"]
    )
    gSet["screen"].blit(friendHPtext, (10, 3))
    gSet["screen"].blit(friendSPtext, (10, 33))

    # Display enemy unit's HP and number at the top right corner
    enemyHPtextContent = f"HP: {enemyUnit.HP}"
    if enemyUnit.HPlossThisTurn > 0:
        enemyHPtextContent += f" (-{enemyUnit.HPlossThisTurn})"
    enemyHPtext = gSet["font-battleInfo"].render(
        enemyHPtextContent, True, gSet["--font-color-light"]
    )
    enemyNMtextContent = f"WAVE: {enemyID} / {enemyNumber}"
    if enemyUnit.SPlossThisTurn() > 0:
        enemyNMtextContent += f" (-{enemyUnit.SPlossThisTurn()})"
    enemyNMtext = gSet["font-battleInfo"].render(
        enemyNMtextContent, True, gSet["--font-color-light"]
    )
    gSet["screen"].blit(
        enemyHPtext, (gSet["screenWidth"] - enemyHPtext.get_width() - 10, 3)
    )
    gSet["screen"].blit(
        enemyNMtext, (gSet["screenWidth"] - enemyNMtext.get_width() - 10, 33)
    )

    # Display the bottons
    gSet["screen"].blit(gSet["turnButton"].img, gSet["turnButton"].pos)
    gSet["screen"].blit(gSet["drawButton"].img, gSet["drawButton"].pos)
    gSet["screen"].blit(gSet["undoButton"].img, gSet["undoButton"].pos)


def drawUnits(friend: Img, enemy: Img):
    """
    Draw the character units on the gSet['screen']
    """

    from battleController import gSet

    gSet["screen"].blit(friend.img, friend.pos)
    gSet["screen"].blit(enemy.img, enemy.pos)


def drawCards(friendUnit: Character, enemyUnit: Character):
    """
    Draw the cards
    friendUnit's cards are displayed at the bottom left
    enemyUnit's cards are displayed at the bottom right
    """

    from battleController import gSet

    cardSpacing = gSet["cardSpace"]

    # Display friend unit's cards at the bottom left
    for i, card in enumerate(friendUnit.onHandCards):
        cardWidth, cardHeight = gSet["cardSize"]
        maxCardsPerRow = max(
            (gSet["screenWidth"] // 2 - 180) // (cardWidth + cardSpacing), 1
        )
        row = i // maxCardsPerRow
        col = i % maxCardsPerRow
        x = 10 + col * (cardWidth + cardSpacing)
        y = gSet["screenHeight"] - cardHeight - 10 - row * (cardHeight + cardSpacing)
        card.img.setPos((x, y))
        gSet["screen"].blit(card.img.img, card.img.pos)

    # Display enemy unit's cards at the bottom right
    for i, card in enumerate(enemyUnit.onHandCards):
        cardWidth, cardHeight = gSet["cardSize"]
        maxCardsPerRow = max(
            (gSet["screenWidth"] // 2 - 180) // (cardWidth + cardSpacing), 1
        )
        row = i // maxCardsPerRow
        col = i % maxCardsPerRow
        x = gSet["screenWidth"] - (col + 1) * (cardWidth + cardSpacing)
        y = gSet["screenHeight"] - cardHeight - 10 - row * (cardHeight + cardSpacing)
        card.img.setPos((x, y))
        gSet["screen"].blit(card.img.img, card.img.pos)


def drawCardBorders(
    friendUnit: Character, enemyUnit: Character, selectedCards: list, hoveredCards: list
):
    """
    Draw the borders for the selected and hovered cards
    If selected, use the selected card border color
    If hovered, use the hovered card border color
    The border should be drawn around the real card image, not the card space (not include the transparent space)
    """

    from battleController import gSet

    cardSpacing = gSet["cardSpace"]

    def drawCardBorder(image, position, color, width=3):
        mask = pg.mask.from_surface(image)
        outline = mask.outline()
        outline = [(position[0] + x, position[1] + y) for x, y in outline]
        if outline:
            pg.draw.lines(gSet["screen"], color, True, outline, width)

    # Draw borders for friend unit's cards
    for i, card in enumerate(friendUnit.onHandCards):
        cardWidth, cardHeight = gSet["cardSize"]
        maxCardsPerRow = max(
            (gSet["screenWidth"] // 2 - 180) // (cardWidth + cardSpacing), 1
        )  # 每行最多显示的卡牌数量
        row = i // maxCardsPerRow
        col = i % maxCardsPerRow
        x = 10 + col * (cardWidth + cardSpacing)
        y = gSet["screenHeight"] - cardHeight - 10 - row * (cardHeight + cardSpacing)

        if card == hoveredCards:
            drawCardBorder(card.img.img, (x, y), gSet["--select-card"])
        elif card in selectedCards:
            drawCardBorder(card.img.img, (x, y), gSet["--selected-card"])

    # Draw borders for enemy unit's cards
    for i, card in enumerate(enemyUnit.onHandCards):
        cardWidth, cardHeight = gSet["cardSize"]
        maxCardsPerRow = max(
            (gSet["screenWidth"] // 2 - 180) // (cardWidth + cardSpacing), 1
        )  # 每行最多显示的卡牌数量
        row = i // maxCardsPerRow
        col = i % maxCardsPerRow
        x = gSet["screenWidth"] - (col + 1) * (cardWidth + cardSpacing)
        y = gSet["screenHeight"] - cardHeight - 10 - row * (cardHeight + cardSpacing)

        if card == hoveredCards:
            drawCardBorder(card.img.img, (x, y), gSet["--select-card"])
        elif card in selectedCards:
            drawCardBorder(card.img.img, (x, y), gSet["--selected-card"])


def drawCardDetail(card: Card, cardFrom: bool):  # True = friend | False = enemy
    """
    Display the card information when hovering over the card
    If the card is from the friend unit and it is selected, display, too
    """

    from battleController import gSet

    if not card:
        return

    # Font set
    cardInfo = [
        f"名称: {card.title}",
        f"门类: {'与' if card.gate == 'and' else '非' if card.gate == 'not' else '或' if card.gate == 'or' else '异' if card.gate == 'xor' else '与非' if card.gate == 'nand' else '或非' if card.gate == 'nor' else '同' if card.gate == 'xnor' else '无类'}",
        f"类型: {'阳' if card.type else '阴'}",
        f"等级: {card.level}",
    ]
    if card.description != "":
        cardInfo.append(f"描述: {card.description}")

    # Card position
    if cardFrom:
        x, y = 10, 70
    else:
        x, y = gSet["screenWidth"] - gSet["screenWidth"] // 3 - 10, 70

    maxWidth = max(gSet["font-cardDetail"].size(line)[0] for line in cardInfo) + 20
    maxWidth = min(maxWidth, 500)

    def wrap(text: str, font: pg.Font, maxWidth: int):
        """
        Wrap text to fit within a given width when rendered with the specified font.
        """
        lines = []
        current_line = ""
        for char in text:
            current_line += char
            width, _ = font.size(current_line)
            if width > maxWidth:
                lines.append(current_line[:-1])
                current_line = char
        if current_line:
            lines.append(current_line)
        return lines

    cardInfoNew = []
    for line in cardInfo:
        texts = wrap(text=line, font=gSet["font-cardDetail"], maxWidth=maxWidth)
        cardInfoNew += texts
    cardInfo = cardInfoNew
    backgroundHeight = len(cardInfo) * 24 + 10

    backgroundRect = pg.Surface((maxWidth, backgroundHeight))
    backgroundRect.set_alpha(255 * 0.7)
    backgroundRect.fill(gSet["--card-info-ground"])

    if not cardFrom:
        x += gSet["screenWidth"] // 3 - maxWidth
    gSet["screen"].blit(backgroundRect, (x, y))

    for line in cardInfo:
        infoText = gSet["font-cardDetail"].render(
            line, True, gSet["--font-color-light"]
        )
        gSet["screen"].blit(infoText, (x + 10, y))
        y += 24
