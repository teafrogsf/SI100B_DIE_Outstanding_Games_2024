<p align="center">
    <img src="icon.png" alt="Library of Redundancy" width="150">
</p>

### **愿您找到想要的书**

# Profile
## Project Name
Library of Redundancy
## Team Name
仿生阳不会梦见电子线代
## Personnel Information
- 丁瑞泽：
  - ID: 2024533127
  - GitHub: [@NH37](https://github.com/azaneNH37)
- 王旻昊：
  - ID: 2024533137
  - GitHub: [@bmwang](https://github.com/bmwangmh)
- 居然：
  - ID: 2024533131
  - GitHub: [@2Bpencil](https://github.com/Quality2Bpencil)
## Contribution
- [@NH37](https://github.com/azaneNH37)
  - 负责了整体架构的搭建，渲染部分的全部代码，肉鸽系统的实现以及LLM部分的思路构建（？），以及永远解不完的资源包（海澜之包舔三遍，每遍都有新发现），还有部分report的撰写
  - 负责模块：AudioSystem，AnimeSystem，Data，EventSystem，RenderSystem（它是最大的！），RougeSystem，SceneSystem,（GameControlSystem，GameDatamanager（其中一些（大部分）），GameInitialSetting，LLMStorage）
- [@bmwang](https://github.com/bmwangmh)
  - 负责了全部战斗数据部分的代码，以及本report的架构，以及~~并不~~勤劳的测试员？（但是在终端玩废墟图书馆真的很辛苦欸）
  - 负责模块：ReceptionSystem ~~（其中曾经有一个长达3k行的文件。）~~
- [@2Bpencil](https://github.com/Quality2Bpencil)
  - 负责了LLM部分的全部代码，以及勤劳（？）的测试员，以及部分美术资源的提取。哦对了，还有驯服llama3.2（事实上，一个3B的小模型还能干什么呢）。
  - 负责模块：LLMSystem（包含情感强烈的prompt部分）
# Environment Setting
### package
- python-3.11.10
- pygame-2.6.1 
- numpy-2.0.1
- openai-1.52.1
- spacy-3.8.2
- scikit-learn-1.5.2
### scikit-learn zh model
  - python -m spacy download zh_core_web_md
# Tutorial
**由于本项目较为复杂，详细教程请移步项目report #3.2后端**
### 你需要知道的操作
- 大部分操作可以通过鼠标左键解决，如果你觉得一个元素像个按钮，你就可以点点它
- 大地图中轻推WASD移动，商人交互游戏有提示 ~~（按F）~~，道路尽头一看就有个像敌人的东西（什么你不打算沿着路走？那祝你好运）（反正大地图不是游玩重点）
- 商店界面和选卡界面默认都是没有选中某个角色的，所以想要操作记得先选中一个角色哦
- 生成出来的卡不是全给你的，是要**三选一**的哦
- 战斗界面极简版：
  - 当每个回合开始时，你会发现角色头顶上的骰子会显示有（最小值-最大值），**拍第一下空格**之后速度骰的速度被确定，这个时候才可以开始进行选牌等操作
  - **拍第二下空格**后会直接进入战斗，不会有任何确认的选项（不會受到任何處分），致敬原作
  - 如果你不想手动操作选牌，在拍第一下空格后可以**按P键**，P键会尽可能为你没有选牌的速度骰子选卡
  - 如果想手动选牌，先**点击己方的某个速度骰**，该角色的手牌将显示，**选中手牌**，**点击敌方某个速度骰**，你就完成了一次选牌；取消选牌既可以**右键**一个已经拥有卡牌的速度骰，也可以在选牌过程中直接右键取消
# 想要展示的一些内容？

## 前有小兵?
<p align="center">
    <img src="MarkdownDisplay\001.png" width="700">
    <img src="MarkdownDisplay\002.png" width="700">
</p>

## 好看（？）的动画
<p align="center">
    <img src="MarkdownDisplay\003.png" width="700">
    <img src="MarkdownDisplay\004.png" width="700">
    <img src="MarkdownDisplay\005.png" width="700">
</p>

## 自由（？）的升级与强大（！）的天赋
<p align="center">
    <img src="MarkdownDisplay\006.png" width="700">
    <img src="MarkdownDisplay\007.png" width="700">
    <img src="MarkdownDisplay\008.png" width="700">
    <img src="MarkdownDisplay\009.png" width="700">
</p>

## 🚁🚁尊贵的坎诺特司书先生正在制作卡牌🚁🚁
<p align="center">
    <img src="MarkdownDisplay\010.png" width="700">
    <img src="MarkdownDisplay\011.png" width="700">
    <img src="MarkdownDisplay\012.png" width="700">
</p>

## 一些对原作品（们）的致敬和拙劣的模仿
<p align="center">
    <img src="MarkdownDisplay\014.png" width="700">
    <img src="MarkdownDisplay\015.png" width="700">
    <img src="MarkdownDisplay\016.png" width="700">
    <img src="MarkdownDisplay\017.png" width="700">
    <img src="MarkdownDisplay\018.png" width="700">
</p>

## 游戏内的制作组名单哦
<p align="center">
    <img src="MarkdownDisplay\013.png" width="700">
</p>

# 想要说的话？
- 本项目真的真的没有也不太有时间得到充分的测试（目前应该仅测了五六次全流程通关2h无bug），因此可能存在一些酒吧内点炒饭（包括LLM的不稳定性的因素）导致游戏崩了的现象，还请诸位老师和TA高抬贵手www，果咩捏果咩捏
- 考虑到是纯血pygame，可能游戏有部分效果体现的不是很好（指各种五毛特效）
- 游戏中塞了一点点彩蛋，可能会被碰巧发现？
- 本来每层中LLM生成卡是有次数限制的，但考虑到妮科的AI搓卡真的太~慢~了~，所以你可以无限制搓哦~
- 已知bug：游戏运行至后期时由于部分audio没有被正常释放，会导致部分音效无法正常表现（反正不会炸），但是没时间修了，所以不管了！（都怪测试员没听出来，哼）（但是效果真的会差一点，本来最后面两场画面表现都是最好的了呜呜呜）
- 以及在《Library of Redundancy》中玩的开心！
- (25.01.13 00:50) 因为有人被远程克隆蒙蔽了双眼，导致完全没有想到克隆本地仓库，浪费了1h和网络搏斗（躺 但是.git真的大啊 600M