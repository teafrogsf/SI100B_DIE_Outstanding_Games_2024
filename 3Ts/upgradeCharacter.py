import json


def load():
    """
    Load the friend data from the file.
    """

    with open("./save/friends.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def save(data):
    """
    Save file with the friend data.
    """

    with open("./save/friends.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def findUnit(data, ID: str):
    """
    Locate the unit with the ID.
    """

    for unit in data["Friends"]:
        if unit["ID"] == ID:
            return unit
    return None


def addMaxHP(val: int):
    """
    Max HP is the maximum health point of the player.
    When gaining HP, the HP will also increase.
    """

    data = load()
    friend = findUnit(data, "fr1")
    if friend:
        friend["maxHP"] += val
        friend["HP"] += val
        save(data)


def addMaxSP(val: int):
    """
    Max SP is the maximum skill point of the player.
    The inital SP of a fight is always 70% of the max SP.
    """

    data = load()
    friend = findUnit(data, "fr1")
    if friend:
        import math

        friend["maxSP"] += val
        friend["SP"] = math.ceil(0.7 * friend["maxSP"])
        save(data)


def addSPHeal(val: int):
    """
    Add the number of SP that the player can gain in one turn.
    This is very very very ...(very * 100) useful. So it should be expensive.
    """

    data = load()
    friend = findUnit(data, "fr1")
    if friend:
        friend["SPHeal"] += val
        save(data)


def addAllCardLevel(val: int):
    """
    Add the level of each card of the player.
    This is also very very very ...(very * 100) useful. So it should be expensive.
    """

    data = load()
    friend = findUnit(data, "fr1")
    if friend:
        for card in friend["cards"]:
            card["level"] += val
        save(data)


def reset():
    """
    Reset all data to the original state.
    """

    with open("./save/origin/friends.json", "r", encoding="utf-8") as file:
        originData = json.load(file)
    save(originData)
