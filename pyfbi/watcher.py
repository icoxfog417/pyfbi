import os
import cProfile
import pstats
import tempfile
from tempfile import NamedTemporaryFile


class Watcher(object):

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
        if self.global_watch:
            self.__profile.disable()
            if self.scheduler is None:
                self.write()
                self.__profile = None
        self.scheduler = None  # off scheduler

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
