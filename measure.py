#
# kreaengine "kmeasure" wrapper
# Copyright (c) 2018 Aedan Cullen.
#

import irload
import ctypes as c

KMEASURE_DEFAULT_FN = "default_measure.ll"
KMEASURE_IR_FUNCS = [
]

class KreaLLMeasure:

    def __init__(self, ir=None):
        self.current_module = None
        
        if ir is None: ir = irload.read_module_from_file(KMEASURE_DEFAULT_FN)
        self.update(ir)
        
    def update(self, ir):
        if self.current_module is not None:
            irload.engine.remove_module(self.current_module)
            
        module, bound_funcs = irload.bind_funcs_from_module(
            ir, KMEASURE_IR_FUNCS
        )
        self.__dict__.update(bound_funcs)
        self.current_module = module
        self.current_ir = ir
