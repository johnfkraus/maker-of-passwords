# two parameters, first param is string; second param is number

import sys

def get_args(name='default', first='a', second=2):
    return first, int(second)

first, second = get_args(*sys.argv)

print(first, second)
