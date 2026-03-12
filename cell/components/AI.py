import KBEngine

import GlobalDefine
from KBEDebug import *


class AI(KBEngine.EntityComponent):
	"""
	负责怪物AI的组件
	"""

	def __init__(self):
		KBEngine.EntityComponent.__init__(self)
		DEBUG_MSG("AI::__init__: created entityID = %i, dict = %s ." % ( self.ownerID, self.__dict__))

		self.addTimer(1, 0.1, GlobalDefine.TIMER_TYPE_AI_HEARTBEAT)

	def onTimer(self, timerHandle, userData):
		if userData == GlobalDefine.TIMER_TYPE_AI_HEARTBEAT:
			if self.state == GlobalDefine.ENTITY_STATE_FREE:
				# 常规状态，这个状态下可以随机移动
				pass
			elif self.state == GlobalDefine.ENTITY_STATE_FIGHT:
				# 战斗状态
				pass
			else:
				# 其他状态，自行扩展
				pass




	def onThinkFree(self):
		"""
		virtual method.
		闲置时think
		"""


	def onThinkFight(self):
		"""
		virtual method.
		战斗时think
		"""