
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