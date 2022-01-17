

def add_numbers(*args):
    print(args)
    total = 0
    for e in args:
        total += e
    print("total = ", total)
    return total

assert add_numbers(1,2,3) == 6
assert add_numbers(1, 2, 3, 4, 5, 6, 7, 8, 9) == 45
