# generate_random_string.py

import random
import string

def generate_random_string(length=10):
    """Генерирует случайную строку из строчных букв заданной длины."""
    letters = string.ascii_lowercase
    random_str = ''.join(random.choice(letters) for _ in range(length))
    return random_str