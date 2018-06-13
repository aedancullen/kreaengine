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

_psw = None

class ServerParamSyncManager(managers.BaseManager): pass
class ClientParamSyncManager(managers.BaseManager): pass

ServerParamSyncManager.register(PSIF_REG_STR, callable=lambda:_psw)
ClientParamSyncManager.register(PSIF_REG_STR)


_manager = None


def parallel_boostrap_host(instance, authkey):
    global _manager, _psw

    _psw = instance
    _manager = ServerParamSyncManager(address=("", PS_PORT), authkey=authkey)
    _manager.start()
    
def parallel_boostrap_worker(addrstr, authkey):
    pass


def bind_sync(addrstr, authkey):
    global _manager

    _manager = ClientParamSyncManager(address=(addrstr, PS_PORT), authkey=authkey)
    _manager.connect()
    syncif = getattr(_manager, PSIF_REG_STR)()
    
    return getattr(syncif, PSIF_SYNC_FUNC)


class ParamSet:
    pass
