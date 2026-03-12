import KBEngine

import KBEUtil
from KBEDebug import *
import Math


class Motion(KBEngine.EntityComponent):
	"""
	负责运动的组件
	"""

	def __init__(self):
		KBEngine.EntityComponent.__init__(self)
		DEBUG_MSG("Motion::__init__: created entityID = %i, dict = %s ." % ( self.ownerID, self.__dict__))

	def randomWalk(self, basePos,radius):
		"""
		随机移动entity
		"""

		if self.isMoving:
			return False

		# 移动半径距离在30米内
		if self.canNavigate():
			destPos = self.owner.getRandomPoints(basePos, radius, 1, 0)
			if len(destPos) == 0:
				return False
			destPos = destPos[0]
		else:
			destPos = KBEUtil.getRandomPointInRadius(basePos, radius)

		self.gotoPosition(destPos)

		return True


	def gotoPosition(self, position, dist=0.0):
		"""
		移动到某个位置
		:param position:Vector3, 目标位置点
		:param dist: float, 达到多少距离则判定为到达
		:return:
		"""
		if self.moveSpeed <= 0:
			ERROR_MSG("Motion::gotoPosition: moveSpeed <= 0")
			return

		if self.isMoving:
			self.stopMotion()

		if self.owner.position.distTo(position) <= 0.05:  # 阈值0.05，如果小于，则不进行移动
			return

		self.isMoving = True
		speed = self.moveSpeed

		if self.owner.canNavigate():
			DEBUG_MSG("Motion(%s[%i])::gotoPosition: canNavigate=True" % (self.owner.__class__.__name__, self.ownerID))
			self.owner.navigate(Math.Vector3(position), speed, dist, speed, 512.0, True, 0, None)
		else:
			if dist > 0.0:
				dest_pos = Math.Vector3(position) - self.position
				dest_pos.normalise()
				dest_pos *= dist
				dest_pos = position - dest_pos
			else:
				dest_pos = Math.Vector3(position)

			WARNING_MSG("Motion(%s[%i])::gotoPosition: canNavigate=False" % (self.owner.__class__.__name__, self.ownerID))

			self.owner.moveToPoint(dest_pos, speed, 0, None, True, False)


	def stopMotion(self):
		"""
		停止移动
		:return:
		"""
		if self.isMoving:
			self.owner.cancelController("Movement")
			self.isMoving = False


	def onAttached(self, owner):
		"""
		组件被附加到Entity时激发
		:param owner: 组件拥有者
		:return:
		"""
		INFO_MSG("Motion(%s[%i])::onAttached" % (self.owner.__class__.__name__, self.ownerID))


	def onDetached(self, owner):
		"""
		组件从Entity上移除时激发
		:param owner:组件拥有者
		:return:
		"""
		INFO_MSG("Motion(%s[%i])::onDetached" % (self.owner.__class__.__name__, self.ownerID))


	def onMove(self, controllerId, userarg):
		"""
		当owner回调onMove时调用本组件的方法
		:param controllerId:
		:param userarg:
		:return:
		"""
		DEBUG_MSG("Motion::onMove: %i controllerId =%i, userarg=%s ,position=%s" % (self.owner.id, controllerId, userarg,self.owner.position))
		self.isMoving = True


	def onMoveFailure(self, controllerId, userarg):
		"""
		当owner回调onMoveFailure时调用本组件的方法
		使用引擎的任何移动相关接口， 在entity一次移动失败时均会调用此接口
		"""
		ERROR_MSG(
			"Motion(%s[%i])::onMoveFailure: controllerId =%i, userarg=%s" % (
				self.owner.__class__.__name__, self.ownerID, controllerId, userarg))

		self.isMoving = False


	def onMoveOver(self, controllerId, userarg):
		"""
		当owner回调onMoveOver时调用本组件的方法
		使用引擎的任何移动相关接口， 在entity移动结束时均会调用此接口
		"""
		self.isMoving = False