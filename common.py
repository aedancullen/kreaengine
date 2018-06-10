#
# kreaengine misc. format/networking
# Copyright (c) 2018 Aedan Cullen.
#

class NoHostRetryException(Exception): pass

import multiprocessing
from multiprocessing import managers
from base64 import b64encode, b64decode

PS_PORT = 17100

PSIF_REG_STR = "kreaengine_psif"
PSIF_SYNC_FUNC = "kreaengine_sync"


_host_sync_callable = lambda *args,**kwargs: None


class ParamSyncInterface: pass

_psw = ParamSyncInterface()
setattr(_psw, PSIF_SYNC_FUNC, lambda *args,**kwargs:_host_sync_callable(*args,**kwargs))


class HostParamSyncManager(managers.BaseManager): pass
class WorkerParamSyncManager(managers.BaseManager): pass

HostParamSyncManager.register(PSIF_REG_STR, callable=lambda:_psw)
WorkerParamSyncManager.register(PSIF_REG_STR)


_hostmanager = None
_workermanager = None

def host_startsync(host_sync_callable, authkey):
	global _host_sync_callable, _hostmanager

	_host_sync_callable = host_sync_callable
	_hostmanager = HostParamSyncManager(address=("", PS_PORT), authkey=authkey)
	_hostmanager.start()
	return b64encode(multiprocessing.current_process().authkey)[:-1]

def worker_getsync(addrstr, authkey):
	global _workermanager

	_workermanager = WorkerParamSyncManager(address=(addrstr, PS_PORT), authkey=authkey)
	_workermanager.connect()
	syncif = getattr(_workermanager, PSIF_REG_STR)()
	return getattr(syncif, PSIF_SYNC_FUNC)


class ParamSet:
	pass