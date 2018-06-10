#
# kreaengine "kmachine" wrapper
# Copyright (c) 2018 Aedan Cullen.
#

import irload
import ctypes as c

KMACHINE_IR_FN = "kmachine.ll"
KMACHINE_IR_FUNCS = [
    ("1",),
    ("2",),
]

class KreaLLMachine:

    def __init__(self):
        bound_funcs = irload.bind_funcs_from_module(
            irload.read_module_from_file(KMACHINE_IR_FN),
            KMACHINE_IR_FUNCS
        )
        self.__dict__.update(bound_funcs)