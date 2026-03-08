import KBEngine

from KBEDebug import DEBUG_MSG


class Space(KBEngine.Space):
	"""
	Space的cell部分。
	"""

	def __init__(self):
		KBEngine.Space.__init__(self)
		spaces = KBEngine.globalData["spaces"] if "spaces" in KBEngine.globalData["spaces"] else {}
		spaces["space_%i" % self.id] = self.base
		KBEngine.globalData["spaces"] = spaces
		pass

	def loginToSpace(self,avatarEntity):
		avatarEntity.createCellEntity(self.cell)

	def onDestroy(self):
		DEBUG_MSG("Space::onDestroy: spaceId: %i" % self.id)
		spaces = KBEngine.globalData["spaces"]
		del spaces["space_%i" % self.id]
		KBEngine.globalData["spaces"] = spaces