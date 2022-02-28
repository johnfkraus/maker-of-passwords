# https://stackoverflow.com/questions/11760578/argparse-arguments-nesting

import collections
import secrets
import sys, getopt
import math
import re
import argparse
from num2words import num2words
from typing_extensions import final
from clint.textui import puts, indent, colored
from password_strength import PasswordStats
from password_strength import PasswordPolicy

def main(args=sys.argv[1:]):
    print("Running...")
    parser = argparse.ArgumentParser(description='Deployment tool')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', '--add', dest='name_to_add', help='Add a new group or a role to existing group')
    group.add_argument('-u', '--upgrade', dest='name_to_upgrade', help='Upgrade a group with the new version')
    parser.add_argument('--web_port', help='Port of the WEB instance that is being added to the group')

    args = parser.parse_args(args)
    print(args)

if __name__ == '__main__':
    main()

# I want to be able to run: "
# python subparser.py -a name --web_port=XXXX

# I don't want to be able to run: "
# python subparser.py -u name --web_port=XXXX

"""
Instead of having -a and -u be options, you may want to make them subcommands. Then, make --web-port an option of the add subcommand:

python my_script.py add name --web_port=XXXX
python my_script.py upgrade name
Something like:

parser = argparse.ArgumentParser(description='Deployment tool')
subparsers = parser.add_subparsers()

add_p = subparsers.add_parser('add')
add_p.add_argument("name")
add_p.add_argument("--web_port")
...

upg_p = subparsers.add_parser('upgrade')
upg_p.add_argument("name")
...
If you try run

my_script.py upgrade name --web_port=1234
you'll get an error for unrecognized argument "--web_port".

Likewise, if you try

my_script.py add name upgrade
you'll get an error for unrecognized argument "upgrade", since you only defined a single positional argument for the 'add' subcommand.

In other words, subcommands are implicitly mutually exclusive. The only tiny wart is that you need to add the "name" positional parameter to each subparser.

"""