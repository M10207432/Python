# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.10
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.





from sys import version_info as _swig_python_version_info
if _swig_python_version_info >= (2, 7, 0):
    def swig_import_helper():
        import importlib
        pkg = __name__.rpartition('.')[0]
        mname = '.'.join((pkg, '_MachineLearn')).lstrip('.')
        try:
            return importlib.import_module(mname)
        except ImportError:
            return importlib.import_module('_MachineLearn')
    _MachineLearn = swig_import_helper()
    del swig_import_helper
elif _swig_python_version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_MachineLearn', [dirname(__file__)])
        except ImportError:
            import _MachineLearn
            return _MachineLearn
        if fp is not None:
            try:
                _mod = imp.load_module('_MachineLearn', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _MachineLearn = swig_import_helper()
    del swig_import_helper
else:
    import _MachineLearn
del _swig_python_version_info
try:
    _swig_property = property
except NameError:
    pass  # Python < 2.2 doesn't have 'property'.

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if (name == "thisown"):
        return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if (not static):
        if _newclass:
            object.__setattr__(self, name, value)
        else:
            self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr(self, class_type, name):
    if (name == "thisown"):
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    raise AttributeError("'%s' object has no attribute '%s'" % (class_type.__name__, name))


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except __builtin__.Exception:
    class _object:
        pass
    _newclass = 0

InputNum = _MachineLearn.InputNum
HiddenNum = _MachineLearn.HiddenNum
OutputNum = _MachineLearn.OutputNum
class HiddenNode(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, HiddenNode, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, HiddenNode, name)
    __repr__ = _swig_repr
    __swig_setmethods__["id"] = _MachineLearn.HiddenNode_id_set
    __swig_getmethods__["id"] = _MachineLearn.HiddenNode_id_get
    if _newclass:
        id = _swig_property(_MachineLearn.HiddenNode_id_get, _MachineLearn.HiddenNode_id_set)
    __swig_setmethods__["layer_id"] = _MachineLearn.HiddenNode_layer_id_set
    __swig_getmethods__["layer_id"] = _MachineLearn.HiddenNode_layer_id_get
    if _newclass:
        layer_id = _swig_property(_MachineLearn.HiddenNode_layer_id_get, _MachineLearn.HiddenNode_layer_id_set)
    __swig_setmethods__["threshold"] = _MachineLearn.HiddenNode_threshold_set
    __swig_getmethods__["threshold"] = _MachineLearn.HiddenNode_threshold_get
    if _newclass:
        threshold = _swig_property(_MachineLearn.HiddenNode_threshold_get, _MachineLearn.HiddenNode_threshold_set)
    __swig_setmethods__["output"] = _MachineLearn.HiddenNode_output_set
    __swig_getmethods__["output"] = _MachineLearn.HiddenNode_output_get
    if _newclass:
        output = _swig_property(_MachineLearn.HiddenNode_output_get, _MachineLearn.HiddenNode_output_set)
    __swig_setmethods__["Err"] = _MachineLearn.HiddenNode_Err_set
    __swig_getmethods__["Err"] = _MachineLearn.HiddenNode_Err_get
    if _newclass:
        Err = _swig_property(_MachineLearn.HiddenNode_Err_get, _MachineLearn.HiddenNode_Err_set)
    __swig_setmethods__["next"] = _MachineLearn.HiddenNode_next_set
    __swig_getmethods__["next"] = _MachineLearn.HiddenNode_next_get
    if _newclass:
        next = _swig_property(_MachineLearn.HiddenNode_next_get, _MachineLearn.HiddenNode_next_set)
    __swig_setmethods__["pre"] = _MachineLearn.HiddenNode_pre_set
    __swig_getmethods__["pre"] = _MachineLearn.HiddenNode_pre_get
    if _newclass:
        pre = _swig_property(_MachineLearn.HiddenNode_pre_get, _MachineLearn.HiddenNode_pre_set)

    def __init__(self):
        this = _MachineLearn.new_HiddenNode()
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this
    __swig_destroy__ = _MachineLearn.delete_HiddenNode
    __del__ = lambda self: None
HiddenNode_swigregister = _MachineLearn.HiddenNode_swigregister
HiddenNode_swigregister(HiddenNode)


def GetInput(list):
    return _MachineLearn.GetInput(list)
GetInput = _MachineLearn.GetInput

def weightEvaluate(start, end_id, node):
    return _MachineLearn.weightEvaluate(start, end_id, node)
weightEvaluate = _MachineLearn.weightEvaluate

def Add(n1, n2):
    return _MachineLearn.Add(n1, n2)
Add = _MachineLearn.Add

def Div(n, div):
    return _MachineLearn.Div(n, div)
Div = _MachineLearn.Div

def SqrtInPyObj(obj):
    return _MachineLearn.SqrtInPyObj(obj)
SqrtInPyObj = _MachineLearn.SqrtInPyObj
# This file is compatible with both classic and new-style classes.


