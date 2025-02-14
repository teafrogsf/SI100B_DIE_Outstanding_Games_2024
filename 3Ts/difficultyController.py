import json

from battleController import gSet

levelNum = 5


def load(level):
    """
    Load the data of the level
    """

    with open(f"./save/level{level}.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def save(level, data):
    """
    Save the data of the level
    """

    with open(f"./save/level{level}.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def loadOrigin(level):
    """
    Load the original data of the level
    """

    with open(f"./save/origin/level{level}.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def setEasy():
    """
    Set the difficulty to easy.
    - All levels of the cards of the enemies are decreased by 1 (except it is already 1).
    - The enemies have 20% less HP.
    """

    for level in range(3):
        data = loadOrigin(level)
        for enemy in data["Enemies"]:
            enemy["HP"] = int(enemy["HP"] * 0.8)
            for card in enemy["cards"]:
                if card["level"] > 1:
                    card["level"] -= 1
        save(level, data)


def setNormal():
    """
    Set the difficulty to normal.
    This is the original difficulty.
    """

    for level in range(3):
        data = loadOrigin(level)
        save(level, data)


def setHard():
    """
    Set the difficulty to hard.
    - All levels of the cards of the enemies are increased by 2.
    - If the level is already larger than 5 (strictly), it will be increased by 1, instead of 2.
    - The enemies have 25% more HP.
    """

    for level in range(3):
        data = loadOrigin(level)
        for enemy in data["Enemies"]:
            enemy["HP"] = int(enemy["HP"] * 1.25)
            for card in enemy["cards"]:
                if card["level"] > 5:
                    card["level"] += 1
                else:
                    card["level"] += 2
        save(level, data)


def reset():
    """
    Reset each level to the original state.
    """

    for level in range(3):
        data = loadOrigin(level)
        save(level, data)
