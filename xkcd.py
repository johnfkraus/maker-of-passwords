import secrets
import math
# On standard Linux systems, use a convenient dictionary file.
# Other platforms may need to provide their own word-list.

num_words_in_pw = 4
word_list_filename = 'wordlists/eff_large_wordlist.txt'

def create_wordlist(filename, numbered_list=False, maximum_word_length=100, words_start_with="N/A"):
    with open(filename) as f:
        if words_start_with == "N/A":
            words = [word.strip().lower() for word in f if len(word) <= maximum_word_length]
            return words
        else: 
            words = [word.strip().lower() for word in f if len(word) <= maximum_word_length and word.lower().startswith(words_start_with)]
            return words

def create_xkcd_password(filename, num_words_in_password, numbered_list=False, maximum_word_length=100, words_start_with="N/A"):
    with open(filename) as f:
        words = create_wordlist(filename, numbered_list, maximum_word_length, words_start_with)
        # words = [word.strip().lower() for word in f if len(word) <= maximum_word_length and word.startswith('Q')]
        word_list_length = len(words)
        possible_combinations = math.pow(word_list_length,num_words_in_password)
        entropy_bits = round(math.log(possible_combinations,2))
        print("number of words in password = " + str(num_words_in_password))
        print("number of words in word list \"" + filename + "\" = " + str(word_list_length))
        print("maximum word length = " + str(maximum_word_length))
        print("number of possible combinations of words = " + str(possible_combinations))
        print("password entropy bits = " + str(entropy_bits))
        if numbered_list == True:
            words2 = [word.split()[1] for word in words]
            password = ' '.join(secrets.choice(words2) for i in range(num_words_in_password)).lower()
        else:
            password = ' '.join(secrets.choice(words) for i in range(num_words_in_password)).lower()

    return password, entropy_bits, word_list_length, possible_combinations

# for n in range(0, 10):
#     password_and_entropy_bits = create_xkcd_password( 'wordlists/eff_large_wordlist.txt', 8, True)
#     print(n, password_and_entropy_bits[1], password_and_entropy_bits[0])

for n in range(0, 10):
    wordlist = "wordlists/Collins_Scrabble_Words_2019.txt"
    number_of_words_in_password = 7
    maximum_word_length = 8
    numbered_list = False  # list has a number in the first column = True
    words_start_with = "z"
    password = create_xkcd_password(wordlist, number_of_words_in_password, maximum_word_length=maximum_word_length, words_start_with=words_start_with)
    print(password)
    print("password = " + password[0])
    print("entropy bits = " + str(password[1]))
