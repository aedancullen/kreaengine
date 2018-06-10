#
# kreaengine cluster host
# Copyright (c) 2018 Aedan Cullen.
#

import common
import multiprocessing

class EngineHost:

	def __init__(self, machineset=None, optimizeset=None, mode_recurrent=False):
		self.statelock = multiprocessing.Lock()
		self.enable = multiprocessing.Event()

		self.mode_recurrent = mode_recurrent

		self.assign_machineset(machineset)
		self.assign_optimizeset(optimizeset)

	def assign_machineset(self, machineset):
		with self.statelock:
			self.machineset = machineset
			self.machineset_hash = hash(self.machineset)

	def assign_optimizeset(self, optimizeset):
		with self.statelock:
			self.optimizeset = optimizeset
			self.optimizeset_hash = hash(self.optimizeset)

	def set_mode_recurrent(self, mode_recurrent):
		with self.statelock:
			self.mode_recurrent = mode_recurrent

	def enable_sync(self):
		self.enable.set()

	def disable_sync(self):
		self.enable.clear()

		

	def configure(self, authkey):
		common.host_startsync(self.sync, authkey)

	def set_machineset(machineset):
		self.machineset = machineset
		self.machineset_hash = hash(self.machineset)

	def set_optimizeset(optimizeset):
		self.optimizeset = optimizeset
		self.optimizeset_hash = hash(self.optimizeset)

	def sync(self, machineset_hash, optimizeset_hash, updateset_merge):

		ret_machineset = None
		ret_optimizeset = None

		if updateset_merge is not None:
			with self.statelock:

				self.optimizeset.merge(updateset_merge)
				self.optimizeset_hash = hash(self.optimizeset)

				if self.mode_recurrent:
					self.machineset = self.optimizeset
					self.machineset_hash = self.optimizeset_hash


		# Release statelock to wait, since hashes/sets may change
		self.enable.wait()

		with self.statelock:
	
			if self.machineset_hash != machineset_hash:
				ret_machineset = self.machineset
			if self.optimizeset_hash != optimizeset_hash:
				ret_optimizeset = self.optimizeset


		return ret_machineset, ret_optimizeset
