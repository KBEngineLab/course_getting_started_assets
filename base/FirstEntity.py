import KBEngine

from FirstSpace import FirstSpace


class FirstEntity(KBEngine.Proxy):
	"""
	第一个实体的base部分
	"""
	def __init__(self):
		KBEngine.Entity.__init__(self)

	def helloBase(self, arg_UNICODE):
		print(arg_UNICODE)



# 	===================================回调方法======================================


	def onClientEnabled( self ):
		"""
		如果在脚本中实现了此回调，当实体可用时（ 各种初始化完毕并且可以与客户端通讯 ）该回调被调用。 这个方法没有参数。
		注意：giveClientTo将控制权赋给了该实体时也会导致该回调被调用。
		"""
		first_space:FirstSpace = KBEngine.globalData["FirstSpace"]
		self.createCellEntity(first_space.cell)
