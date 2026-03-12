import math
import random


def getRandomPointInRadius( spawnPoints, radius):
	"""
	在spawnPoints为中心的radius半径内获取随机坐标
	"""
	x, y, z = spawnPoints

	# 随机角度
	angle = random.uniform(0, 2 * math.pi)

	# 随机半径（sqrt保证分布均匀）
	r = radius * math.sqrt(random.random())

	new_x = x + r * math.cos(angle)
	new_z = z + r * math.sin(angle)

	return new_x, y, new_z