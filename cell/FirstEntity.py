import KBEngine
class FirstEntity(KBEngine.Entity):
	"""
	第一个实体的cell部分
	"""
	def __init__(self):
		KBEngine.Entity.__init__(self)

		# 通知客户端，进入世界
		self.client.onEnter()

	def say(self, exposed, arg_UNICODE):
		"""
		实现CellMethods中的say方法
		"""
		# 广播给所有客户端
		self.allClients.onSay("Entity::" + str(exposed) + " " + arg_UNICODE)



