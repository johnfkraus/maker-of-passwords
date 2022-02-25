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

ljust_width = 55 # formatting param for printing strings to terminl

def create_wordlist_profile(filename): #, numbered_list=False, maximum_word_length=100, 
                    #contains=None, words_start_with=None,  words_end_with=None, notcontain=None):
    worddict = {}
    with open(filename) as f:
        for word in f:
            word = word.strip().lower()
            word_len = len(word)
            if word_len in worddict.keys():
                worddict[word_len] = worddict[word_len] + 1
            else:
                worddict[word_len] = 1

    sortedworddict = collections.OrderedDict(sorted(worddict.items()))
    total_words = 0
    cumulative_words = 0
    for key in sortedworddict.keys():
        if key > 6:
            return
        total_words = total_words + worddict[key]
        cumulative_words = cumulative_words + worddict[key]
        print(key, " : ", worddict[key], " cumul: ", cumulative_words)
    print("Total words in sortedworddict: ", total_words)


def get_no_vowel_words():
    novowelwords = []
    words = ['who', 'what', 'when', 'where', 'why', 'sly', 'shy', 'bashful', 'coy', 'myth', 'hymn']
    vowel = ['a', 'e', 'i', 'o', 'u']

    for word in words:
        novowel = True    

        for letter in word:
            if letter in vowel:
                novowel=False

        if novowel == True:
            novowelwords.append(word)


    print(novowelwords)


# convenience method for neater looking printing of a label followed by a number
# "value" parameter is expected to be a decimal integer
def print_formatted_label(inlabel, value, parameter=None):
    ljust_width = 55
    if parameter:
        label  =  inlabel + " (" + str(parameter) + ")"
        # print("65, length of label = ", len(label))
        print(label.ljust(ljust_width), " = ", ("{:,}".format(value)).rjust(8))
    else:
        label = inlabel
        print(label.ljust(ljust_width), " = ", ("{:,}".format(value)).rjust(8))



def create_wordlist_with_defns(filename, numbered_list=False, maximum_word_length=100,
                    contains=None, words_start_with=None,  words_end_with=None, notcontain=None):
    templist_contains = []
    templist_notcontain = []
    templist_words_start_with = []
    final_word_list = None
    if contains:
        contains = contains.strip().lower()
    if notcontain:
        notcontain = notcontain.strip().lower()
    with open(filename) as f:
        # if contains == None and words_start_with == None and words_end_with == None and notcontain == None:
        original_list_unfiltered = [line.split("\t") for line in f]

        print_formatted_label("Length of unfiltered word list", len(original_list_unfiltered))

        final_word_list = [pass_def for pass_def in original_list_unfiltered if
             len(pass_def[0].strip()) <= maximum_word_length]

        print_formatted_label("Length word list after word length filter", len(final_word_list), maximum_word_length)



        
        for pass_def in final_word_list:
            pass_def[0] = pass_def[0].strip().lower()
            pass_def[1] = pass_def[1].strip()


        # no vowels
            if True: # no vowels param specified
                x = re.search("\b[bcdfghjklmnpqrstvwxyz]+\b", pass_def[0])
                if x:
                    print(pass_def[0])



            if contains:
                if contains in pass_def[0]:
                    templist_contains.append(pass_def)
                final_word_list = templist_contains
        

        print_formatted_label("Length of word list after contains filter", len(final_word_list), 
            "None" if contains == None else contains)
        if notcontain:
            for pass_def in final_word_list:
                if not notcontain in pass_def[0]:
                    templist_notcontain.append(pass_def)
                final_word_list = templist_notcontain

            print_formatted_label("Length of word list after noncontain filter", len(final_word_list), notcontain)


        if words_start_with:
            for pass_def in templist_notcontain:
                if pass_def[0][0] == words_start_with:
                    templist_words_start_with.append(pass_def)
            print("len templist_notcontain (", notcontain, ") = ",
                  len(templist_notcontain))
            final_word_list = templist_words_start_with

    print_formatted_label("Length of final_word_list", len(final_word_list))
    return final_word_list


