import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from pyfbi.profiler import pyFBI
from pyfbi.profiler import watch


@watch
def func1(a, b):
    return a + b

def func2(a, b):
    return a + b

@watch
def func3(a, b):
    return a + b


pyFBI.start()
[f(1, 2) for f in (func1, func2, func3)]
pyFBI.stop()
pyFBI.show()
