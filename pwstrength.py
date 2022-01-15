
from password_strength import PasswordStats
from password_strength import PasswordPolicy

policy = PasswordPolicy.from_names(
    length=8,  # min length: 8
    uppercase=2,  # need min. 2 uppercase letters
    numbers=2,  # need min. 2 digits
    special=2,  # need min. 2 special characters
    nonletters=2,  # need min. 2 non-letter characters (digits, specials, anything)
)

# password = 'qwerty123'
passwords = ['qwerty123','G00dPassw0rd?!', '1100011010','V3ryG00dPassw0rd?!', 'andyally' ]

for password in passwords:
    stats = PasswordStats(password)
    print(password, round(stats.entropy_bits), stats.entropy_density, stats.strength())
