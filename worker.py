#
# kreaengine cluster worker
# Copyright (c) 2018 Aedan Cullen.
#

import common
import machine
import measure

class EngineWorker:

	def __init__(self):

		self.machine = KreaLLMachine()
		
		self.measureir = None
		self.measure = None

		self.assign_machineset(None)
		self.assign_optimizeset(None)

	def assign_machineset(self, machineset):
		self.machineset = machineset
		self.machineset_hash = hash(self.machineset)

	def assign_optimizeset(self, optimizeset):
		self.optimizeset = optimizeset
		self.optimizeset_hash = hash(self.optimizeset)
	


	def configure(self, addrstr, authkey):
		try:
			self.remote_sync = common.worker_getsync(addrstr, authkey)
		except:
			raise common.NoHostRetryException("Assuming correct authkey, host nonexistent")
		
		self.sync(None)

	def sync(self, updateset_merge):

		try:
			(machineset,optimizeset) = self.remote_sync(
				self.machineset_hash,
				self.optimizeset_hash,
				updateset_merge
			)
		except:
			raise common.NoHostRetryException("Sync missed; wait for host, then reconfigure")
		
		if machineset is not None: self.assign_machineset(machineset)
		if optimizeset is not None: self.assign_optimizeset(optimizeset)


	def tick(self):

		self.machine.

		self.sync(newset.diff(self.optimizeset))

