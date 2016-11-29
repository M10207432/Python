#!/usr/bin/env python
""" setup.py file for SWIG example """
from distutils.core import setup, Extension

MachineLearn_module = Extension('_MachineLearn',
                           sources=['MachineLearn_wrap.cxx', 'MachineLearn.cpp'], )

setup (name = 'MachineLearn',
       version = '0.1',
       author = "Wayne",
       description = """Simple swig example from docs""",
       ext_modules = [MachineLearn_module],
       py_modules = ["MachineLearn"], )
