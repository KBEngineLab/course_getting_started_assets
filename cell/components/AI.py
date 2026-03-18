import random
import time

import KBEngine

import GlobalDefine
from Avatar import Avatar
from KBEDebug import *
from components.Motion import Motion


class AI(KBEngine.EntityComponent):
	"""
	负责怪物AI的组件
	依赖Motion组件
	"""

	def __init__(self):
		KBEngine.EntityComponent.__init__(self)
		DEBUG_MSG("AI(%s[%i])::__init__: created dict = %s ." % (self.owner.__class__.__name__, self.ownerID, self.__dict__))

		if self.owner.motion is None:
			ERROR_MSG("AI(%s[%i])::__init__:  has no motion component!" % (self.owner.__class__.__name__, self.ownerID))
			return

		# 下次移动时间
		self.nextMoveTime = 0

		# 下次攻击时间,cd你可以写进配置里，这里我们默认为2s
		self.nextAttackTime = 0

		# 敌人列表
		self.enemyList = []
		self.territoryControllerID = 0

		self.addTimer(1, 0.1, GlobalDefine.TIMER_TYPE_AI_HEARTBEAT)

	def addTerritory(self):
		"""
		添加领地
		进入领地范围的某些entity将视为敌人
		"""
		assert self.territoryControllerID == 0 and "territoryControllerID != 0"
		trange = self.owner.territoryArea / 2.0
		self.territoryControllerID = self.owner.addProximity(trange, 0, 0)

		if self.territoryControllerID <= 0:
			ERROR_MSG("AI(%s[%i])::addTerritory: range=%i, is error!" % (self.owner.__class__.__name__, self.ownerID, trange))
		else:
			DEBUG_MSG("AI(%s[%i])::addTerritory:range=%i, id=%i." % (self.owner.__class__.__name__, self.ownerID, trange, self.territoryControllerID))

	def delTerritory(self):
		"""
		删除领地
		"""
		if self.territoryControllerID > 0:
			self.owner.cancelController(self.territoryControllerID)
			self.territoryControllerID = 0
			DEBUG_MSG("AI(%s[%i])::::delTerritory" % (self.owner.__class__.__name__, self.ownerID, ))

	def onEnterTrap(self, entityEntering, rangeXZ, rangeY, controllerID, userArg=0):
		"""
		KBEngine method.
		有entity进入trap
		"""

		if controllerID != self.territoryControllerID:
			return

		if entityEntering.isDestroyed or entityEntering.__class__.__name__ != "Avatar" or entityEntering.state == GlobalDefine.ENTITY_STATE_DEAD:
			return

		if  self.owner.state != GlobalDefine.ENTITY_STATE_FREE:
			return

		if entityEntering.id in self.enemyList:
			return


		DEBUG_MSG("AI(%s[%i])::onEnterTrap:entityEntering=(%s)%i, range_xz=%s, range_y=%s, controllerID=%i, userarg=%i" %  (self.owner.__class__.__name__, self.ownerID,  entityEntering.__class__.__name__, entityEntering.id, rangeXZ, rangeY, controllerID, userArg))

		self.enemyList.append(entityEntering.id)
		if self.owner.state != GlobalDefine.ENTITY_STATE_FIGHT:
			self.owner.state = GlobalDefine.ENTITY_STATE_FIGHT

	def onLeaveTrap(self, entityLeaving, rangeXZ, rangeY, controllerID, userArg=0):
		"""
		KBEngine method.
		有entity离开trap
		"""
		if controllerID != self.territoryControllerID:
			return

		if entityLeaving.__class__.__name__ != "Avatar" :
			return

		if entityLeaving.id in self.enemyList:
			self.enemyList.remove(entityLeaving.id)

		DEBUG_MSG("AI(%s[%i])::onLeaveTrap: entityLeaving=(%s)%i." % (self.owner.__class__.__name__, self.ownerID, entityLeaving.__class__.__name__, entityLeaving.id))


	def onTimer(self, timerHandle, userData):
		if userData == GlobalDefine.TIMER_TYPE_AI_HEARTBEAT:
			if self.owner.state == GlobalDefine.ENTITY_STATE_FREE:
				# 常规状态，这个状态下可以随机移动
				self.onThinkFree()

			elif self.owner.state == GlobalDefine.ENTITY_STATE_FIGHT:
				# 战斗状态
				self.onThinkFight()

			elif self.owner.state == GlobalDefine.ENTITY_STATE_DEAD:
				# 死亡
				self.delTimer(timerHandle)
			else:
				# 其他状态，自行扩展
				pass




	def onThinkFree(self):
		"""
		virtual method.
		闲置时think
		"""
		# 闲置时创建一个触发器
		if self.territoryControllerID <= 0:
			self.addTerritory()

		# 闲置时，有可能有玩家复活了，所以这里要检查一下
		for _id in self.enemyList:
			item = KBEngine.entities.get(_id)
			if item is None:
				self.enemyList.remove(_id)
				continue
			if item.isDestroyed:
				self.enemyList.remove(item.id)
				continue
			if item.state == GlobalDefine.ENTITY_STATE_DEAD:
				continue
			# 进入战斗
			self.owner.state = GlobalDefine.ENTITY_STATE_FIGHT
			break


		motion:Motion = self.owner.motion

		if motion.isMoving:
			return False

		if time.time() < self.nextMoveTime:
			return False

		res = motion.randomWalk(self.owner.position, 10)
		if res:
			self.nextMoveTime =  int(time.time() + random.randint(5, 15))
		else:
			return False

		return True

	def onThinkFight(self):
		"""
		virtual method.
		战斗时think
		"""

		if self.territoryControllerID > 0:
			self.delTerritory()


		# 如果仇恨列表为空
		if len(self.enemyList) <= 0:
			self.owner.state = GlobalDefine.ENTITY_STATE_FREE
			return


		entity = None

		for _id in self.enemyList:
			item = KBEngine.entities.get(_id)
			if item is None:
				self.enemyList.remove(_id)
				continue
			if item.isDestroyed:
				self.enemyList.remove(item.id)
				continue
			if item.state == GlobalDefine.ENTITY_STATE_DEAD:
				continue

			entity = item
			break


		# 如果没有获取到entity，就重置状态
		if entity is None:
			self.owner.state = GlobalDefine.ENTITY_STATE_FREE
			return

		# KBEngine.entities.get(self.enemyList[0])


		# if entity is None:
		# 	self.enemyList.remove(entityId)
		# 	return

		# if entity.isDestroyed :
		# 	self.enemyList.remove(entity.id)
		# 	return

		#or entity.state == GlobalDefine.ENTITY_STATE_DEAD

		entity.checkState()

		if entity.state == GlobalDefine.ENTITY_STATE_DEAD:
			return



		# 当两者间的距离大于15后移除，当然，你也可以设置一个原点，让entity回到原点
		if entity.position.distTo(self.owner.position) > 15:
			self.enemyList.remove(entity.id)
			return


		# 这里假设攻击距离是2
		attackMaxDist = 2

		if entity.position.distTo(self.owner.position) > attackMaxDist:
			# 追敌
			self.owner.motion.gotoPosition(entity.position, attackMaxDist - 0.2)
			return
		else:
			# 攻击
			if time.time() < self.nextAttackTime:
				return
			entity.recvDamage(self.owner.id,1,self.owner.attack)
			self.nextAttackTime = int(time.time() + 2)
			pass

		DEBUG_MSG("AI(%s[%i])::onThinkFight: enemyList=%s" % (self.owner.__class__.__name__, self.ownerID,len(self.enemyList)))