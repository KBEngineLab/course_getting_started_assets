import KBEngine

from Account import Account


class Space(KBEngine.Space):
	"""
    Space的base部分，
    注意：它是一个实体，并不是真正的space，真正的space存在于cellapp的内存中，通过这个实体与之关联并操控space。
    """

	def __init__(self):
		KBEngine.Space.__init__(self)


	def onLoseCell(self):
		KBEngine.globalData["SpaceMgr"].onSpaceLoseCell( self.spaceKey)

	def onGetCell(self):
		KBEngine.globalData["SpaceMgr"].onSpaceGetCell(self.cell, self.spaceKey)

	def onDestroy(self):
		if self.cell is not None:
			# 销毁cell实体
			self.destroyCellEntity()
			return

		# # 销毁base
		# self.destroy()


