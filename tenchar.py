import string
import secrets
from password_strength import PasswordStats

special_chars = "!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"


alphabet = string.ascii_letters + string.digits + string.punctuation
print(alphabet)
for n in range(0,100):
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(12))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3):
            break

    stats = PasswordStats(password)
    # print(stats.strength())  #-> Its strength is 0.316
    # print(stats.entropy_bits)

    #print(password, PasswordStats(password).entropy_bits)
    print(password, stats.entropy_bits, stats.entropy_density)