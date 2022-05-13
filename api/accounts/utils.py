import random
import string

def random_name_generator():
    char = random.choice(string.ascii_letters)
    name = char + ''.join(str(random.randint(0, 9)) for i in range(14))

    return name