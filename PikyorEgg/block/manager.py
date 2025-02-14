
class BlockManager:
	def __init__(self):
		self.dic = {}
		
	def register(self, blockID: str, block: type):
		if blockID in self.dic:
			raise ValueError(f"注册一个已存在的方块ID: {blockID}")
		self.dic[blockID] = block
	
	def get(self, blockID: str):
		return self.dic[blockID]


blockManager: BlockManager = BlockManager()
