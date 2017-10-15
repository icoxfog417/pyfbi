import unittest
import os
import sys
import shutil
import time
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from pyfbi.profiler import pyFBI
from pyfbi.profiler import watch
from pyfbi.fbi_stat import FBIStat


@watch
def func1():
    time.sleep(1)


@watch
def func2():
    time.sleep(1)


class TestOneStat(unittest.TestCase):
    PATH = os.path.join(os.path.dirname(__file__), "read_stat")

    @classmethod
    def setUpClass(cls):
        if not os.path.isdir(cls.PATH):
            os.mkdir(cls.PATH)
        pyFBI.start()
        for f in [func1, func2, func2, func1, func2]:
            f()
        pyFBI.stop()
        pyFBI.dump(cls.get_path())

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.PATH)

    @classmethod
    def get_path(cls):
        return os.path.join(cls.PATH, "stat_file")

    def test_read_stats(self):
        stats = FBIStat.read_stats(self.get_path())
        print(FBIStat.headers())
        for s in stats:
            print(s)


if __name__ == "__main__":
    unittest.main()
