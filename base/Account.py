# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import json

class Account(KBEngine.Proxy):
	def __init__(self):
		KBEngine.Proxy.__init__(self)
		
	def onTimer(self, id, userArg):
		"""
		KBEngine method.
		使用addTimer后， 当时间到达则该接口被调用
		@param id		: addTimer 的返回值ID
		@param userArg	: addTimer 最后一个参数所给入的数据
		"""
		DEBUG_MSG(id, userArg)
		
	def onClientEnabled(self):
		"""
		KBEngine method.
		该entity被正式激活为可使用， 此时entity已经建立了client对应实体， 可以在此创建它的
		cell部分。
		"""
		INFO_MSG("account[%i] entities enable. entityCall:%s" % (self.id, self.client))
			
	def onLogOnAttempt(self, ip, port, password):
		"""
		KBEngine method.
		客户端登陆失败时会回调到这里
		"""
		INFO_MSG(ip, port, password)
		return KBEngine.LOG_ON_ACCEPT
		
	def onClientDeath(self):
		"""
		KBEngine method.
		客户端对应实体已经销毁
		"""
		DEBUG_MSG("Account[%i].onClientDeath:" % self.id)
		self.destroy()

	def reqAvatarList(self):
		"""
		客户端请求查询角色列表
		"""
		DEBUG_MSG("Account[%i].reqAvatarList: size=%i." % (self.id, len(self.characters)))
		self.client.onReqAvatarList(self.characters)
		pass

	def reqCreateAvatar(self, arg_UNICODE):
		"""
		客户端请求创建角色
		"""

		if len(self.characters) >= 3:
			DEBUG_MSG("Account[%i].reqCreateAvatar:%s. character=%s.\n" % (self.id, arg_UNICODE, self.characters))
			self.client.onReqCreateAvatar(2,"")
			return


		self.characters.append({
			"dbid":KBEngine.genUUID64(),
			"name":arg_UNICODE,
		})
		#
		self.client.onReqCreateAvatar(0,self.characters)
		pass

	def reqAvatarEnterGame(self, arg_DBID):
		"""
		客户端请求角色进入游戏世界
		"""
		DEBUG_MSG("Account[%i].reqAvatarEnterGame:AvatarID:%i" % (self.id,arg_DBID))
		pass

	def reqRemoveAvatar(self, arg_DBID):
		"""
		客户端请求删除角色
		"""
		DEBUG_MSG("Account[%i].reqRemoveAvatar:%i" % (self.id, arg_DBID))

		for character in self.characters:
			if character["dbid"] == arg_DBID:
				self.characters.remove(character)
				self.client.onReqRemoveAvatar(1,character["dbid"])
				return

		self.client.onReqRemoveAvatar(0,0)





