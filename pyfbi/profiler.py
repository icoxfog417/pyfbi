import cProfile
import pstats
from tempfile import NamedTemporaryFile


class Profiler(object):

    def __init__(self):
        self.is_profiling = False
        self.stats = None

    def start(self):
        self.is_profiling = True
        self.stats = None

    def stop(self):
        self.is_profiling = False

    def write(self, profile):
        new_stats = pstats.Stats(profile)
        if self.stats is None:
            self.stats = new_stats
        else:
            with NamedTemporaryFile() as tempf:
                new_stats.dump_stats(tempf.name)
                self.stats.add(tempf.name)

    def show(self):
        if self.stats is not None:
            self.stats.print_stats()
    
    def dump(self, file_path):
        if self.stats is not None:
            self.stats.dump_stats(file_path)


pyFBI = Profiler()


class watch(object):

    def __init__(self, func):
        self.profile = cProfile.Profile()
        self.func = func

    def __call__(self, *args, **kwargs):
        if pyFBI.is_profiling:
            self.profile.enable()

        result = self.func(*args, **kwargs)

        if pyFBI.is_profiling:
            self.profile.disable()
            pyFBI.write(self.profile)

        return result
