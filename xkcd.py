import secrets
import sys, getopt
import math
import argparse
from clint.textui import puts, indent, colored

# On standard Linux systems, use a convenient dictionary file.
# Other platforms may need to provide their own word-list.

num_words_in_pw = 4
word_list_filename = 'wordlists/eff_large_wordlist.txt'

def create_wordlist(filename, numbered_list=False, maximum_word_length=100, 
                    contains=None, words_start_with=None,  words_end_with=None, notcontain=None):
    templist = None
    with open(filename) as f:
        if contains == None and words_start_with == None and words_end_with == None:
            templist = [word.strip().lower()
                    for word in f if len(word) <= maximum_word_length]
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

    # # using list comprehension to remove duplicated from list
    # words = []
    # [words.append(x) for x in templist if x not in words]
    # return words   

def Sorting(lst):
    lst2 = sorted(lst, key=len)
    return lst2


def create_xkcd_password(filename="xxwordlists/Collins_Scrabble_Words_2019.txt", 
    num_words_in_password=7, numbered_list=False, contains=None, maximum_word_length=100, words_start_with=None, words_end_with=None, notcontain=None):
    print("notcontain = ", notcontain)
    with open(filename) as f:
        words = create_wordlist(filename, numbered_list,
                                maximum_word_length, contains, words_start_with, notcontain=notcontain)
        word_list_length = len(words)
        possible_combinations = math.pow(word_list_length,num_words_in_password)
        entropy_bits = round(math.log(possible_combinations,2))
        print("number of words in password = " + str(num_words_in_password))
        print("number of words in (filtered) word list \"" + filename + "\" = " + str(word_list_length))
        print("maximum word length = " + str(maximum_word_length))
        print("number of possible combinations of words = " + str(possible_combinations))
        print("password entropy bits = " + str(entropy_bits))
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
    
    
def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser()  # (prog=_program)

    parser.add_argument("--num",
                        help="number of passwords to generate",
                        type=int, default=1)

    parser.add_argument("--numwords",
                        help="number of words in each password",
                        type=int, default = 6)

    parser.add_argument("--maxwordlen",
                        help="max number of characters in each word",
                        type=int, default=8)

    parser.add_argument("--wordlist",
                        help="list of words to select from",
                        type=str, default="wordlists/Collins_Scrabble_Words_2019.txt")

    parser.add_argument("-n", "--notcontain",
                        help="word should not contain this letter",
                        type=str, default="u")

    # parser.add_argument("-f",
    #                     "--flag",
    #                     help="Specify a flag",
    #                     action="store_true")

    # parser.add_argument("--rating",
    #                     help="An option with a limited range of values",
    #                     choices=[1, 2, 3],
    #                     type=int)

    # Allow --day and --night options, but not together.
    group = parser.add_mutually_exclusive_group()

    group.add_argument("-s", "--startswith",
                        help="words in password should start with one of these letters",
                        type=str, default = None)

    group.add_argument("-c", "--contains",
                        help="words in password should contain one of these letters",
                        type=str, default = "q")

    group.add_argument("-e", "--endswith",
                        help="words in password should end with one of these letters",
                        type=str, default = None)

    # group.add_argument("--day",
    #                    help="mutually exclusive option",
    #                    action="store_true")

    # group.add_argument("--night",
    #                    help="mutually exclusive option",
    #                    action="store_true")

    args = parser.parse_args(args)

    print("args = ", args)

    for n in range(0, args.num):
        #wordlist = "wordlists/Collins_Scrabble_Words_2019.txt"
        # number_of_words_in_password = 7
        # maximum_word_length = args.maxwordlen

        #words_start_with = "z"
        #å password = create_xkcd_password(wordlist, number_of_words_in_password,
        #                                 maximum_word_length=maximum_word_length, words_start_with=words_start_with)
        password = create_xkcd_password(filename=args.wordlist, num_words_in_password=int(args.numwords),
                                         maximum_word_length=args.maxwordlen, contains=args.contains, notcontain=args.notcontain)

        print(password)
        print("password = " + password[0])
        print("entropy bits = " + str(password[1]))



if __name__ == '__main__':
    main()


# if __name__ == "__main__":
#     print("main", sys.argv)
#     main(sys.argv[1:])

