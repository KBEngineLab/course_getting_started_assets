import KBEngine
import copy
from KBEDebug import *

class Avatar(KBEngine.Entity):
	def __init__(self):
		KBEngine.Entity.__init__(self)
		DEBUG_MSG("Avatar::__init__:%s." % (self.__dict__))

	def onEnterSpace(self):
		"""
		KBEngine method.
		这个entity进入了一个新的space
		"""
		DEBUG_MSG("%s::onEnterSpace: %i" % (self.__class__.__name__, self.id))

	def onLeaveSpace(self):
		"""
		KBEngine method.
		这个entity将要离开当前space
		"""
		DEBUG_MSG("%s::onLeaveSpace: %i" % (self.__class__.__name__, self.id))


	def onJump(self):
		DEBUG_MSG("%s::onJump: %i" % (self.__class__.__name__, self.id))
