import os
import shutil
import sys
import time
import pstats
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import pyfbi


@pyfbi.target
def func1():
    time.sleep(1)


@pyfbi.target
def func2():
    time.sleep(2)


@pyfbi.target
def func3():
    time.sleep(3)


if __name__ == "__main__":
    stat_dir = os.path.join(os.path.dirname(__file__), "stats")
    with pyfbi.watch_periodic(seconds=5, stat_dir=stat_dir):
        for f in [func1, func2, func2, func3, func1, func1]:
            f()

    files = os.listdir(stat_dir)
    for f in files:
        stats = pstats.Stats(os.path.join(stat_dir, f))
        print(f)
        stats.print_stats()

    assert len(files) == 2, "10 sec creates 2 file"
    shutil.rmtree(stat_dir)
