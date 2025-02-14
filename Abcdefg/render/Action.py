ACTIONS = []  # 用于存储所有动作的列表


class Action:

    # 构造函数，初始化动作
    def __init__(self, name: str, file):
        ACTIONS.append(self)  # 将当前动作对象添加到 ACTIONS 列表中
        self.name = name  # 动作的名称
        self.pos = []  # 存储动作位置和其他参数的列表
        self.ticks = 0  # 当前动作的帧数
        if file is not None:
            with open(file, "r") as f:
                s = f.read()  # 读取文件内容
                for line in s.split('\n'):  # 按行分割文件内容
                    if len(line) == 0:
                        continue  # 跳过空行
                    line1 = line.split('|')  # 按“|”分割行
                    num = line1[0].split()  # 取第一个部分并按空格分割
                    poses = []  # 存储位置坐标
                    for i in range(len(num) // 2):  # 假设每两个数是一个位置坐标 (x, y)
                        poses.append((float(num[i * 2]), float(num[i * 2 + 1])))  # 将坐标转换为浮点数并添加到 poses 列表
                    if len(line1) >= 5:
                        sounds = line1[4].split()  # 如果有声音参数，按空格分割为列表
                    self.pos.append((poses, int(line1[1]) if len(line1) >= 2 else 0,  # 伤害
                                     int(line1[2]) if len(line1) >= 3 else 0,  # 回血
                                     line1[3] if len(line1) >= 4 else '', sounds if len(line1) >= 5 else []))
                    # 将每个动作位置、帧数、描述和声音信息添加到 pos 列表中

    # 每调用一次 tick 方法，动作帧数加一，最大不超过动作的总帧数 - 1
    def tick(self):
        self.ticks = min(self.ticks + 1, len(self.pos) - 1)

    # 获取当前动作的位置（坐标、帧数、描述、声音等信息）
    def get_current_pos(self):
        return self.pos[self.ticks] if len(self.pos) > 0 else (None, 0, 0, '', [])

    # 判断动作是否结束（即 ticks 是否已到达动作的最后一帧）
    def is_end(self):
        return self.ticks == len(self.pos) - 1

    # 重置动作的帧数
    def reset(self):
        self.ticks = 0


# 以下是具体的动作实例，每个动作都通过文件初始化。
ATTACK_RIGHT = Action("attack_right", "./assets/actions/attack_right.txt")  # 右侧攻击动作
ATTACK_LEFT = Action("attack_left", "./assets/actions/attack_left.txt")  # 左侧攻击动作
ARROW_LEFT = Action("attack_left", "./assets/actions/arrow_left.txt")
TNT_RIGHT = Action("attack_left", "./assets/actions/tnt_right.txt")
ULTIMATE_RIGHT = Action("ultimate_right", "./assets/actions/ultimate_right.txt")  # 右侧终极技能动作
ESCAPE_LEFT = Action("escape_left", "./assets/actions/escape_left.txt")  # 左侧逃跑动作
LASER_CANNON_LEFT = Action("laser_cannon_left", "./assets/actions/laser_cannon_left.txt")
LIFE_STEAL_RIGHT = Action("live_steal_right", "./assets/actions/life_steal_right.txt")
EMPTY = Action("empty", None)  # 空的动作，没有对应的文件
