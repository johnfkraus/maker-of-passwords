import math

possible_combinations = 255 # int(1024 + 1024/2)
print((possible_combinations))
print(bin(possible_combinations))
print(math.log(possible_combinations, 2))
print(math.pow(2, math.log(possible_combinations, 2)))

