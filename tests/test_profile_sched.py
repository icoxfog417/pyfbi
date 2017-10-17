import os
import shutil
import sys
import time
import pstats
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from pyfbi.profiler import pyFBI, Scheduler
from pyfbi.profiler import watch


@watch
def func1():
    time.sleep(1)


@watch
def func2():
    time.sleep(2)


@watch
def func3():
    time.sleep(3)


if __name__ == "__main__":
    profile_dir = os.path.join(os.path.dirname(__file__), "profile")
    sched = Scheduler(5, stat_dir=profile_dir)
    pyFBI.start(sched)
    for f in [func1, func2, func2, func3, func1, func1]:
        f()
    pyFBI.stop()

    files = os.listdir(profile_dir)
    for f in files:
        stats = pstats.Stats(os.path.join(profile_dir, f))
        print(f)
        stats.print_stats()

    assert len(files) == 2, "10 sec creates 2 file"
    shutil.rmtree(profile_dir)
