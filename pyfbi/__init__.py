import cProfile
from functools import update_wrapper, partial
from contextlib import contextmanager
from .watcher import Watcher
from .scheduler import Scheduler


_watcher = Watcher()


class target(object):

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
        if _watcher.is_profiling and not _watcher.global_watch:
            profile = cProfile.Profile()
            profile.enable()

        result = self.func(*args, **kwargs)

        if profile is not None:
            profile.disable()
            _watcher.write(profile)

        return result


@contextmanager
def watch(global_watch=False):
    _watcher.start(global_watch=global_watch)
    yield
    _watcher.stop()


@contextmanager
def watch_periodic(seconds, stat_dir, global_watch=False, stat_file="stat"):
    sched = Scheduler(seconds, stat_dir, stat_file)
    _watcher.start(scheduler=sched, global_watch=global_watch)
    yield
    _watcher.stop()


def show():
    _watcher.show()


def dump(file_path):
    _watcher.dump(file_path)
