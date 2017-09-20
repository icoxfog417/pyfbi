# pyFBI

pyFBI enables "as much as needed" profiling by decorator.

```py
from pyfbi.profiler import pyFBI
from pyfbi.profiler import watch


@watch
def func1(a, b):
    return a + b

def func2(a, b):
    return a + b

@watch
def func3(a, b):
    return a + b


pyFBI.start()
[f(1, 2) for f in (func1, func2, func3)]
pyFBI.stop()
pyFBI.show()
```

only "watched" function is profiled.

```
         4 function calls in 0.000 seconds

   Random listing order was used

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.000    0.000 tests/demo.py:8(func1)
        2    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
        1    0.000    0.000    0.000    0.000 tests/demo.py:15(func3)
```

## Installation

comming soon

## Features

### Dump stats to file

You can save the profiled result to file.

```
pyFBI.dump("your_profile_path")
```
