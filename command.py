import sys
import argparse
# from . import _program
from clint.textui import puts, indent, colored


def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser() # (prog=_program)

    parser.add_argument("--num",
                        help="number of passwords to generate",
                        type=int, default=3)

    parser.add_argument("--numwords",
                        help="number of words in each password",
                        type=int)

    parser.add_argument("-s", "--startswith",
                        help="words in password should start with one of these letters",
                        type=str)

    parser.add_argument("-c", "--contains",
                        help="words in password should contain one of these letters",
                        type=str)

    parser.add_argument("-e", "--endswith",
                        help="words in password should end with one of these letters",
                        type=str)

    parser.add_argument("-f",
                        "--flag",
                        help="Specify a flag",
                        action="store_true")
    parser.add_argument("--rating",
                        help="An option with a limited range of values",
                        choices=[1, 2, 3],
                        type=int)

    # Allow --day and --night options, but not together.
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--day",
                       help="mutually exclusive option",
                       action="store_true")
    group.add_argument("--night",
                       help="mutually exclusive option",
                       action="store_true")

    args = parser.parse_args(args)

    print(args)
    puts(colored.blue("Arguments"))
    #puts(colored.green("int value: ") + str(args.int_value))
    puts(colored.green("flag: ") + str(args.flag))
    puts(colored.green("rating: ") + str(args.rating))
    puts(colored.green("starts with: ") + str(args.startswith))
    puts(colored.green("contains: ") + str(args.contains))
    puts(colored.green("ends with: ") + str(args.endswith))


if __name__ == '__main__':
    main()
