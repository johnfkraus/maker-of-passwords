import secrets
import math
# On standard Linux systems, use a convenient dictionary file.
# Other platforms may need to provide their own word-list.
#with open('/usr/share/dict/words') as f:
#with open('words.txt') as f:

num_words_in_pw = 4
word_list_filename = 'wordlists/eff_large_wordlist.txt'
#numbered_list = True  # list has a number in the first column = True

def create_xkcd_password(filename, num_words, numbered_list):
    with open(filename) as f:
        words = [word.strip() for word in f]
        word_list_length = len(words)
        possible_combinations = math.pow(word_list_length,num_words)
        entropy_bits = round(math.log(possible_combinations,2))
        print("number of words in password = " + str(num_words))
        print("number of words in word list \"" + filename + "\" = " + str(word_list_length))
        print("number of possible combinations of words = " + str(possible_combinations))
        print("password entropy bits = " + str(entropy_bits))
        if numbered_list == True:
            words2 = [word.split()[1] for word in words]
            password = ' '.join(secrets.choice(words2) for i in range(num_words)).lower()
        else:
            password = ' '.join(secrets.choice(words) for i in range(num_words)).lower()

    return password, entropy_bits, word_list_length, possible_combinations

# for n in range(0, 10):
#     password_and_entropy_bits = create_xkcd_password( 'wordlists/eff_large_wordlist.txt', 8, True)
#     print(n, password_and_entropy_bits[1], password_and_entropy_bits[0])

for n in range(0, 10):
    wordlist = "wordlists/Collins_Scrabble_Words_2019.txt"
    number_of_words_in_password = 5
    numbered_list = False  # list has a number in the first column = True
    password_and_entropy_bits = create_xkcd_password('wordlists/Collins_Scrabble_Words_2019.txt', 5, False)
    print(n, password_and_entropy_bits[1], password_and_entropy_bits[0])

# get_xkcd_password( 'eff_large_wordlist.txt', 6)
# get_xkcd_password( 'eff_short_wordlist_1.txt', 7)
# get_xkcd_password( 'eff_short_wordlist_2_0.txt', 7)