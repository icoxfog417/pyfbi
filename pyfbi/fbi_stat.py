import os
import pstats


class FBIStat():

    def __init__(
        self,
        file_path,
        func_name,
        line_no,
        ncalls,
        tottime,
        cumtime,
        callers
    ):
        self.file_path = file_path
        self.func_name = func_name
        self.line_no = line_no
        self.ncalls = ncalls
        self.tottime = tottime
        self.cumtime = cumtime
        self.callers = callers

    @property
    def is_builtin(self):
        if self.file_path == "~":
            return True
        else:
            return False

    @property
    def file_name(self):
        return os.path.basename(self.file_path)

    @property
    def dir_name(self):
        return os.path.dirname(self.file_path)

    @property
    def key(self):
        return self._make_key([self.file_path, self.line_no, self.func_name])

    @property
    def is_top(self):
        return True if len(self.callers) > 0 else False

    @classmethod
    def _make_key(cls, k):
        return "{0}:{1}({2})".format(k[0], k[1], k[2])

    @property
    def percall_tot(self):
        return 0 if self.ncalls == 0 else self.tottime / self.ncalls

    @property
    def percall_cum(self):
        return 0 if self.ncalls == 0 else self.cumtime / self.ncalls

    @classmethod
    def read_stats(cls, stat_path):
        stats = pstats.Stats(stat_path)
        _fbi_stats = []
        for k, v in stats.stats.items():
            file_path, line_no, func_name = k
            ncalls = v[0]
            tottime = v[2]
            cumtime = v[3]
            callers = []
            for k in v[4]:
                callers.append(cls._make_key(k))

            s = FBIStat(
                file_path, func_name, line_no, 
                ncalls, tottime, cumtime, callers)
            _fbi_stats.append(s)

        return _fbi_stats

    @classmethod
    def headers(cls):
        return "{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format(
            "ncalls", "tottiem", "percall", "cumtime", "percall",
            "filename:lineno(function)"
        )

    def __str__(self):
        return "{0}\t{1:.3f}\t{2:.3f}\t{3:.3f}\t{4:.3f}\t{5}".format(
            self.ncalls, self.tottime, self.percall_tot,
            self.cumtime, self.percall_cum, self.key
        )

    def to_dict(self):
        return {
            "key": self.key,
            "file_name": self.file_name,
            "dir_name": self.dir_name,
            "location": "{} @{}".format(self.func_name, self.line_no),
            "ncalls": self.ncalls,
            "tottime": self.tottime,
            "percall_tot": self.percall_tot,
            "cumtime": self.cumtime,
            "percall_cum": self.percall_cum,
            "is_builtin": self.is_builtin,
            "is_top": self.is_top
        }
