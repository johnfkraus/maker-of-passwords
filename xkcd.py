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

# num_words_in_pw = 4
word_list_filename = 'wordlists/eff_large_wordlist.txt'

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
    print("Total : ", total_words)

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


def create_wordlist_with_defns(filename, numbered_list=False, maximum_word_length=100,
                    contains=None, words_start_with=None,  words_end_with=None, notcontain=None):
    templist_length = None
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
        print("len unfiltered word list             = ", "{:,}".format(len(original_list_unfiltered)))

        print("len unfiltered word list".ljust(43)," = ", "{:,}".format(len(original_list_unfiltered)))

        final_word_list = [pass_def for pass_def in original_list_unfiltered if
             len(pass_def[0].strip()) <= maximum_word_length]
        print("len word list after word length filter (", maximum_word_length, ") = ", len(final_word_list))

        for pass_def in final_word_list:
            pass_def[0] = pass_def[0].strip().lower()
            pass_def[1] = pass_def[1].strip()

        if contains:
            if contains in pass_def[0]:
                templist_contains.append(pass_def)
            final_word_list = templist_contains
        
        label = "len word list after contains filter (" , contains, ") = ",
        print("len word list after contains filter (", contains, ") = ",
              len(final_word_list))

        if notcontain:
            for pass_def in final_word_list:
                if not notcontain in pass_def[0]:
                    templist_notcontain.append(pass_def)
                final_word_list = templist_notcontain

            label = "len word list after noncontain filter (", notcontain, ")"
            print("len word list after noncontain filter (", notcontain, ") = ",
                  len(final_word_list))


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
            
    print("len final_word_list = ",
            len(final_word_list))

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
    # assume no space between words in password
    password = password.replace(" ","")
    stats = PasswordStats(password)

    print(password, round(stats.entropy_bits),
          stats.entropy_density, stats.strength())
    print("alphabet = ", stats.alphabet)
    print("alphabet_cardinality = ", stats.alphabet_cardinality)
    print("char_categories = ", stats.char_categories)
    print("char_categories_detailed = ", stats.char_categories_detailed)
    print("combinations = ", "{:,}".format(stats.combinations))
    print("entropy_density = ", stats.entropy_density)
    print("26-letter entropy bits = ", get_entropy_bits_based_on_alphabet_length(password, 26))



def get_entropy_bits_based_on_alphabet_length(password, alpha_len):
    # num_letters_in_alphabet = 26
    password_len = len(password)
    # password_len = 2
    possible_combinations_of_letters = int(math.pow(alpha_len, password_len))
    entropy_bits = math.ceil(math.log(possible_combinations_of_letters, 2))
    print("possible_combinations of", password_len, "letters with", alpha_len, "-character alphabet = ", "{:,}".format(possible_combinations_of_letters), "or", bin(possible_combinations_of_letters), ", entropy bits = ", entropy_bits)
    print(num2words(possible_combinations_of_letters))
    # how many binary digts are required to encode the number of combinations
    return entropy_bits


def get_xkcd_entropy(words, num_words_in_password):
    word_list_length = len(words)
    possible_combinations = int(math.pow(word_list_length,num_words_in_password))
    entropy_bits = math.ceil(math.log(possible_combinations,2))
    print("number of words in (filtered) word list = " + "{:,}".format(word_list_length))
    print("number of words in password = " + str(num_words_in_password))
    # print("maximum word length (no. of characters) = " + str(maximum_word_length))
    print("number of possible combinations of words = ", "{:,}".format(possible_combinations), " or ", bin(possible_combinations))

    print(num2words(possible_combinations))

    print("entropy bits based on no. of possible word combinations = " + str(entropy_bits))


def create_xkcd_password(filename="xxwordlists/Collins_Scrabble_Words_2019.txt", 
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

            print("password = ", password)
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
            # if numbered_list == True:
            #     words2 = [word.split()[1] for word in words]
            #     password = ' '.join(secrets.choice(words2) for i in range(num_words_in_password)).lower()
            # else:
            password = ' '.join(secrets.choice(words) for i in range(num_words_in_password)).lower()

            return password, entropy_bits, word_list_length, possible_combinations

# for n in range(0, 10):
#     password_and_entropy_bits = create_xkcd_password( 'wordlists/eff_large_wordlist.txt', 8, True)
#     print(n, password_and_entropy_bits[1], password_and_entropy_bits[0])

numbered_list = False  # list has a number in the first column = True
    
def main(args=sys.argv[1:]):

    print("\n######################## MAKER OF PASSWORDS #########################\n")

    print("Not implemented: --contains parameter")
    print("Passwords composed of multiple dictionary words are assumed to have no delimiters between the words.")

    wordlists = ["wordlists/Collins_Scrabble_Words_2019.txt",
                 "wordlists/Collins_Scrabble_Words_2019_with_definitions.txt"]

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
                        type=str, default=wordlists[1])

    parser.add_argument("-n", "--notcontain",
                        help="words should not contain this single letter",
                        type=str, default="u")

    # Allow --day and --night options, but not together.
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


# if __name__ == "__main__":
#     print("main", sys.argv)
#     main(sys.argv[1:])

# def main(argv):
#     parser = argparse.ArgumentParser(description='Process some integers.')
#     parser.add_argument("-n")
#     try:
#         opts, args = getopt.getopt(argv,"nhi:o:",["n=","l=", "s=", "e="])
#         print(opts, args)
#     except getopt.GetoptError:
#         print('xkcd.py -i <inputfile> -o <outputfile>')
#         sys.exit(2)
#     startswith = []
#     endswith = []
#     contains = []
#     num = 0
#     for opt, arg in opts:
#         if opt == '-h':
#             print('xkcd.py -n <number of passwords to generate> -s <words start with> -e <words end with letter> -c <words contain letters>')
#             sys.exit()
#         elif opt in ("n", "--num"):
#             num = arg
#             print("num = ", num)
#         elif opt in ("-s", "--startswith"):
#             startswitharg = arg
#             if startswitharg.contains(","):
#                 startswith.append(startswitharg.split(","))
#             print(startswith)
#         elif opt in ("-e", "--endswith"):
#             endswitharg = arg
#             if endswitharg.contains(","):
#                 endswith.append(endswitharg.split(","))
#             print(endswith)

#     #print( 'Input file is "', inputfile)
