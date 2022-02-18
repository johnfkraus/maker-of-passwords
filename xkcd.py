import collections
import secrets
import sys, getopt
import math
import argparse
from num2words import num2words
from typing_extensions import final
from clint.textui import puts, indent, colored
from password_strength import PasswordStats
from password_strength import PasswordPolicy

numbered_list = False  # list has a number in the first column = True
ljust_width = 55 # formatting param for printing strings to terminl

# word_list_filename = 'wordlists/eff_large_wordlist.txt'

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


def create_wordlist(filename, numbered_list=False, maximum_word_length=100, 
                    contains=None, words_start_with=None,  words_end_with=None, notcontain=None):
    templist = None
    with open(filename) as f:
        if contains == None and words_start_with == None and words_end_with == None:
            templist = [word.strip().lower()
                    for word in f if len(word.strip().lower()) <= maximum_word_length]
        else: 
            if notcontain == None:
                contains = contains.lower()
                templist = [word.strip().lower() for word in f if len(word) <= maximum_word_length and contains in word.lower()]
            else:
                notcontain = notcontain.lower()
                templist = [word.strip().lower() for word in f if len(word) <= maximum_word_length and contains in word.lower() and not notcontain in word.lower()]
        if numbered_list == True:
            words2 = [word.split()[1] for word in templist]
            return words2
        else:
            return templist


# value = decimal integer
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
    # templist_length = None
    templist_contains = []
    templist_notcontain = []
    templist_words_start_with = []
    final_word_list = None
    wordlist = None
    if contains:
        contains = contains.strip().lower()
    if notcontain:
        notcontain = notcontain.strip().lower()
    with open(filename) as f:
        # if contains == None and words_start_with == None and words_end_with == None and notcontain == None:
        original_list_unfiltered = [line.split("\t") for line in f]
        # print("len unfiltered word list             = ", "{:,}".format(len(original_list_unfiltered)))

        #print("len unfiltered word list".ljust(ljust_width)," = ", "{:,}".format(len(original_list_unfiltered)))

        print_formatted_label("93 length of unfiltered word list", len(original_list_unfiltered))

        final_word_list = [pass_def for pass_def in original_list_unfiltered if
             len(pass_def[0].strip()) <= maximum_word_length]
        #print("len word list after word length filter (", maximum_word_length, ") = ", "{:,}".format(len(final_word_list)))

        print_formatted_label("97 length word list after word length filter", len(final_word_list), maximum_word_length)

        for pass_def in final_word_list:
            pass_def[0] = pass_def[0].strip().lower()
            pass_def[1] = pass_def[1].strip()

        if contains:
            if contains in pass_def[0]:
                templist_contains.append(pass_def)
            final_word_list = templist_contains
        
        # label = "len word list after contains filter (" , contains, ") = ",
        # print("len word list after contains filter (", contains, ") = ", "{:,}".format(len(final_word_list)))
        print_formatted_label("112 length of word list after contains filter", len(final_word_list), 
            "None" if contains == None else contains)
        if notcontain:
            for pass_def in final_word_list:
                if not notcontain in pass_def[0]:
                    templist_notcontain.append(pass_def)
                final_word_list = templist_notcontain

            # label = "len word list after noncontain filter (" + notcontain + ")"
            # print("len word list after noncontain filter (", notcontain, ") = ", ("{:,}".format(len(final_word_list)).rjust(8)))
            # print(label.ljust(ljust_width), " = ",  ("{:,}".format(len(final_word_list)).rjust(8)))

            print_formatted_label("119 length of word list after noncontain filter", len(final_word_list), notcontain)

        # replace
        # for pass_def in templist_contains:
        #     if notcontain:
        #         if not notcontain in pass_def[0]:
        #             templist_notcontain.append(pass_def)
        #         final_word_list = templist_notcontain
        #     else:
        #         templist_notcontain = templist_contains
        # print("len templist_notcontain (", notcontain, ") = ",
        #       len(templist_notcontain))

        if words_start_with:
            for pass_def in templist_notcontain:
                if pass_def[0][0] == words_start_with:
                    templist_words_start_with.append(pass_def)
            print("len templist_notcontain (", notcontain, ") = ",
                  len(templist_notcontain))
            final_word_list = templist_words_start_with
            
    # print("length of final_word_list = ".ljust(ljust_width), " = ", ("{:,}".format(len(final_word_list)).rjust(8)))

    print_formatted_label("148 length of final_word_list", len(final_word_list))

            # templist_words_start_with = templist_notcontain 
            # templist = [line.split("\t") for line in f if len(
            #     line.split("\t")[0].strip()) <= maximum_word_length and 
            #     contains in line.split("\t")[0].strip().lower() and 
            #     not notcontain in line.split("\t")[0].strip().lower()]


    return final_word_list
    # return templist_notcontain
            # for line in f:
            #     templist = line.split("\t")
            # templist = [word.strip().lower()
            #             for word in f if len(word.strip().lower()) <= maximum_word_length]
        # else:
        #     if notcontain == None:
        #         contains = contains.lower()
        #         templist = [word.strip().lower() for word in f if len(
        #             word) <= maximum_word_length and contains in word.lower()]
        #     else:
        #         notcontain = notcontain.lower()
        #         templist = [word.strip().lower() for word in f if len(
        #             word) <= maximum_word_length and contains in word.lower() and not notcontain in word.lower()]
        # if numbered_list == True:
        #     words2 = [word.split()[1] for word in templist]
        #     return words2
        # else:
        #     return templist

    # # using list comprehension to remove duplicated from list
    # words = []
    # [words.append(x) for x in templist if x not in words]
    # return words   

