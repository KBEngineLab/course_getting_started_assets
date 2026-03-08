import random

import KBEngine

from KBEDebug import *


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


		target:Avatar = KBEngine.entities.get(arg_targetID)
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
		if arg_attackerID == self.id:
			return

		self.HP -= arg_damage

		if self.HP <= 0:
			self.HP = 0
			self.state = 1


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









