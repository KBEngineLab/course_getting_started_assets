import KBEngine
from KBEDebug import *
import Math


class Motion(KBEngine.EntityComponent):
	"""
	负责运动的组件
	"""

	def __init__(self):
		KBEngine.EntityComponent.__init__(self)
		DEBUG_MSG("Motion::__init__: created entityID = %i, dict = %s ." % ( self.ownerID, self.__dict__))




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
