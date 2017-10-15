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
    if not os.path.isdir(profile_dir):
        os.mkdir(profile_dir)
    path = os.path.join(profile_dir, "sched_p")

    sched = Scheduler(5, path)
    pyFBI.start(sched)
    for f in [func1, func2, func2, func3, func1, func1]:
        f()
    pyFBI.stop()

    files = os.listdir(profile_dir)
    assert len(files) == 2, "10 sec creates 2 file"
    for f in files:
        stats = pstats.Stats(os.path.join(profile_dir, f))
        print(f)
        stats.print_stats()

    shutil.rmtree(profile_dir)
