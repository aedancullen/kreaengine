#
# kreaengine "kmachine" wrapper
# Copyright (c) 2018 Aedan Cullen.
#

import irload
import ctypes as c

KMACHINE_DEFAULT_IR = """\
"""

KMACHINE_IR_FUNCS = [
]

class KreaLLMachine:

    def __init__(self, ir=None):
        self.current_module = None
        
        if ir is None: ir = KMACHINE_DEFAULT_IR
        self.update(ir)
        
    def update(self, ir):
        if self.current_module is not None:
            irload.engine.remove_module(self.current_module)
            
        module, bound_funcs = irload.bind_funcs_from_module(
            ir, KMACHINE_IR_FUNCS
        )
        self.__dict__.update(bound_funcs)
        self.current_module = module
        self.current_ir = ir
