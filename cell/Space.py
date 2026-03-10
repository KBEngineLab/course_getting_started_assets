import KBEngine

import GlobalDefine
from KBEDebug import DEBUG_MSG
from data import d_npcs
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

		self.addTimer(1, 0.1, GlobalDefine.TIMER_TYPE_NPC_CREATE)

	def loginToSpace(self,avatarEntity):
		DEBUG_MSG("Space::loginToSpace: spaceId: %i" % self.spaceID)
		avatarEntity.createCell(self)

	def onDestroy(self):
		DEBUG_MSG("Space::onDestroy: spaceId: %i" % self.spaceID)
		spaces = KBEngine.globalData["spaces"]
		del spaces["space_%i" % self.id]
		KBEngine.globalData["spaces"] = spaces

	def onTimer(self, timerHandle, userData):
		DEBUG_MSG("Space::onTimer: tid=%i, userData=%i" % (timerHandle, userData))

		if userData == GlobalDefine.TIMER_TYPE_NPC_CREATE:
			self.createNPC(timerHandle)


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
			"moveSpeed": npc["moveSpeed"],
			"dialog": npc["dialog"],
		}
		KBEngine.createEntity("NPC",self.spaceID,npc["position"],npc["direction"],params)

		# for key,item in d_npcs.data.items():

