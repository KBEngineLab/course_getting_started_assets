import random

import KBEngine

import GlobalDefine
from KBEDebug import *
from data import d_npcs


class Avatar(KBEngine.Entity):
	"""
	Avatar的cell部分
	"""
	def __init__(self):
		KBEngine.Entity.__init__(self)

	def useSkill(self, exposed, arg_targetID, arg_skillID):
		"""
		攻击，这里我们默认arg_skillID为1，即为普通攻击，伤害为5-20
		"""

		if exposed != self.id:
			return


		target = KBEngine.entities.get(arg_targetID)
		if target is None:
			ERROR_MSG("Avatar::useSkill(%i):targetID=%i not found" % (self.id, arg_targetID))
			return

		damage = random.randint(5, 20)
		target.recvDamage(self.id,arg_skillID, damage)
		# target.HP -= damage
		#
		# if target.HP <= 0:
		# 	target.HP = 0
		# 	target.state = 1



	def recvDamage(self, arg_attackerID, arg_skillID, arg_damage):
		"""
		受到攻击
		"""
		DEBUG_MSG("Avatar::recvDamage: %i, %i, %i" % (self.id, arg_attackerID, arg_damage))
		if arg_attackerID == self.id:
			return

		hp = self.HP - arg_damage
		if hp > 0:
			self.HP = hp
		else:
			self.HP = 0

		self.checkState()

	def checkState(self):
		if self.HP <= 0:
			self.die()

	def die(self):
		self.HP = 0
		self.MP = 0
		self.state = GlobalDefine.ENTITY_STATE_DEAD

	def relive(self, exposed):
		"""
		复活
		"""
		if exposed != self.id:
			return

		if self.HP <= 0:
			DEBUG_MSG("Avatar::relive: %i" % self.id)
			self.setHP(self.HP_Max)
			self.setMP(self.MP_Max)
			self.state = GlobalDefine.ENTITY_STATE_FREE

	def jump(self, exposed):
		"""跳跃"""

		if exposed != self.id:
			return

		DEBUG_MSG("Avatar::jump: %i" % self.id)

		self.otherClients.onJump()

	def setHP(self, arg_INT32):
		self.HP = arg_INT32

	def setMP(self, arg_INT32):
		self.MP = arg_INT32

	def setHPMax(self, arg_INT32):
		self.HP_Max = arg_INT32

	def setMPMax(self, arg_INT32):
		self.MP_Max = arg_INT32

	def dialog(self, exposed, arg_entityID, arg_EID):
		if exposed != self.id:
			return

		entity = KBEngine.entities.get(arg_entityID)
		if entity is None:
			ERROR_MSG("Avatar::dialog(%i):entityID=%i not found" % (self.id, arg_entityID))
			return
		DEBUG_MSG("Avatar::dialog: %i" % self.id)

		spaceKey = KBEngine.globalData["spaces"]["space_%i" % self.spaceID]["space_key"]
		npcs = d_npcs.data.get(spaceKey, None)
		if npcs is None or arg_EID not in npcs:
			ERROR_MSG("Avatar::dialog(%i):space=%s not found" % (self.id, spaceKey))
			return

		self.client.onDialog(arg_entityID,npcs[arg_EID]["dialog"][random.randint(0,len(npcs[arg_EID]["dialog"]) - 1)])










