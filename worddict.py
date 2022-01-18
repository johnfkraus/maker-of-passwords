

def create_wordlist(filename):
    # , numbered_list=False, maximum_word_length=100,
    #                 contains=None, words_start_with=None,  words_end_with=None):
    templist = None
    with open(filename) as f:
        templist = [line.strip() for line in f]
    
    return templist

# read the file that contains definitions
filename = "wordlists/Collins_Scrabble_Words_2019_with_definitions.txt"

list = create_wordlist(filename)

for i in range(0,12):
    splitted = list[i].split("\t", 1)
    print(splitted)
