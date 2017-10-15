import os
import cProfile
import pstats
from datetime import datetime
from time import perf_counter
import tempfile
from tempfile import NamedTemporaryFile


class Profiler(object):

    def __init__(self):
        self.is_profiling = False
        self.stats = None
        self.scheduler = None

    def start(self, scheduler=None):
        self.is_profiling = True
        self.stats = None
        self.scheduler = scheduler
        if self.scheduler is not None:
            self.scheduler.start()

    def stop(self):
        self.is_profiling = False
        self.scheduler = None  # off scheduler

    def write(self, profile):
        new_stats = pstats.Stats(profile)
        if self.stats is None:
            self.stats = new_stats
        else:
            # Because of windows, can't use with statement 
            tempf = NamedTemporaryFile(delete=False)
            new_stats.dump_stats(tempf.name)
            tempf.flush()
            tempf.close()
            self.stats.add(tempf.name)
            os.remove(os.path.join(tempfile.gettempdir(), tempf.name))

        if self.scheduler is not None and self.scheduler.is_timing():
            self.dump(self.scheduler.get_path())
            self.stats = None

    def show(self):
        if self.stats is not None:
            self.stats.print_stats()
    
    def dump(self, file_path):
        if self.stats is not None:
            self.stats.dump_stats(file_path)


class Scheduler(object):

    def __init__(self, seconds, file_path):
        self.seconds = seconds
        self.file_path = file_path
        self.start_time = None

    def start(self):
        self.start_time = perf_counter()

    def is_timing(self):
        now = perf_counter()
        if (now - self.start_time) >= self.seconds:
            self.start_time = now
            return True
        else:
            return False

    def get_path(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if "." in self.file_path:
            root, ext = os.path.splitext(self.file_path)
            path = "{}_{}{}".format(root, timestamp, ext)
        else:
            path = "{}_{}".format(self.file_path, timestamp)
        return path


pyFBI = Profiler()


class watch(object):

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        profile = None
        if pyFBI.is_profiling:
            profile = cProfile.Profile()
            profile.enable()

        result = self.func(*args, **kwargs)

        if profile is not None:
            profile.disable()
            pyFBI.write(profile)

        return result
