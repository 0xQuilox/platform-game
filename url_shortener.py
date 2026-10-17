import random
import string


# Our in-memory storage: short_code -> long_url
# In Django this will become a Model, but the idea is the same: a mapping
url_map = {}


def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    code = "".join(random.choice(characters) for _ in range(length))
    return code

# TODO: write shorten(long_url) from memory below
def shorten(long_url):
    code = generate_short_code()
    url_map[code] = long_url
    return code

def expand(short_code):
    return url_map.get(short_code)
