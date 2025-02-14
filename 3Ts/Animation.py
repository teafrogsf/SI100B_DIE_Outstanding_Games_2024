class Sleep:
    def __init__(self, seconds: float, name: str):
        import math
        from battleController import gSet

        self.frames = math.ceil(seconds * gSet["fps"])
        self.name = name

    def __str__(self):
        return self.name

    def update(self) -> bool:
        """
        Just sleeeeeeeeep
        If return True, the object should be removed since the animation is finished
        """

        self.frames -= 1
        if self.frames == 0:
            return True
        return False


class moveAnimation:
    from Img import Img

    def __init__(
        self,
        object: Img,
        animateSeconds: float,
        nowPos: tuple,
        endPos: tuple,
        name: str,
    ):
        import math
        from battleController import gSet

        self.object = object
        self.framRemain = math.ceil(animateSeconds * gSet["fps"])
        self.nowPos = nowPos
        object.setPos(nowPos)
        self.endPos = endPos
        self.moveXperFrame = (endPos[0] - self.nowPos[0]) / self.framRemain
        self.moveYperFrame = (endPos[1] - self.nowPos[1]) / self.framRemain
        self.name = name

    def __str__(self):
        return self.name

    def update(self) -> bool:
        """
        Update the position of the object
        If return True, the object should be removed since the animation is finished
        """

        self.framRemain -= 1
        self.nowPos = (
            self.nowPos[0] + self.moveXperFrame,
            self.nowPos[1] + self.moveYperFrame,
        )
        self.object.setPos(self.nowPos)

        if self.framRemain == 0:
            self.object.setPos(
                self.endPos
            )  # Ensure the object reaches the end position
            return True
        return False


class fadeAnimation:
    from Img import Img

    def __init__(
        self,
        object: Img,
        animateSeconds: float,
        nowAlpha: int,
        endAlpha: int,
        name: str,
    ):
        import math
        from battleController import gSet

        self.object = object
        self.framRemain = math.ceil(animateSeconds * gSet["fps"])
        self.nowAlpha = nowAlpha
        self.endAlpha = endAlpha
        self.fadePerFrame = (endAlpha - nowAlpha) / self.framRemain
        self.name = name

    def __str__(self):
        return self.name

    def update(self) -> bool:
        """
        Update the alpha of the object
        If return True, the object should be removed since the animation is finished
        """

        self.framRemain -= 1
        self.nowAlpha += self.fadePerFrame
        self.object.setAlpha(self.nowAlpha)

        if self.framRemain == 0:
            self.object.setAlpha(
                self.endAlpha
            )  # Ensure the object reaches the end alpha
            return True
        return False