def Sorting(lst):
    lst2 = sorted(lst, key=len)
    return lst2

def get_pw_strength(password):
    # assume no spaces or other delimiters between words in password
    password = password.replace(" ","")
    stats = PasswordStats(password)

    print(password, round(stats.entropy_bits),
          stats.entropy_density, stats.strength())
    print("alphabet = ", stats.alphabet)
    print("alphabet_cardinality = ", stats.alphabet_cardinality)
    print("char_categories = ", stats.char_categories)
    print("char_categories_detailed = ", stats.char_categories_detailed)
    print("combinations = ", "{:,}".format(stats.combinations))
    print("digits = ", len(str(stats.combinations)))
    print("entropy_density = ", stats.entropy_density)
    print("26-letter entropy bits = ", get_entropy_bits_based_on_alphabet_length(password, 26))

# instead of calculating entopy based on length of word list and number of words drawn, you can also calculate entropy based on the available characters.
# how many binary digts are required to encode the number of combinations
def get_entropy_bits_based_on_alphabet_length(password, alpha_len):
    # num_letters_in_alphabet = 26, no upper or lower case, no special characters, etc.
    password_len = len(password)
    possible_combinations_of_letters = int(math.pow(alpha_len, password_len))
    entropy_bits = math.ceil(math.log(possible_combinations_of_letters, 2))
    print("214 possible_combinations of", password_len, "letters with", alpha_len, "-character alphabet = ", "{:,}".format(possible_combinations_of_letters), "or", bin(possible_combinations_of_letters), ", entropy bits = ", entropy_bits)
    # Note: num2words US vs. UK disjunct.
    # https://www.merriam-webster.com/dictionary/number#table
    print(num2words(possible_combinations_of_letters))
    return entropy_bits


