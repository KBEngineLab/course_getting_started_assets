import random

import KBEngine

from KBEDebug import DEBUG_MSG


class NPC(KBEngine.Entity):

	def __init__(self):
		KBEngine.Entity.__init__(self)
		DEBUG_MSG("NPC::__init__: created entityID = %i, spaceID = %s ,name = %s ." % ( self.id, self.spaceID,self.name))

	def onEnterWorld(self):
		"""
		KBEngine method.
		如果实体非客户端控制实体，则表明实体进入了服务端上客户端控制的实体的View范围，此时客户端可以看见这个实体了。
		如果实体是客户端控制的实体则表明该实体已经在服务端创建了cell并进入了space。
		"""
		DEBUG_MSG("%s::onEnterWorld: %i" % (self.__class__.__name__, self.id))

	def onLeaveWorld(self):
		"""
		KBEngine method.
		如果实体非客户端控制实体，则表明实体离开了服务端上客户端控制的实体的View范围，此时客户端看不见这个实体了。
		如果实体是客户端控制的实体则表明该实体已经在服务端销毁了cell并离开了space。
		"""
		DEBUG_MSG("%s::onLeaveWorld: %i" % (self.__class__.__name__, self.id))

	def onMove(self, controllerId, userarg):
		"""
		KBEngine method.
		使用引擎的任何移动相关接口， 在entity一次移动完成时均会调用此接口
		"""
		DEBUG_MSG("%s::onMove: %i controllerId =%i, userarg=%s" % \
		          (self.__class__.__name__, self.id, controllerId, userarg))
		pass

	def onMoveFailure(self, controllerId, userarg):
		"""
		KBEngine method.
		使用引擎的任何移动相关接口， 在entity一次移动完成时均会调用此接口
		"""
		DEBUG_MSG("%s::onMoveFailure: %i controllerId =%i, userarg=%s" % \
		          (self.__class__.__name__, self.id, controllerId, userarg))

	def onMoveOver(self, controllerId, userarg):
		"""
		KBEngine method.
		使用引擎的任何移动相关接口， 在entity移动结束时均会调用此接口
		"""
		DEBUG_MSG("%s::onMoveOver: %i controllerId =%i, userarg=%s" % \
						(self.__class__.__name__, self.id, controllerId, userarg))
		pass