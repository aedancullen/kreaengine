#
# kreaengine IR loader
# Copyright (c) 2018 Aedan Cullen.
#

from llvmlite import binding as llvmbinding

llvmbinding.initialize()
llvmbinding.initialize_native_target()
llvmbinding.initialize_native_asmprinter()

target = llvmbinding.Target.from_default_triple()
target_machine = target.create_target_machine()
backing_mod = llvmbinding.parse_assembly("")
engine = llvmbinding.create_mcjit_compiler(backing_mod, target_machine)


def bind_funcs_from_module(filename, bind_funcs):
    ir = None
    with open(filename, "r") as irfile:
        ir = irfile.read()
    mod = llvmbinding.parse_assembly(ir)
    mod.verify()
    engine.add_module(mod)
    engine.finalize_object()
    engine.run_static_constructors()

    fdict = {}
    for name, cfunctype in bind_funcs:
        ptr = engine.get_function_address(name)
        fdict[name] = cfunctype(ptr)

    return fdict