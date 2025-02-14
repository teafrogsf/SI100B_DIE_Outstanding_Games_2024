"""
这是个用来编辑地图的文件
0 -> 空地
1 -> 道路
2 -> 宝箱
3 -> 地刺
4,5 -> 传送门（前进）
6,7 -> 传送门（返回）
8 -> 空气墙

row, col 的顺序和 pygame 坐标系顺序一样
x 轴向右为正方向, y 轴向下为正方向
"""

import random, time
from GameSettings import *


class GenMap:
    def __init__(self, id):
        self.row = WindowSettings.height // MoveSettings.blockSize
        self.col = WindowSettings.width // MoveSettings.blockSize
        if id != 3:
            self.col *= 3  # 屏幕外的地图
        else:
            self.col *= 2

        self.Map = [
            [[0 for i in range(self.col)] for j in range(self.row)] for k in range(4)
        ]  # n*m*4
        self.ChestMoney = [
            [[0 for i in range(self.col)] for j in range(self.row)] for k in range(4)
        ]  # n*m*4

        if id == 0:
            self.randomMap()
        else:
            self.designedMap(id)

    def designedMap(self, id):
        # row = 13, col = 60 or 40
        r = self.row
        c = self.col

        # 铺地板
        for j in range(c):
            self.Map[1][r - 1][j] = 1

        if id == 1:
            self.Map[1][r - 2][5] = 6
            self.Map[1][r - 2][6] = 7

            # 多级向上 AD 跳
            for i in range(r - 3):
                self.Map[1][i][3] = 1
            self.Map[1][r - 4][4] = 1
            self.Map[1][r - 7][4] = 1
            self.Map[1][r - 10][4] = 1
            self.Map[1][r - 11][4] = 2
            self.ChestMoney[1][r - 11][4] = random.randint(20, 30)

            self.Map[1][r - 2][9] = 1
            for i in range(r - 3, r):
                self.Map[1][i][10] = 1
            for i in range(r - 5, r - 2):
                self.Map[1][i][11] = 1

            # 远跳 + 冲刺
            self.Map[1][r - 3][12] = 1
            self.Map[1][r - 6][20] = 1
            self.Map[1][r - 6][28] = 1

            self.Map[1][r - 7][28] = 2
            self.ChestMoney[1][r - 7][28] = random.randint(20, 30)

            self.Map[1][r - 6][29] = 1
            self.Map[1][r - 7][29] = 3

            self.Map[1][r - 5][32] = 1
            self.Map[1][r - 6][32] = 3
            self.Map[1][r - 5][33] = 1
            self.Map[1][r - 5][34] = 1
            self.Map[1][r - 6][34] = 3

            self.Map[1][r - 10][34] = 1
            self.Map[1][r - 7][36] = 1

            self.Map[1][r - 11][40] = 1
            self.Map[1][r - 11][41] = 1

            for i in range(r - 9, r - 1):
                self.Map[1][i][46] = 1
            self.Map[1][r - 6][47] = 1
            self.Map[1][r - 4][48] = 1

            for i in range(51, 57):
                self.Map[1][r - 5][i] = 1
                self.Map[1][r - 8][i] = 1
            self.Map[1][r - 6][56] = 1
            self.Map[1][r - 7][56] = 1
            self.Map[1][r - 6][55] = 2
            self.ChestMoney[1][r - 6][55] = random.randint(20, 30)

            for i in range(56, 59):
                self.Map[1][r - 8][i] = 1

            for i in range(50, 53):
                self.Map[1][r - 2][i] = 3

            self.Map[1][r - 2][58] = 2
            self.ChestMoney[1][r - 2][58] = random.randint(20, 30)
            self.Map[1][r - 2][57] = 2
            self.ChestMoney[1][r - 2][57] = random.randint(20, 30)

            for i in range(r):
                self.Map[1][i][59] = 1

            self.Map[1][r - 9][57] = 4
            self.Map[1][r - 9][58] = 5

        if id == 2:
            # 铺地板
            for j in range(self.col):
                self.Map[2][r - 1][j] = 1
            self.Map[2][r - 2][0] = 6
            self.Map[2][r - 2][1] = 7
            self.Map[2][r - 4][3] = 1
            self.Map[2][r - 7][3] = 1
            self.Map[2][r - 10][3] = 1
            self.Map[2][r - 10][4] = 1

            for i in range(3, r - 4):
                self.Map[2][i][5] = 1
            self.Map[2][r - 2][5] = 3

            for i in range(3, r - 4):
                self.Map[2][i][12] = 1
            self.Map[2][r - 2][12] = 3
            self.Map[2][r - 2][14] = 2
            self.ChestMoney[2][r - 2][14] = random.randint(20, 30)

            for i in range(18, 30):
                self.Map[2][r - 2][i] = 3

            self.Map[2][r - 4][20] = 1
            self.Map[2][r - 4][26] = 1
            self.Map[2][r - 5][26] = 2
            self.ChestMoney[2][r - 5][26] = random.randint(20, 30)
            self.Map[2][r - 4][30] = 1

            self.Map[2][r - 6][29] = 1
            self.Map[2][r - 8][32] = 1
            self.Map[2][r - 8][33] = 1
            for i in range(0, 3):
                self.Map[2][i][34] = 1
            for i in range(r - 8, r - 1):
                self.Map[2][i][34] = 1
            self.Map[2][r - 7][35] = self.Map[2][r - 11][35] = 1
            self.Map[2][r - 6][36] = self.Map[2][r - 10][36] = 1
            self.Map[2][r - 5][37] = self.Map[2][r - 9][37] = 1
            self.Map[2][r - 4][38] = self.Map[2][r - 8][38] = 1
            self.Map[2][r - 5][38] = 3
            self.Map[2][r - 3][39] = self.Map[2][r - 8][39] = 1
            self.Map[2][r - 2][40] = 2
            self.ChestMoney[2][r - 5][33] = random.randint(20, 30)
            self.Map[2][r - 2][41] = 3
            self.Map[2][r - 2][42] = 3
            self.Map[2][r - 2][43] = 3
            self.Map[2][r - 2][44] = 3

            self.Map[2][r - 2][54] = 4
            self.Map[2][r - 2][55] = 5

        if id == 3:
            self.Map[3][r - 3][0] = 6
            self.Map[3][r - 3][1] = 7
            for j in range(c):
                self.Map[3][r - 2][j] = 8

    # 随机生成地图
    def randomMap(self):
        random.seed(time.time())
        # 铺地板
        for j in range(self.col):
            self.Map[0][self.row - 1][j] = 1
        self.Map[0][self.row - 2][0] = 4
        self.Map[0][self.row - 2][1] = 5
        """
        GenTerrain1 几段连续的跳台
        """
        len1 = 5  # 每段 5 块
        cnt1 = 3  # 3 段
        maxHeight1 = 2  # 相邻两段的最大落差

        def GenTerrain1(x, lastY):
            for i in range(cnt1):
                l = max(lastY - maxHeight1, 3)
                r = min(lastY + maxHeight1, self.row - 4)  # 可以从最低的地面直接通过
                y = random.randint(l, r)
                L = x + i * len1
                R = min(self.col - 1, x + (i + 1) * len1 - 1)
                for j in range(L, R):
                    self.Map[0][y][j] = 1
                lastY = y
            return lastY

        lastY = self.row // 2
        for i in range(0, self.col, len1 * cnt1 + 1):
            lastY = GenTerrain1(i, lastY)

        """
        GenTerrain2 阶梯（上或下）
        """

        def GenTerrain2(x):
            vec = []
            for i in range(self.row):
                for j in range(self.col - 1):
                    if self.Map[0][i][j] == 1 and self.Map[0][i][j + 1] == 0:
                        vec.append([i, j])
            p = random.randint(0, len(vec) - 1)
            cnt = random.randint(2, 3)
            x = vec[p][0]
            y = vec[p][1]
            for i in range(cnt):
                if x < 0 or y < 0 or x > self.row - 1 or y > self.col - 1:
                    break
                if (x > 1 and self.Map[0][x - 1][y] == 1) or (
                    x < self.row - 1 and self.Map[0][x + 1][y] == 1
                ):
                    break
                self.Map[0][x][y] = 1
                x += 1
                y += 1

        for i in range(5):
            GenTerrain2(random.randint(10, self.col - 5))

        """
        GenChest 生成宝箱
        """

        def GenChest():
            vec = []
            for i in range(self.row):
                for j in range(self.col):
                    if (self.Map[0][i][j] == 1 and i > 0) and (i < self.row - 1):
                        vec.append((i, j))
            for i in range(3):
                p = random.randint(0, len(vec) - 1)
                self.Map[0][vec[p][0] - 1][vec[p][1]] = 2
                self.ChestMoney[0][vec[p][0] - 1][vec[p][1]] = random.randint(20, 30)

        GenChest()

        """
        GenTrap 生成陷阱
        """

        def GenTrap():
            # l = random.randint(0, self.col - 1)
            # r = random.randint(l, min(l + 3, self.col - 1))
            # for i in range(l, r):
            #     self.Map[0][self.row - 1][i] = 3
            vec = []
            for i in range(self.row):
                for j in range(self.col):
                    if (self.Map[0][i][j] == 1) and (i < self.row - 1):
                        vec.append([i, j])

            for i in range(10):
                p = random.randint(0, len(vec) - 1)
                self.Map[0][vec[p][0] - 1][vec[p][1]] = 3

        GenTrap()

        self.Map[0][self.row - 2][self.col - 2] = 4
        self.Map[0][self.row - 2][self.col - 1] = 5
