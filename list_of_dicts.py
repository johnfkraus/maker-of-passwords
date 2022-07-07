import pprint

pp = pprint.PrettyPrinter(indent=4, compact=False, width=30)

# Defining a list of dictionaries in Python
ls_dict = [{'py': 'Python', 'mat': 'MATLAB', 'cs': 'Csharp'},
           {'A': 65, 'B': 66, 'C': 67},
           {'a': 97, 'b': 98, 'c': 99}]

dict = {}
dict["pw4"] = {"abc": True}
#ls_dict.append("pw2":{"abc": True})
ls_dict.append(dict["pw4"])
# Printing the results
print("ls_dict = ")
pp.pprint(ls_dict)

# Validating the type of 'ls_dict' and its element
print(type(ls_dict))
print(type(ls_dict[0]))


stuff = ['spam', 'eggs', 'lumberjack', 'knights', 'ni']
stuff.insert(0, stuff[:])
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(stuff)
# [   ['spam', 'eggs', 'lumberjack', 'knights', 'ni'],
#     'spam',
#     'eggs',
#     'lumberjack',
#     'knights',
#     'ni']