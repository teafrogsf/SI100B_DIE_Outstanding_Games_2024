class Character:
    from Img import Img
    from Card import Card

    def __init__(
        self,
        ID: str,
        name: str,
        HP: int,
        SP: int,
        SPHeal: int,
        maxHP: int,
        maxSP: int,
        cards: list,
        img: Img,
        imgDash: Img,
        imgAttackYang: Img,
        imgAttackYin: Img,
    ):
        self.ID = ID
        self.name = name
        self.HP = HP
        self.SP = SP
        self.SPHeal = SPHeal
        self.cards = cards
        self.maxHP = maxHP
        self.maxSP = maxSP
        self.img = img
        self.imgDash = imgDash
        self.imgAttackYang = imgAttackYang
        self.imgAttackYin = imgAttackYin
        self.showImg = img
        self.onHandCards = cards
        self.usedCards = []
        self.unusedCards = []
        self.useThisTurn = []
        self.lostThisTurn = []
        self.getThisTurn = []
        self.HPlossThisTurn = 0

    def __str__(self):
        return self.ID

    def SPlossThisTurn(self) -> int:
        """
        Get the SP loss of the character this turn.
        """

        return len(self.useThisTurn) + len(self.getThisTurn)

    def useCard(self, card: Card) -> None:
        """
        Use a card.
        If the card has effect "When used ..." [time='use'], apply the effect.
        """

        for effect in card.effects:
            pass  # TODO <------------------------------------------------------------------------------------------ apply the effect
        try:
            self.onHandCards.remove(card)
        except ValueError:
            raise ValueError("Invalid card: the card is not on hand")
        self.usedCards.append(card)
        self.useThisTurn.append(card)
        if self.SP - len(self.useThisTurn) < 0:
            raise ValueError("Invalid SP: the SP of the character is negative")

    def lostCard(self, card: Card) -> None:
        """
        Lost a card
        If the card has effect "When lost ..." [time='lost'], apply the effect.
        """

        for effect in card.effects:
            pass  # TODO <------------------------------------------------------------------------------------------ apply the effect
        try:
            self.onHandCards.remove(card)
        except ValueError:
            raise ValueError("Invalid card: the card is not on hand")
        self.usedCards.append(card)
        self.lostThisTurn.append(card)

    def getCard(self) -> Card:
        import random

        """
        Get a card.
        If the card has effect "When get ..." [time='get'], apply the effect.
        If the character has no cards left, shuffle the used cards and set them as the cards of the character.
        If no used cards are left, or the character can't draw a card, return None
        """

        if self.SP - self.SPlossThisTurn() <= 0:
            return None
        if self.unusedCards == []:
            self.unusedCards = self.usedCards
            self.usedCards = []
            if self.unusedCards == []:
                return None
        card = random.choice(self.unusedCards)
        self.unusedCards.remove(card)
        for effect in card.effects:
            pass  # TODO <------------------------------------------------------------------------------------------ apply the effect
        self.getThisTurn.append(card)
        self.onHandCards.append(card)
        return card

    def directLoad(self, cards: list) -> None:
        """
        Directly load the cards to the character.
        Put these cards on hand.
        For all the other cards, put them in the unused cards.
        This is used ONLY for enemies, as they can't draw cards (so they operate in fixed strategies).
        """

        self.onHandCards = []
        for card in cards:
            self.onHandCards.append(card)
        self.unusedCards = [card for card in self.cards if card not in self.onHandCards]
        self.usedCards = []
        self.useThisTurn = []
        self.lostThisTurn = []
        self.getThisTurn = []


def copyCharacter(char: Character):
    """
    Copy the character.
    It must be a deep copy.
    """

    import copy

    return copy.deepcopy(char)