# experiment with the password_strength package; work in process
def get_pw_strength(password):
    # assume no spaces or other delimiters between words in password
    password = password.replace(" ","")
    stats = PasswordStats(password)

    print(password, "entropy bits = ", round(stats.entropy_bits),"entropy density = ", stats.entropy_density,"strength = ", stats.strength())
    print("alphabet = ", stats.alphabet)
    print("alphabet_cardinality = ", stats.alphabet_cardinality)
    print("char_categories = ", stats.char_categories)
    print("char_categories_detailed = ", stats.char_categories_detailed)
    print("combinations = ", "{:,}".format(stats.combinations), ", digits = ", len(str(stats.combinations)))
    print("entropy_density = ", stats.entropy_density)
    print("26 lower-case letter entropy bits = ", get_entropy_bits_based_on_alphabet_length(password, 26))

# instead of calculating entopy based on length of word list and number of words drawn, you can also calculate entropy based on the available characters.
# how many binary digits are required to encode the number of combinations
def get_entropy_bits_based_on_alphabet_length(generated_password, alpha_len):
    password_len = len(generated_password)
    possible_combinations_of_letters = int(math.pow(alpha_len, password_len))
    entropy_bits = math.ceil(math.log(possible_combinations_of_letters, 2))
    print("Possible_combinations of letters using a", alpha_len, "-character set and a password of", password_len, "letters = ", "{:,}".format(possible_combinations_of_letters), "or", bin(possible_combinations_of_letters), ", entropy bits = ", entropy_bits)
    # Note: num2words US vs. UK disjunct.
    # https://www.merriam-webster.com/dictionary/number#table
    print(num2words(possible_combinations_of_letters).capitalize())
    return entropy_bits


# How long would it take to exhaust the search space for a given number of possible password
# combinations and a given rate of password hashing.
# Regarding the assumed rate of password hashing, one benchmark, 350 billion per second, 
# might be taken from this old blog post: https://pthree.org/2013/04/16/password-attacks-part-i-the-brute-force-attack/
def time_to_exhaust_search_space(possible_combinations, passwords_per_sec_billions=350):
    passwords_per_second = passwords_per_sec_billions * 1000000000
    seconds_to_exhaust = possible_combinations / passwords_per_second
    if seconds_to_exhaust < 1.0:
        print("Less than one second required to exhaust search space at a rate of ", passwords_per_sec_billions, "billion passwords per second.")
    else:
        print("Time to exhaust search space = ", display_time(
            seconds_to_exhaust, granularity=1), " at ", passwords_per_sec_billions, "billion passwords per second.")
    return seconds_to_exhaust


intervals = (
    ('years', 31536000),  # 365 * 60 * 60 * 24 * 7
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
)

def display_time(seconds, granularity=2):
    # years_in_seconds = 31536000 
    # years_threshold = years_in_seconds * 4
    # # if seconds > years_threshold:
    # #     years = "{:,}".format(seconds/years_in_seconds)
    #     # print(seconds/years_in_seconds, "years" )
    #     # print(years, "years" )

    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            value =  "{:,}".format(value)
            result.append("{} {}".format(value, name))

    # return ', '.join(result[:granularity])
    return ', '.join(result[:granularity])

# the following method might be better than display_time(), above.  Not implemented yet, though.
def seconds_to_text(unit, granularity = 1):

  ratios = {
    'decades' : 311040000, # 60 * 60 * 24 * 30 * 12 * 10
    'years'   : 31104000,  # 60 * 60 * 24 * 30 * 12
    'months'  : 2592000,   # 60 * 60 * 24 * 30
    'days'    : 86400,     # 60 * 60 * 24
    'hours'   : 3600,      # 60 * 60
    'minutes' : 60,        # 60
    'seconds' : 1          # 1
  }

  texts = []
  for ratio in ratios:
    result, unit = divmod(unit, ratios[ratio])
    if result:
      if result == 1:
        ratio = ratio.rstrip('s')
      texts.append(f'{result} {ratio}')
  texts = texts[:granularity] 
  if not texts:
    return f'0 {list(ratios)[-1]}'
  text = ', '.join(texts)
  if len(texts) > 1:
    index = text.rfind(',')
    text = f'{text[:index]} and {text[index + 1:]}'
  return text


