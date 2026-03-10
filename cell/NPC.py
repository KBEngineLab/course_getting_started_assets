import random

import KBEngine

from KBEDebug import DEBUG_MSG


class NPC(KBEngine.Entity):
	"""
	NPC的cell部分
	"""

	def __init__(self):
		KBEngine.Entity.__init__(self)
		DEBUG_MSG("NPC::__init__: created entityID = %i, spaceID = %s." % ( self.id, self.spaceID))



	def helloNPC(self, exposed):
		self.allClients.onHelloNPC(self.dialog[random.randint(0,len(self.dialog))])


