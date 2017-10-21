from __future__ import print_function
import os
import sys
import time
import pstats
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import pyfbi


@pyfbi.target
def func(a, b):
    time.sleep(1)
    return a + b


@pyfbi.target
def func2(a, b):
    time.sleep(2)
    return a + b


class SampleClass():

    @pyfbi.target
    def show(self, seconds):
        time.sleep(seconds)
        return None


if __name__ == "__main__":
    print("Profile to stream  *******************")
    s = SampleClass()
    with pyfbi.watch():
        func(1, 2)
        s.show(1)
    func(1, 2)  # not recorded
    pyfbi.show()

    print("Profile to File **********************")
    path = os.path.join(os.path.dirname(__file__), "profile_result")
    with pyfbi.watch():
        func(2, 3)
        func(1, 2)
        func2(1, 2)
    pyfbi.dump(path)
    stats = pstats.Stats(path)
    stats.print_stats()
    os.remove(path)
