
# numerical persistance; https://www.youtube.com/watch?v=Wim9WJeDTHQ&ab_channel=Numberphile

# run as: `python per.py 277777788888899` to get 11 steps

import sys

def per(n, steps=0):
  if len(str(n)) == 1:
    # print(n)
    print("Total # of steps: ", steps)
    retval = "Total # of steps = " + str(steps)
    print(retval)
    return "Total # of steps = " + str(steps)

  steps += 1
  digits = [int(i) for i in str(n)]

  result = 1
  for j in digits:
    result *= j
  print(result)

  per(result, steps)


# print(per(778899999))
 

# print(per(277777788888899))
'''
# TWO PARAMS
def get_args(name='default', first='a', second=2):
    return first, int(second)

first, second = get_args(*sys.argv)
print(first, second)
'''

# ONE PARAM
def get_args(name='default', first=277777788888899):
    return int(first)

first  = get_args(*sys.argv)
print("first = ", first)

print(per(first))