def get_xkcd_entropy(words, num_words_in_password):
    word_list_length = len(words)
    possible_combinations = int(math.pow(word_list_length,num_words_in_password))
    entropy_bits = math.ceil(math.log(possible_combinations,2))
    print("Number of possible combinations of words = ", "{:,}".format(possible_combinations), " or ", bin(possible_combinations))
    print("# of decimal digits = ", len(str(possible_combinations)))
    print(num2words(possible_combinations).capitalize())
    time_to_exhaust_search_space(possible_combinations)
    print("entropy bits based on no. of possible word combinations = " + str(entropy_bits))


def create_xkcd_password(filename="wordlists/Collins_Scrabble_Words_2019_with_definitions.txt",
        num_words_in_password=7, 
        numbered_list=False, 
        contains=None,
        maximum_word_length=8,
        words_start_with=None, 
        words_end_with=None,
        notcontain=None):

    create_wordlist_profile(filename)
    with open(filename) as f:
        pwlist = []
        password = ''
        words = create_wordlist_with_defns(filename, numbered_list,
                                maximum_word_length, contains, words_start_with, notcontain=notcontain)
        for i in range(num_words_in_password):
            pwlist.append(secrets.choice(words))

        for i in range(len(pwlist)):
            password = password + pwlist[i][0].strip().lower() + ' '
            password = password.lower()

        print(">>> password = ", password, "<<<")
        for i in range(len(pwlist)):
            print(str(i + 1), pwlist[i][0].strip() + ' -- ' + pwlist[i][1].strip())

        get_xkcd_entropy(words, num_words_in_password)
        get_pw_strength(password)

    
def main(args=sys.argv[1:]):
    # TODO: add parameter validation.  I.e., no numbers where letters are expected.
    # TODO: parameter values can contain more than one character; i.e., you can specify that more than one letter should not appear in the word list.
    # TODO: add -v parameter for verbose terminal output; then trim down the default terminal output
    # TODO: recovery gracefully if there are zero words in the word list.

    # Why is 'wordlists' a list?  You might have more the one word list option, but mainly this list was for trying different word lists and migrating to a list containing definitions.
    wordlists = ["wordlists/Collins_Scrabble_Words_2019_with_definitions.txt"]


    # https: // docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser(description="""A password generator inspired by[xkcd](http://xkcd.com/936/). 
    Generates passwords by drawing English words randomly from a Scrabble word list, subject to your optional custom parameters.  Supplies word definitions as an aid to memory. Calculates password entropy metrics. Helps you win at Scrabble.\n
Warning: this program is incomplete. Not all functionality is enabled. Little testing has been done. Passwords composed of multiple lower-case dictionary words are displayed with space delimiters for legibility but are assumed to be concatenated with no delimiters between the words for entropy calculations.""")

    parser.add_argument("-t", "--ctpw",
                        help="number of passwords to generate, default=1",
                        type=int, default=1)

    parser.add_argument("-w","--numwords" ,
                        help="number of words in each password, default=6",
                        type=int, default = 6)

    parser.add_argument("-m", "--maxwordlen",
                        help="max number of characters per word, default=8",
                        type=int, default=8)

    parser.add_argument('--novowels', action='store_false')


    parser.add_argument("-l", "--wordlist",
                        help="path to list of words from which to select",
                        type=str, default=wordlists[0])

    parser.add_argument("-x", "--notcontain",
                        help="words should not contain this single letter",
                        type=str, default=None)

    # Allow --day and --night options, but not together.  This exclusivity is not exactly necessary and subject to refactoring when the code is improved enough to handle independent parameters.
    group = parser.add_mutually_exclusive_group()

    group.add_argument("-s", "--startswith",
                        help="words in password should start with one of these letters",
                        type=str, default=None)

    group.add_argument("-c", "--contains",
                        help="words in password should contain one of these letters",
                        type=str, default = None)

    group.add_argument("-e", "--endswith",
                        help="words in password should end with one of these letters",
                        type=str, default = None)

    args = parser.parse_args(args)

    print("args = ", args)

    for n in range(0, args.ctpw):
        if (args.ctpw > 1):
            print("========Generated password #", n + 1, "========")

        create_xkcd_password(filename=args.wordlist, num_words_in_password=int(args.numwords),
                                         maximum_word_length=args.maxwordlen, contains=args.contains, notcontain=args.notcontain)


if __name__ == '__main__':
    main()
