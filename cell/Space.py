import math
import random

import KBEngine

import GlobalDefine
import KBEUtil
from KBEDebug import DEBUG_MSG
from data import d_npcs, d_monsters_spawnpoints
import copy

class Space(KBEngine.Space):
	"""
	Space的cell部分。
	"""

	def __init__(self):
		KBEngine.Space.__init__(self)
		DEBUG_MSG("Space::__init__: created space entityID = %i, spaceKey = %s." % ( self.id, self.cellSpaceKey))

		spaces = KBEngine.globalData["spaces"] if "spaces" in KBEngine.globalData else {}
		spaces["space_%i" % self.spaceID] = {
			"call":self.base,
			"space_key":self.cellSpaceKey,
		}
		KBEngine.globalData["spaces"] = spaces

		self.tempCreateNPCs = copy.deepcopy(d_npcs.data.get(self.cellSpaceKey, None))
		self.tempCreateMonsters = copy.deepcopy(d_monsters_spawnpoints.data.get(self.cellSpaceKey, None))

		# monsters需要持续创建，所以这里保存下来，当entity被销毁后，重新创建
		self.monsters = {}
		# 先重置monster数量
		for key,item in self.tempCreateMonsters.items():
			self.monsters[key] = 0

		DEBUG_MSG("Space::__init__: monsters create count: %s" % self.monsters)

		self.addTimer(1, 0.1, GlobalDefine.TIMER_TYPE_NPC_CREATE)
		self.addTimer(1, 0.5, GlobalDefine.TIMER_TYPE_MONSTER_CREATE)

	def loginToSpace(self,avatarEntity):
		DEBUG_MSG("Space::loginToSpace: spaceId: %i" % self.spaceID)
		avatarEntity.createCell(self)

	def onDestroy(self):
		DEBUG_MSG("Space::onDestroy: spaceId: %i" % self.spaceID)
		spaces = KBEngine.globalData["spaces"]
		del spaces["space_%i" % self.id]
		KBEngine.globalData["spaces"] = spaces

	def onTimer(self, timerHandle, userData):
		# DEBUG_MSG("Space::onTimer: tid=%i, userData=%i" % (timerHandle, userData))

		if userData == GlobalDefine.TIMER_TYPE_NPC_CREATE:
			self.createNPC(timerHandle)

		if userData == GlobalDefine.TIMER_TYPE_MONSTER_CREATE:
			self.createMonster(timerHandle)


	def createMonster(self,tid):
		"""
		创建Monster
		"""
		for key,item in self.tempCreateMonsters.items():
			# 如果已经创建了，则跳过
			if self.monsters[key] >= item["createCount"]:
				continue


			DEBUG_MSG("Space::createMonster: %s" % item)

			params = {
				"eid":key,
				"name": item["name"],
				"moveSpeed": item["moveSpeed"],
				"attack": item["attack"],
				"HP": item["HP"],
				"MP": item["MP"],
				"HP_Max": item["HP_Max"],
				"MP_Max": item["MP_Max"],
				"territoryArea":item["territoryArea"],
				"motion":{
					"moveSpeed":item["moveSpeed"]
				},
			}

			KBEngine.createEntity("Monster",self.spaceID,KBEUtil.getRandomPointInRadius(item["spawnPoints"],30),(0.0,0.0,0.0),params)

			self.monsters[key] += 1

			# 直接return，把创建分摊到每个时钟周期
			return

	def createNPC(self,tid):

		if self.tempCreateNPCs is None or len(self.tempCreateNPCs) <= 0:
			self.delTimer(tid)
			return


		key = list(self.tempCreateNPCs.keys())[0]
		npc = self.tempCreateNPCs.pop(key)

		DEBUG_MSG("Space::createNPC: %s" % npc)
		params = {
			"eid":key,
			"name": npc["name"],
			"dialog": npc["dialog"],
			"motion":{
				"moveSpeed":npc["moveSpeed"]
			}
		}
		KBEngine.createEntity("NPC",self.spaceID,npc["position"],npc["direction"],params)

		# for key,item in d_npcs.data.items():

	def onEntityDestroyed(self, arg_UNICODE):
		DEBUG_MSG("Space::onEntityDestroyed: %s" % arg_UNICODE)
		self.monsters[arg_UNICODE] -= 1

		if self.monsters[arg_UNICODE] <= 0:
			self.monsters[arg_UNICODE] = 0

