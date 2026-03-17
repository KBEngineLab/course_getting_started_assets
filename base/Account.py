# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import json

from data import d_spaces, d_avatar_init


class Account(KBEngine.Proxy):
	def __init__(self):
		KBEngine.Proxy.__init__(self)
		self.activeAvatar = None
		
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

		if self.activeAvatar:
			if self.activeAvatar.client is not None:
				self.activeAvatar.giveClientTo(self)

			self.activeAvatar.destroyCellEntity()
			self.activeAvatar = None


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


	def reqCreateAvatar(self, arg_UNICODE):
		"""
		客户端请求创建角色
		"""

		if len(self.characters) >= 3:
			DEBUG_MSG("Account[%i].reqCreateAvatar:%s. character=%s.\n" % (self.id, arg_UNICODE, self.characters))
			self.client.onReqCreateAvatar(2,"")
			return


		# self.characters.append({
		# 	"dbid":KBEngine.genUUID64(),
		# 	"name":arg_UNICODE,
		# })
		# #
		# self.client.onReqCreateAvatar(0,self.characters)
		spaceData = d_spaces.datas.get("xinshoucun")
		avatarInitInfo = d_avatar_init.datas
		props = {
			"accountId"			: self.id,
			"name"			: arg_UNICODE,
			"direction"			: avatarInitInfo.get("direction", (0.0,0.0,0.0)),
			"position"			: spaceData.get("spawnPos", (0.0,0.0,0.0)),
			"HP":avatarInitInfo.get("HP", 100),
			"HP_Max":avatarInitInfo.get("HP_Max", 100),
			"MP":avatarInitInfo.get("MP", 120),
			"MP_Max":avatarInitInfo.get("MP_Max", 120),
		}

		avatar = KBEngine.createEntityLocally('Avatar', props)

		if avatar:
			avatar.writeToDB(self._onAvatarSaved)


	def _onAvatarSaved(self, success, avatar):
		"""
		新建角色写入数据库回调
		"""
		INFO_MSG('Account::_onAvatarSaved:(%i) create avatar state: %i, %s, %i' % (self.id, success,
		                                                                           avatar.cellData["name"],
		                                                                           avatar.databaseID))

		# 如果此时账号已经销毁， 角色已经无法被记录则我们清除这个角色
		if self.isDestroyed:
			if avatar:
				avatar.destroy(True)

			return


		if success:
			self.characters.append({
				"dbid":avatar.databaseID,
				"name":avatar.cellData["name"],
			})
			pass
		else:
			ERROR_MSG('Account::_onAvatarSaved:(%i) create avatar error' % self.id)

		avatar.destroy()

		if self.client:
			self.client.onReqCreateAvatar(1,self.characters)



	def reqAvatarEnterGame(self, arg_DBID):
		"""
		客户端请求角色进入游戏世界
		"""
		DEBUG_MSG("Account[%i].reqAvatarEnterGame:AvatarID:%i" % (self.id,arg_DBID))
		for character in self.characters:
			if character["dbid"] == arg_DBID:
				KBEngine.createEntityFromDBID("Avatar", arg_DBID, self._onAvatarCreated)


	def _onAvatarCreated(self, baseRef, dbid, wasActive):
		if wasActive:
			ERROR_MSG("Account::_onAvatarCreated:(%i): this character is in world now!" % (self.id))
			return
		if baseRef is None:
			ERROR_MSG("Account::_onAvatarCreated:(%i): the character you wanted to created is not exist!" % (self.id))
			return

		avatar = KBEngine.entities.get(baseRef.id)
		if avatar is None:
			ERROR_MSG("Account::_onAvatarCreated:(%i): when character was created, it died as well!" % (self.id))
			return

		if self.isDestroyed:
			ERROR_MSG("Account::_onAvatarCreated:(%i): i dead, will the destroy of Avatar!" % (self.id))
			avatar.destroy()
			return

		# 可以从配置文件或者持久化中获取角色的地图位置，这里我们写死
		self.client.onEnter("world")
		self.activeAvatar = avatar
		self.giveClientTo(avatar)

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

	def onDestroy(self):
		if self.activeAvatar:
			self.activeAvatar = None






