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

		self.assign_measureir(common.default_measureir)
		self.assign_machineset(common.ParamSet())
		self.assign_optimizeset(common.ParamSet())

	def assign_measureir(self, measureir):
		self.measureir = measureir
		self.measureir_hash = hash(self.measureir)
		self.measure = KreaLLMeasure(self.measureir)

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
			(measureir,machineset,optimizeset) = self.remote_sync(
				self.measureir_hash
				self.machineset_hash,
				self.optimizeset_hash,
				updateset_merge
			)
		except:
			raise common.NoHostRetryException("Sync missed; wait for host, then reconfigure")
		
		if measureir is not None: self.assign_measureir(measureir)
		if machineset is not None: self.assign_machineset(machineset)
		if optimizeset is not None: self.assign_optimizeset(optimizeset)


	def tick(self):

		self.machine.

		self.sync(newset.diff(self.optimizeset))

