import os
import sys
import time
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import pyfbi


@pyfbi.target
def func1():
    time.sleep(1)

def func2():
    time.sleep(2)

@pyfbi.target
def func3():
    time.sleep(3)


with pyfbi.watch():
    [f() for f in (func1, func2, func3)]
pyfbi.show()


with pyfbi.watch(global_watch=True):
    [f() for f in (func1, func2, func3)]
pyfbi.show()
