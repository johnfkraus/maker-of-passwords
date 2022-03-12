# https://dev.to/micahcarrick/python-argument-parsing-with-log-level-and-config-file-1d6p

import collections
import secrets
import sys, getopt
import math
import re
import logging
import argparse
from num2words import num2words
from typing_extensions import final
from clint.textui import puts, indent, colored
from password_strength import PasswordStats
from password_strength import PasswordPolicy


def main(args):
    logging_argparse = argparse.ArgumentParser(prog=__file__, add_help=False)
    logging_argparse.add_argument('-l', '--log-level', default='WARNING',
                                  help='set log level')
    logging_args, _ = logging_argparse.parse_known_args(args)

    try:
        logging.basicConfig(level=logging_args.log_level)
    except ValueError:
        logging.error("Invalid log level: {}".format(logging_args.log_level))
        sys.exit(1)

    logger = logging.getLogger(__name__)
    logger.info("Log level set: {}"
                .format(logging.getLevelName(logger.getEffectiveLevel())))
    
    parsers = [logging_argparse]
    main_parser = argparse.ArgumentParser(prog=__file__, parents=parsers)
    main_parser.add_argument('-1', '--option1')
    main_parser.add_argument('-2', '--option2')
    main_args = main_parser.parse_args(args)

    
if __name__ == "__main__":
    main(sys.argv[1:])

