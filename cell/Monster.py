import random

import KBEngine

import GlobalDefine
from KBEDebug import DEBUG_MSG


class Monster(KBEngine.Entity):
	"""
	Monster的cell部分
	"""

	def __init__(self):
		KBEngine.Entity.__init__(self)
		DEBUG_MSG("Monster::__init__: created entityID = %i, spaceID = %s , position = %s." % (self.id, self.spaceID,self.position))

	def recvDamage(self, arg_attackerID, arg_skillID, arg_damage):
		"""
		受到攻击
		"""
		if arg_attackerID == self.id:
			return

		self.HP -= arg_damage

		if self.HP <= 0:
			self.HP = 0
			self.MP = 0
			self.state = GlobalDefine.ENTITY_STATE_DEAD

	def setHP(self, arg_INT32):
		self.HP = arg_INT32

	def setMP(self, arg_INT32):
		self.MP = arg_INT32

	def setHPMax(self, arg_INT32):
		self.HP_Max = arg_INT32

	def setMPMax(self, arg_INT32):
		self.MP_Max = arg_INT32

	def onDestroy(self):
		# KBEngine.entities.get(self.spaceID)
		space = KBEngine.globalData["space_%i" % self.spaceID]
		if space:
			space["call"].cell.onEntityDestroyed(self.eid)