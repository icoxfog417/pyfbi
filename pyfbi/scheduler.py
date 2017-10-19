import os
from datetime import datetime
from threading import Timer


class Scheduler(object):

    def __init__(self, seconds, stat_dir, stat_file="stat"):
        self.seconds = seconds
        self.stat_dir = stat_dir
        self.stat_file = stat_file
        self._timer = None
        self.__watcher = None

    def start(self, profiler):
        self.stop()
        self.__watcher = profiler
        self._timer = Timer(self.seconds, self._record)
        if not os.path.isdir(self.stat_dir):
            os.mkdir(self.stat_dir)
        self._timer.start()

    def _stop_timer(self):
        if self._timer is not None:
            self._timer.cancel()
            self._timer = None

    def _record(self):
        if self.__watcher:
            path = self.get_path()
            if self.__watcher.global_watch:
                self.__watcher.write()
                self.__watcher.dump(path)
                self.__watcher._init_global_watch()
            else:
                self.__watcher.dump(path)
            self.__watcher.stats = None
            self._stop_timer()
            self._timer = Timer(self.seconds, self._record)
            self._timer.start()
    
    def stop(self):
        self.__watcher = None
        self._stop_timer()

    def get_path(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if "." in self.stat_file:
            name, ext = os.path.splitext(self.stat_file)
            file_name = "{}_{}{}".format(name, timestamp, ext)
        else:
            file_name = "{}_{}".format(self.stat_file, timestamp)
        return os.path.join(self.stat_dir, file_name)
