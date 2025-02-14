# PikyorEgg队的成员分工

- 施云翀  游戏基底及大部分基础逻辑、游玩体验优化、附加功能；
- 马嘉欣  游戏实现的代码设计、玩家、敌人等的具体实现；音乐搜集、音乐音效播放模块实现；AI交互实现；
- 徐奕  所有艺术设计；游戏玩法、流程、文案设计；游戏文案窗口相关的代码具体实现。

# 使用说明

- 运行方式：
  - python运行main.py文件。
- 生成文件：
  - 根据游戏需要，会生成user文件夹，其中包含一个config.json文件和一个archive文件夹。
  - config.json文件保存了所有游戏设置。
  - archive文件夹保存了所有游戏存档。其中，每一个文件都是单独的存档；去掉.json后缀就是存档名。

# 游戏玩法

- 操作你的小鸡，在危险中成长，习得技能，突破极限，孵出小鸡！
- 如需指引，可将鼠标放到临近实体上，或Enter向ai系统询问
- 如遇地图分离过不去的情况，或使用闪现技，或重开即可，视为类Minecraft地图生成特性

# 游戏操作

- 人物移动 WASD
- 状态面板 E
- 任务面板 Tab
- 暂停并打开暂停菜单 Esc
- 询问AI游戏助手 Enter
- 锁定/解锁视角 Space
- 做窝 H
- 选定公鸡/下蛋 R
- 选定主动技能/选定后按相同键使用 1~6数字键
- 取消选定技能 右键或相同数字键
- 移动视角 中键按住拖动
- 缩放地图 滚轮
- 作弊按键 Q
- 特殊地，在最后的蛋蛋工厂，你需要鼠标左键拖动其中的词条填充右侧的5个槽位，让AI绘制独属于你的鸡蛋。

# 文件

- assets/ 所有静态图像、声音资源
- block/ 方块相关逻辑
  - block.py 所有的方块类和子类
  - manager.py 方块资源管理器，将方块类和方块ID一一对应，减少循环import、局部import
- entity/ 实体相关逻辑
  - active_skill.py 所有主动技能类
  - enemy.py 所有敌对生物类
  - entity.py 实体基类，及玩家、蛋等末端实体类
  - manager.py 实体资源管理器，将实体类和实体ID一一对应，减少循环import、局部import
  - skill.py 技能基类及所有被动技能类
- interact/ 玩家交互逻辑
  - interacts.py 所有玩家交互信息
  - status.py 状态类，用于保存和简化处理玩家交互信息
- item/ 道具，已弃用
- LLA/ AI交互逻辑
- music/ 声音、音效
  - music.py 音像资源管理器
- render/ 渲染逻辑
  - font.py 管理所有字体资源
  - renderable.py 渲染基类，及所有可渲染对象
  - renderer.py 渲染器
  - resource.py 管理纹理图片资源
- save/ 存档逻辑
  - configs.py 处理游戏配置文件，保存玩家设置
  - save.py 处理游戏存档数据
- user/ 玩家信息。由游戏自动生成，首次运行前不存在
  - archive/ 所有存档文件和鸡蛋位图
  - config.json 游戏配置文件
- utils/ 所有工具模块和类工具模块
  - util.py 日志、报错信息优化
  - element.py 游戏元素基类。与Item协作，现可弃用
  - error.py 游戏内定义的错误类
  - game.py 游戏框架逻辑，游戏管理器
  - sync.py 用于防止多线程数据冲突造成游戏进行不协调
  - text.py RenderableString类，简化文本渲染流程
  - vector.py 向量类，提高位置计算相关代码可读性和流程
- window/ 窗口相关逻辑
  - hud.py HUD类，在游戏中实时现实游戏信息，包括血条、成长值、文字提示等
  - ingame.py 游戏内窗口，包括状态窗口、任务窗口等
  - input.py 输入窗口，主要包含AI助手窗口
  - widget.py 窗口按钮
  - window.py 窗口基类，及开始窗口等游戏流程外窗口；鼠标浮窗
- world/ 游戏世界（即场景）相关逻辑
  - world.py 所有世界（场景）类
- main.py 游戏入口点
