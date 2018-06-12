#
# kreaengine cluster worker
# Copyright (c) 2018 Aedan Cullen.
#

import common
import machine
import measure

class EngineWorker:

	def __init__(self):
		
		self.measure = measure.KreaLLMeasure()
		self.measureir_hash = hash(self.measure.current_ir)
		self.machine = machine.KreaLLMachine()
		self.machineir_hash = hash(self.machine.current_ir)

		self.assign_machineset(common.ParamSet())
		self.assign_optimizeset(common.ParamSet())

	def assign_measureir(self, measureir):
		self.measureir = measureir
		self.measureir_hash = hash(self.measureir)
		self.measure.update(self.measureir)
		
	def assign_machineir(self, machineir):
		self.machineir = machineir
		self.machineir_hash = hash(self.machineir)
		self.machine.update(self.machineir)

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
			(measureir,machineir,machineset,optimizeset) = self.remote_sync(
				self.measureir_hash
				self.machineir_hash,
				self.machineset_hash,
				self.optimizeset_hash,
				updateset_merge
			)
		except:
			raise common.NoHostRetryException("Sync missed; wait for host, then reconfigure")
		
		if measureir is not None: self.assign_measureir(measureir)
		if machineir is not None: self.assign_machineir(machineir)
		if machineset is not None: self.assign_machineset(machineset)
		if optimizeset is not None: self.assign_optimizeset(optimizeset)


	def tick(self):

		#self.machine.

		self.sync(newset.diff(self.optimizeset))

