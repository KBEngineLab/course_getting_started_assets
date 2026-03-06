# -*- coding: utf-8 -*-
import KBEngine
import copy
from KBEDebug import *

class Account(KBEngine.Entity):
	def __init__(self):
		KBEngine.Entity.__init__(self)
		DEBUG_MSG("Account::__init__:%s." % (self.__dict__))

		self.base.reqAvatarList()
		self.base.reqCreateAvatar("test")
		self.base.reqCreateAvatar("test222")
		self.dbid = 0


	def onReqAvatarList(self,avatarList):
		DEBUG_MSG("Account::onReqAvatarList:%s" % avatarList)
		pass
	def onReqCreateAvatar(self,recode,avatarList):
		DEBUG_MSG("Account::onReqCreateAvatar:%i %s" % (recode,avatarList))
		self.dbid = avatarList[0]["dbid"]
		DEBUG_MSG(self.dbid)
		self.base.reqRemoveAvatar(int(self.dbid))
		self.base.reqAvatarList()
		pass
	def onReqRemoveAvatar(self,recode,DBID):
		DEBUG_MSG("Account::onReqRemoveAvatar:%i %s" % (recode,DBID))
		pass