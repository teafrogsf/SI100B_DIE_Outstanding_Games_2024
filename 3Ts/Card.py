class Card:
    from Img import Img

    def __init__(
        self,
        ID: str,
        title: str,
        description: str,
        gate: str,
        type: bool,
        level: int,
        effects: list,
        img: Img,
    ):
        self.ID = ID
        self.title = title
        self.description = description
        self.gate = gate
        self.type = type
        self.level = level
        self.effects = effects
        self.img = img

    def __str__(self):
        return self.ID


def cardAttack(gate: str, card0: Card, card1: Card, card2: Card = None, time: int = 0):
    """
    Use the gate of self to attack the cards
    gate: The gate of the card that is attacking.
    card1, card2: The cards that are being attacked.
    When attacked, the cards will be merged into one,
        with the effects of the card being applied to the new card (except for fragile effects).
    The level of the new card will be the sum of the levels of the two cards.
    """

    import pygame as pg
    from Img import Img

    if card0.gate != gate:
        raise ValueError(
            "Invalid operation: the gate of the card is not the same as the gate of the operation"
        )
    resultCard = Card(
        ID=0,
        title=f"生成卡[{time}]",
        description=card1.title + ("" if card2 is None else "+" + card2.title),
        gate="None",
        type=True,
        level=0,
        effects=[],
        img=Img(pg.image.load("./assets/card/1.png").convert_alpha(), (75, 75), (0, 0)),
    )
    if gate == "not":
        if card2 is not None:
            raise ValueError("Invalid operation: 'not' gate operates on one card")
        resultCard.type = not card1.type
        resultCard.level = card1.level
        for effect in card1.effects:
            if "fragile" not in effect:
                resultCard.effects.append(effect)
    elif gate == "and":
        if card2 is None:
            raise ValueError("Invalid operation: 'and' gate operates on two cards")
        resultCard.type = card1.type and card2.type
        resultCard.level = max(card1.level, card2.level)
        for effect in card1.effects:
            if "fragile" not in effect:
                resultCard.effects.append(effect)
        for effect in card2.effects:
            if "fragile" not in effect:
                resultCard.effects.append(effect)
    elif gate == "or":
        if card2 is None:
            raise ValueError("Invalid operation: 'or' gate operates on two cards")
        resultCard.type = card1.type or card2.type
        resultCard.level = max(card1.level, card2.level)
        for effect in card1.effects:
            if "fragile" not in effect:
                resultCard.effects.append(effect)
        for effect in card2.effects:
            if "fragile" not in effect:
                resultCard.effects.append(effect)
    elif gate == "xor":
        if card2 is None:
            raise ValueError("Invalid operation: 'xor' gate operates on two cards")
        resultCard.type = card1.type != card2.type
        resultCard.level = max(card1.level, card2.level)
        for effect in card1.effects:
            if "fragile" not in effect:
                resultCard.effects.append(effect)
        for effect in card2.effects:
            if "fragile" not in effect:
                resultCard.effects.append(effect)
    elif gate == "nand":
        if card2 is None:
            raise ValueError("Invalid operation: 'nand' gate operates on two cards")
        resultCard.type = not (card1.type and card2.type)
        resultCard.level = max(card1.level, card2.level)
        for effect in card1.effects:
            if "fragile" not in effect:
                resultCard.effects.append(effect)
        for effect in card2.effects:
            if "fragile" not in effect:
                resultCard.effects.append(effect)
    elif gate == "nor":
        if card2 is None:
            raise ValueError("Invalid operation: 'nor' gate operates on two cards")
        resultCard.type = not (card1.type or card2.type)
        resultCard.level = max(card1.level, card2.level)
        for effect in card1.effects:
            if "fragile" not in effect:
                resultCard.effects.append(effect)
        for effect in card2.effects:
            if "fragile" not in effect:
                resultCard.effects.append(effect)
    elif gate == "xnor":
        if card2 is None:
            raise ValueError("Invalid operation: 'nxor' gate operates on two cards")
        resultCard.type = not (card1.type != card2.type)
        resultCard.level = max(card1.level, card2.level)
        for effect in card1.effects:
            if "fragile" not in effect:
                resultCard.effects.append(effect)
        for effect in card2.effects:
            if "fragile" not in effect:
                resultCard.effects.append(effect)
    else:
        raise ValueError("Invalid gate: the gate does not exist")
    return resultCard
