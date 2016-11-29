@echo on

::Delete file
DEL _MachineLearn.pyd

::Wait for a while
ping 127.0.0.1 -n 6 >nul

::Compile
SET VS90COMNTOOLS=%VS110COMNTOOLS%
swig -c++ -python MachineLearn.i
python setup.py build_ext --inplace

echo finish
PAUSE
