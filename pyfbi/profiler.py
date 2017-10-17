import os
import cProfile
import pstats
from datetime import datetime
from threading import Timer
import tempfile
from functools import update_wrapper, partial
from tempfile import NamedTemporaryFile


class Profiler(object):

    def __init__(self):
        self.is_profiling = False
        self.stats = None
        self.scheduler = None
        self.__profile = None

    def start(self, scheduler=None, global_watch=False):
        self.is_profiling = True
        self.stats = None
        self.scheduler = scheduler
        if global_watch:
            self._init_global_watch()

        if self.scheduler is not None:
            self.scheduler.start(self)

    @property
    def global_watch(self):
        return (True if self.__profile is not None else False)
    
    def _init_global_watch(self):
        self.__profile = cProfile.Profile()
        self.__profile.enable()

    def stop(self):
        self.is_profiling = False
        if self.scheduler:
            self.scheduler.stop()
            self.scheduler = None  # off scheduler
        if self.global_watch:
            self.__profile.disable()
            self.__profile = None

    def write(self, profile=None):
        new_stats = None
        if profile:
            new_stats = pstats.Stats(profile)
        elif self.global_watch:
            self.__profile.disable()
            new_stats = pstats.Stats(self.__profile)
            self.__profile.enable()
        else:
            raise Exception("Can not record the profile.")

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

    def show(self):
        if self.stats is not None:
            self.stats.print_stats()
    
    def dump(self, file_path):
        if self.stats is not None:
            self.stats.dump_stats(file_path)


class Scheduler(object):

    def __init__(self, seconds, stat_dir, stat_file="stat"):
        self.seconds = seconds
        self.stat_dir = stat_dir
        self.stat_file = stat_file
        self._timer = None
        self.__profiler = None

    def start(self, profiler):
        self.stop()
        self.__profiler = profiler
        self._timer = Timer(self.seconds, self._record)
        if not os.path.isdir(self.stat_dir):
            os.mkdir(self.stat_dir)
        self._timer.start()

    def _stop_timer(self):
        if self._timer is not None:
            self._timer.cancel()
            self._timer = None

    def _record(self):
        if self.__profiler:
            path = self.get_path()
            if self.__profiler.global_watch:
                self.__profiler.write()
                self.__profiler.dump(path)
                self.__profiler._init_global_watch()
            else:
                self.__profiler.dump(path)
            self.__profiler.stats = None
            self._stop_timer()
            self._timer = Timer(self.seconds, self._record)
            self._timer.start()
    
    def stop(self):
        self.__profiler = None
        self._stop_timer()

    def get_path(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if "." in self.stat_file:
            name, ext = os.path.splitext(self.stat_file)
            file_name = "{}_{}{}".format(name, timestamp, ext)
        else:
            file_name = "{}_{}".format(self.stat_file, timestamp)
        return os.path.join(self.stat_dir, file_name)


pyFBI = Profiler()


class watch(object):

    def __init__(self, func):
        update_wrapper(self, func)
        self.func = func

    def __get__(self, obj, objtype):
        # Support instance methods.
        if obj is not None:
            return partial(self.__call__, obj)
        else:
            return self.__call__

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
