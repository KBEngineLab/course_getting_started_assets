
import KBEngine
from KBEDebug import *
from Space import Space
from data import d_spaces
import Functor


class SpaceMgr(KBEngine.Entity):
	"""
	这是一个空间管理器，当首个baseapp启动时创建此管理器，并创建所有的space
	"""

	def __init__(self):
		KBEngine.Entity.__init__(self)
		self.spaces = {}
		self.spaceInfoMap = d_spaces.datas


		# 向全局共享数据中注册这个管理器的entityCall以便在所有逻辑进程中可以方便的访问
		# 但需要注意，只有在同一个app中访问SpaceMgr，才会有返回值，其他app均为远程调用，无返回值
		KBEngine.globalData["SpaceMgr"] = self

		self.createSpace(self.spaceInfoMap)

	def loginToSpace(self,avatarEntity,spaceKey):
		"""
		登录到某个Space
		"""
		spaceBase:Space = self.spaces[spaceKey]
		spaceBase.cell.loginToSpace(avatarEntity)

	def createSpace(self,spaceInfoMap):
		for key, space in spaceInfoMap.items():
			DEBUG_MSG("SpaceMgr::createSpace: spaceKey:[%s] ,spaceInfo:[%s]" % (key,space))
			KBEngine.createEntityAnywhere(space["spaceType"],{"spaceKey":key}, Functor.Functor(self.onSpaceCreated,key))

	def onSpaceCreated(self,spaceKey, space):
		"""
		一个space创建好后的回调
		"""
		DEBUG_MSG("Spaces::onSpaceCreated: spaceKey:%s entityID=%i" % (spaceKey,space.id))
		self.spaces[spaceKey] = space


	def onSpaceLoseCell(self, spaceKey):
		"""
		space的cell失效了，从Space里触发
		"""
		del self.spaces[spaceKey]

	def onSpaceGetCell(self, spaceEntityCall, spaceKey):
		"""
		space的cell创建好了，从Space里触发
		"""
		DEBUG_MSG("Spaces::onSpaceGetCell: space %s. spaceId=%i" % (spaceKey, spaceEntityCall.id))


