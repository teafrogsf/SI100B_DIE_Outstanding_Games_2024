import json


class Dialog:

    def __init__(self, filename: str):
        self.filename = './assets/dialogs/' + filename + '.json'
        self.dialogs = {}
        self.current = None
        self.load()

    def load(self):
        # 从 JSON 文件加载对话数据
        with open(self.filename, 'r') as f:  # 打开对话文件
            data = json.load(f)  # 读取文件中的数据
            self.dialogs = data['data']  # 将 'data' 部分加载到 dialogs 字典中
            self.current = self.dialogs[data['start']]  # 设置当前对话为起始对话

    def next(self, choice: int):
        nxt = self.current['player'][choice]['next']
        if nxt[0] == '!':
            return nxt[1:]
        self.current = self.dialogs[nxt]
        return self.current


'''
{
  "start": "1",
  "data": {
    "1": {
      "npc": "nether_npc2_dia1",
      "player": [
        {
          "str": "nether_player2_dia1",
          "next": "2"
        }
      ]
    },
    "2": {
      "npc": "nether_npc2_dia2",
      "player": [
        {
          "str": "nether_player2_dia2",
          "next": "!1"
        }
      ]
    }
  }
}
'''