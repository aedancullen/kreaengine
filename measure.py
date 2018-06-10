#
# kreaengine "kmeasure" wrapper
# Copyright (c) 2018 Aedan Cullen.
#

import irload
import ctypes as c

KMEASURE_IR_FUNCS = [
    ("1",),
    ("2",),
]

class KreaLLMeasure:

    def __init__(self, ir):
        bound_funcs = irload.bind_funcs_from_module(
            ir, KMEASURE_IR_FUNCS
        )
        self.__dict__.update(bound_funcs)