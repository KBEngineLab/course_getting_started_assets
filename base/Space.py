import KBEngine

class Space(KBEngine.Space):
	"""
    Space的base部分，
    注意：它是一个实体，并不是真正的space，真正的space存在于cellapp的内存中，通过这个实体与之关联并操控space。
    """

	def __init__(self):
		KBEngine.Space.__init__(self)
		self.cellData["cellSpaceKey"] = self.spaceKey


	def onLoseCell(self):
		KBEngine.globalData["SpaceMgr"].onSpaceLoseCell( self.spaceKey)
		self.destroy()

	def onGetCell(self):
		KBEngine.globalData["SpaceMgr"].onSpaceGetCell(self.cell, self.spaceKey)

