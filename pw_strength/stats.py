
# import secrets
# import sys, getopt
import math
# import re
import logging as log
# import argparse
from num2words import num2words
# from typing_extensions import final
# from clint.textui import puts, indent, colored
# from password_strength import PasswordStats
# from password_strength import PasswordPolicy


# instead of calculating entropy based on length of word list and number of words drawn, you can also calculate entropy based on the available characters.
# how many binary digits are required to encode the number of combinations
def get_entropy_bits_based_on_alphabet_length2(generated_password, alpha_len):
    password_len = len(generated_password)
    possible_combinations_of_letters = int(math.pow(alpha_len, password_len))
    entropy_bits = math.ceil(math.log(possible_combinations_of_letters, 2))
    log.info("Possible_combinations of letters using a" + str(alpha_len) + "-character set and a password of" + str(
        password_len) + "letters (ignoring xkcd process) = " + "{:,}".format(
        possible_combinations_of_letters) + "or" + bin(possible_combinations_of_letters) + ", entropy bits = " + str(
        entropy_bits))
    # Note: num2words US vs. UK disjunct.
    # https://www.merriam-webster.com/dictionary/number#table
    log.info(num2words(possible_combinations_of_letters).capitalize())
    return entropy_bits
