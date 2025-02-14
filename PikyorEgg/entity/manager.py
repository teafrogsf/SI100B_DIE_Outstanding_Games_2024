
class EntityManager:
	def __init__(self):
		self.dic = {}
	
	def register(self, entityID: str, block: type):
		if entityID in self.dic:
			raise ValueError(f"注册一个已存在的实体ID: {entityID}")
		self.dic[entityID] = block
	
	def get(self, entityID: str):
		return self.dic[entityID]


class SkillManager:
	def __init__(self):
		self.dic = {}
	
	def register(self, skillID: int, skill: type):
		if skillID in self.dic:
			raise ValueError(f"注册一个已存在的技能ID: {skillID}")
		self.dic[skillID] = skill
		
	def get(self, skillID: int):
		return self.dic[skillID]


entityManager: EntityManager = EntityManager()
skillManager: SkillManager = SkillManager()