# see: https://pthree.org/2013/04/16/password-attacks-part-i-the-brute-force-attack/
# How long would it take to exhaust the search space for a given number of possible pasword
# combinations and a given rate of password hashing.
def time_to_exhaust_search_space(possible_combinations, passwords_per_sec_billions=350):
    passwords_per_second = passwords_per_sec_billions * 1000000000
    seconds_to_exhaust = possible_combinations / passwords_per_second
    print("221 time to exhaust search space = ", display_time(
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
    years_in_seconds = 31536000 
    years_threshold = years_in_seconds * 4
    # if seconds > years_threshold:
    #     years = "{:,}".format(seconds/years_in_seconds)
        # print(seconds/years_in_seconds, "years" )
        # print(years, "years" )

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


# years5_4 =   5987369392383789062
# print(display_time(49999999999444499, granularity=2))
# print(display_time(499999, granularity=2))
# print(display_time(years5_4, granularity=2))

# the following method might be better than display_time(), above.
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
    print("number of possible combinations of words = ", "{:,}".format(possible_combinations), " or ", bin(possible_combinations))
    print("# of decimal digits = ", len(str(possible_combinations)))
    time_to_exhaust_search_space(possible_combinations)

    print(num2words(possible_combinations))
    print("entropy bits based on no. of possible word combinations = " + str(entropy_bits))


def create_xkcd_password(filename="wordlists/Collins_Scrabble_Words_2019_with_definitions.txt",
        num_words_in_password=7, 
        numbered_list=False, 
        contains=None,
        maximum_word_length=8,
        words_start_with=None, 
        words_end_with=None,
        notcontain=None):

    # print("notcontain = ", notcontain)
    create_wordlist_profile(filename)
    with open(filename) as f:
        if True:
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

        else:
            words = create_wordlist(filename, numbered_list,
                                maximum_word_length, contains, words_start_with, notcontain=notcontain)
            word_list_length = len(words)
            possible_combinations = int(math.pow(word_list_length,num_words_in_password))
            entropy_bits = math.ceil(math.log(possible_combinations,2))
            print("number of words in (filtered) word list \"" + filename +
                "\" = " + "{:,}".format(word_list_length))
            print("number of words in password = " + str(num_words_in_password))
            print("maximum word length (no. of characters) = " + str(maximum_word_length))
            print("number of possible combinations of words = ", "{:,}".format(possible_combinations),  bin(possible_combinations))
            print("entropy bits based on no. of possible word combinations = " + str(entropy_bits))
            password = ' '.join(secrets.choice(words) for i in range(num_words_in_password)).lower()
            return password, entropy_bits, word_list_length, possible_combinations

    
def main(args=sys.argv[1:]):
    print("\n######################## MAKER OF PASSWORDS #########################")
    print("""* Generate xkcd-type passwords by drawing from a list of words useful in a game of Scrabble.
* Provide word definitions as an aid to memory.
* Provide password entropy metrics.
* Win at Scrabble.
""")
    print("Not implemented: --contains parameter")
    print("Passwords composed of multiple dictionary words are assumed to have no delimiters between the words for entropy calculations.")

    # you might have more the one word list option, but mainly this list was for trying different word lists and migrating to a list containing definitions.
    wordlists = ["wordlists/Collins_Scrabble_Words_2019_with_definitions.txt"]

    parser = argparse.ArgumentParser()

    parser.add_argument("--num",
                        help="number of passwords to generate, default=1",
                        type=int, default=1)

    parser.add_argument("--numwords",
                        help="number of words in each password, default=6",
                        type=int, default = 6)

    parser.add_argument("--maxwordlen",
                        help="max number of characters per word, default=8",
                        type=int, default=8)

    parser.add_argument("--wordlist",
                        help="path to list of words from which to select",
                        type=str, default=wordlists[0])

    parser.add_argument("-n", "--notcontain",
                        help="words should not contain this single letter",
                        type=str, default="u")

    # Allow --day and --night options, but not together.  This exclusivity is not exactly necessary and subject to refactoring when the code is improved enough to handle independent parameters.
    group = parser.add_mutually_exclusive_group()

    group.add_argument("-s", "--startswith",
                        help="words in password should start with one of these letters",
                        type=str, default = None)

    # not implemented apparently
    group.add_argument("-c", "--contains",
                        help="words in password should contain one of these letters",
                        type=str, default = None)

    group.add_argument("-e", "--endswith",
                        help="words in password should end with one of these letters",
                        type=str, default = None)

    args = parser.parse_args(args)

    print("args = ", args)

    for n in range(0, args.num):
        password = create_xkcd_password(filename=args.wordlist, num_words_in_password=int(args.numwords),
                                         maximum_word_length=args.maxwordlen, contains=args.contains, notcontain=args.notcontain)


if __name__ == '__main__':
    main()
