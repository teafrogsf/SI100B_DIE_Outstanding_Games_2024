import math


# 定义一个数学函数，用于计算某个值的平方和
def f(x1):
    return (x1 - 375) ** 2 / 400 + 75


frames = 90  # 总帧数设置为 90

# 生成攻击动作（左侧）
with open("attack_left.txt", "w") as file:
    for i in range(frames):
        # 计算每一帧的位置，x 轴逐渐从 600 移动到接近 150
        x = 600 - (450 * i / frames)
        # 将计算的 x 和 y 值写入文件，其中 y 值由 f(x) 计算得到
        file.write(f"{x:.0f} {f(x):.0f}\n")
    # 添加攻击效果标记
    file.write("150 200|10|0||hit\n")
    # 继续写入从 150 到 600 的位置变化
    for i in range(frames // 2):
        x = 450 * i / frames * 2 + 150
        file.write(f"{x:.0f} 200\n")

# 生成攻击动作（右侧）
with open("attack_right.txt", "w") as file:
    for i in range(frames):
        # 计算每一帧的位置，x 轴逐渐从 150 移动到接近 600
        x = 450 * i / frames + 150
        # 将计算的 x 和 y 值写入文件，其中 y 值由 f(x) 计算得到
        file.write(f"{x:.0f} {f(x):.0f}\n")
    # 添加攻击效果标记
    file.write("600 200|10|0||hit\n")
    # 继续写入从 600 到 150 的位置变化
    for i in range(frames // 2):
        x = 600 - (450 * i / frames * 2)
        file.write(f"{x:.0f} 200\n")

with open("arrow_left.txt", "w") as file:
    file.write(f"600 200\n")
    file.write(f"600 200\n")
    file.write(f"600 200|0|0||arrow\n")
    for i in range(46):
        file.write(f"600 200\n")
    file.write(f"600 200|20|0||hit\n")
    for i in range(20):
        file.write(f"600 200\n")

with open("tnt_right.txt", "w") as file:
    file.write(f"150 200\n")
    file.write(f"150 200\n")
    file.write(f"150 200|0|0||tnt\n")
    for i in range(96):
        file.write(f"150 200\n")
    file.write(f"150 200|20|0||explosion hit\n")
    for i in range(50):
        file.write(f"150 200\n")

# 生成终极技能（右侧）
with open("ultimate_right.txt", "w") as file:
    # 生成初始的 10 帧，位置从 150 到 600 变化
    for x in range(10):
        file.write(f"{150 + 450 / 10 * x} 200\n")
    # 接下来 10 帧保持 600 位置不变
    for x in range(10):
        file.write(f"600 200\n")
    # 创建特殊效果的技能轨迹，生成 10 帧的轨迹坐标
    for x in range(10):
        file.write(f"{600 - 100 / 10 * x} {200 - 100 / 10 * x} {600 + 100 / 10 * x} {200 - 100 / 10 * x}"
                   f" {600 - 100 / 10 * x} {200 + 100 / 10 * x} {600 + 100 / 10 * x} {200 + 100 / 10 * x}"
                   f"|0|0|clone_tech|zeus\n")
    # 输出终极技能的范围
    file.write(f"500 100 700 100 500 300 700 300|60|0||zeus\n")
    # 生成 90 帧的技能范围，随着时间的推移，技能的范围逐渐增大
    for x in range(90):
        k = (math.sqrt(100 / 90) * x) ** 2
        file.write(f"{500 + k} {100 + k} {700 - k} {100 + k}"
                   f" {500 + k} {300 - k} {700 - k} {300 - k}|0|0|clone_tech\n")
    # 最后 40 帧的运动轨迹，x 从 600 逐渐变到 150
    for x in range(40):
        file.write(f"{600 - 450 / 40 * x} 200\n")

# 生成逃跑动作（左侧）
with open("escape_left.txt", "w") as file:
    # 生成 30 帧逃跑的轨迹，x 从 150 增加到 500
    for x in range(30):
        file.write(f"{150 + 350 / 30 * x} 200\n")
    # 生成接下来的 20 帧，位置保持在 500 处
    for x in range(20):
        file.write(f"500 200\n")
    # 生成 50 帧的动作标记，模拟角色在逃跑过程中的动作
    for x in range(50):
        file.write(f"500 200|0|0|mocking\n")
    # 最后 30 帧，x 从 500 逐渐变化到 150
    for x in range(30):
        file.write(f"{500 - 550 * x / 25:.0f} 200\n")

with open("laser_cannon_left.txt", "w") as file:
    for x in range(49):
        file.write(f"600 200\n")
    file.write("600 200|20|0||hit\n")
    for x in range(40):
        file.write(f"600 200\n")

with open("life_steal_right.txt", "w") as file:
    for i in range(10):
        for x in range(9):
            file.write(f"150 200|0|0|life_steal\n")
        file.write(f"150 200|27|0|life_steal|heart\n")
    for i in range(10):
        for x in range(9):
            file.write(f"150 200|0|0|life_steal\n")
        file.write(f"150 200|0|10|life_steal|heart\n")
