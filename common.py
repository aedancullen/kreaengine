#
# kreaengine misc. format/networking
# Copyright (c) 2018 Aedan Cullen.
#

import irload
import multiprocessing
from multiprocessing import managers

class NoHostRetryException(Exception): pass


PS_PORT = 17100

PSIF_REG_STR = "kreaengine_psif"
PSIF_SYNC_FUNC = "sync"
PSIF_CTRL_FUNCS = [
    "assign_measureir",
    "assign_machineir",
    "assign_machineset",
    "assign_optimizeset",
    "assign_mode_recurrent",
    "enable_sync",
    "disable_sync"
]

_psw = None

class ServerParamSyncManager(managers.BaseManager): pass
class ClientParamSyncManager(managers.BaseManager): pass

ServerParamSyncManager.register(PSIF_REG_STR, callable=lambda:_psw)
ClientParamSyncManager.register(PSIF_REG_STR)


_hostmanager = None
_workermanager = None
_ctrlmanager = None


def parallel_boostrap_host(instance, authkey):
    global _hostmanager, _psw

    _psw = instance
    _hostmanager = ServerParamSyncManager(address=("", PS_PORT), authkey=authkey)
    _hostmanager.start()
    
def parallel_boostrap_worker(addrstr, authkey):
    pass


def bind_sync(addrstr, authkey):
    global _workermanager

    _workermanager = ClientParamSyncManager(address=(addrstr, PS_PORT), authkey=authkey)
    _workermanager.connect()
    syncif = getattr(_workermanager, PSIF_REG_STR)()
    
    return getattr(syncif, PSIF_SYNC_FUNC)

def bind_ctrl(addrstr, authkey):
    global _ctrlmanager
    
    _ctrlmanager = ClientParamSyncManager(address=(addrstr, PS_PORT), authkey=authkey)
    _ctrlmanager.connect()
    syncif = getattr(_ctrlmanager, PSIF_REG_STR)()
    
    bound_funcs = {}
    for func in PSIF_CTRL_FUNCS:
        bound_funcs[func] = getattr(syncif, func)
        
    return bound_funcs

class ParamSet:
    pass
