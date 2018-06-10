#
# kreaengine cluster worker
# Copyright (c) 2018 Aedan Cullen.
#

import common

class EngineWorker:

	def __init__(self):
		self.machineset = None
		self.optimizeset = None
	
	def configure(self, addrstr, authkey):
		try:
			self.remote_sync = common.worker_getsync(addrstr, authkey)
		except:
			raise common.NoHostRetryException("Assuming correct authkey, host nonexistent")
		
		self.sync(None)

	def sync(self, updateset_merge):

		machineset_hash = hash(self.machineset)
		optimizeset_hash = hash(self.optimizeset)

		try:
			(machineset,optimizeset) = self.remote_sync(machineset_hash,optimizeset_hash,updateset_merge)
		except:
			raise common.NoHostRetryException("Sync missed; wait for host, then reconfigure")
		
		self.machineset = machineset if machineset is not None else self.machineset
		self.optimizeset = optimizeset if optimizeset is not None else self.machineset


	def tick(self):

		# ....

		self.sync(newset.diff(self.optimizeset))

