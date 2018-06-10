#
# kreaengine cluster worker
# Copyright (c) 2018 Aedan Cullen.
#

import common

class EngineWorker:

	def __init__(self):
		self.machineset = None
		self.optimizeset = None
	
	def run(self, addrstr, authkey):
		self.remote_sync = common.worker_getsync(addrstr, authkey)

	def sync(self):

		machineset_hash = hash(self.machineset)
		optimizeset_hash = hash(self.optimizeset)

		(machineset,optimizeset) = self.remote_sync(machineset_hash,optimizeset_hash)
		
		self.machineset = machineset if machineset is not None else self.machineset
		self.optimizeset = optimizeset if optimizeset is not None else self.machineset

