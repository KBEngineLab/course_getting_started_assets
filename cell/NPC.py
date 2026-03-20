import random

import KBEngine

import GlobalDefine
import KBEUtil
from KBEDebug import DEBUG_MSG


class NPC(KBEngine.Entity):
	"""
	NPC的cell部分
	"""

	def __init__(self):
		KBEngine.Entity.__init__(self)
		DEBUG_MSG("NPC::__init__: created entityID = %i, spaceID = %s." % ( self.id, self.spaceID))

		if self.motion.moveSpeed > 0:
			# 5s 移动一次
			self.addTimer(1, 10, GlobalDefine.TIMER_TYPE_NPC_MOVE)

	def onTimer(self, timerHandle, userData):
		if userData == GlobalDefine.TIMER_TYPE_NPC_MOVE:
			self.motion.randomWalk(self.position, 10)





