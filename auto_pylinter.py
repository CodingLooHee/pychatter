'''
Walker use for linting
'''
import os
from fnmatch import fnmatch
from pylint import epylint as lint

for path, subdir, files in os.walk('.\\'):
    for name in files:
        if fnmatch(name, '*.py'):
            print(f'Checking {name}...')
            lint.py_run(os.path.join(path, name))
