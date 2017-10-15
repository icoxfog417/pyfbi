import os
import sys
import time
import pstats
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from pyfbi.profiler import pyFBI
from pyfbi.profiler import watch


@watch
def func(a, b):
    time.sleep(1)
    return a + b


@watch
def func2(a, b):
    time.sleep(2)
    return a + b


if __name__ == "__main__":
    print("Profile to stream  *******************")
    pyFBI.start()
    func(1, 2)
    pyFBI.stop()
    func(1, 2)  # not recorded
    pyFBI.show()

    print("Profile to File **********************")
    path = os.path.join(os.path.dirname(__file__), "profile_result")
    pyFBI.start()
    func(2, 3)
    func(1, 2)
    func2(1, 2)
    pyFBI.stop()
    pyFBI.dump(path)
    stats = pstats.Stats(path)
    stats.print_stats()
    os.remove(path)
