#
# kreaengine "kmachine" wrapper
# Copyright (c) 2018 Aedan Cullen.
#

import irload
import ctypes as c

KMACHINE_IR_FUNCS = [
    ("1",),
    ("2",),
]

class KreaLLMachine:

    def __init__(self, ir):
        bound_funcs = irload.bind_funcs_from_module(
            ir, KMACHINE_IR_FUNCS
        )
        self.__dict__.update(bound_funcs)
