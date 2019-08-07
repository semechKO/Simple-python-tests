from logger import fin_logger

class DB:
	def __init__(self):
		self.tanks = {1101: {'credits': 500, 'gold': 0}, #tankID : {params}
							2101: {'credits': 850, 'gold': 10},
							3101: {'credits': 1500, 'gold': 50}}

		self.guns = {1101: {223: {'credits': 20, 'gold': 0}, #tankID : {gunID: {params}}
						224: {'credits': 0, 'gold': 30}},
					2101: {555: {'credits': 250, 'gold': 0},
						655: {'credits': 240, 'gold': 0}},
					3101: {485: {'credits': 220, 'gold': 0},
						286: {'credits': 120, 'gold': 0}}}

class Shop:
	def __init__(self):
		self.fin_logger = fin_logger()
		self.db = DB()

	def __buyTank(self, player, tankID):
		if tankID in self.db.tanks:
			player.inventoryPlanes.append(tankID)

			if self.db.tanks[tankID]['credits'] >= player.resources.credits and \
				self.db.tanks[tankID]['gold'] >= player.resources.gold:

				player.resources.credits -= self.db.tanks[tankID]['credits']
				player.resources.gold -= self.db.tanks[tankID]['gold']
			player.saveResources()
			self.fin_logger.log_state(player)

	def __buyGuns(self, *args):
		player, tankID, gunID = args

		if tankID in player.inventoryPlanes and gunID in self.db.guns[tankID]:
			player.inventoryGuns[tankID].append(gunID)
			player.resources.credits -= self.db.guns[tankID][gunID]['credits']
			player.resources.gold -= self.db.guns[tankID][gunID]['gold']
			player.saveResources()

		self.fin_logger.log_state(player)