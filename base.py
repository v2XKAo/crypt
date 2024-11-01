import os
import sys
import hashlib


LOWER_CASE = "abcdefghijklmnopqrstuvwxyz"
UPPER_CASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALPHA = LOWER_CASE + UPPER_CASE
NUMBERIC = "0123456789"
ALPHA_NUMERIC = ALPHA + NUMBERIC
ALPHA_NUMERIC_SPECIAL = ALPHA_NUMERIC + "!@#$%^&*()-_=+[]{};:'\",.<>/?\\|`~"

CHARSET_SLUGS = {
    "lower": LOWER_CASE,
    "upper": UPPER_CASE,
    "alpha": ALPHA,
    "numeric": NUMBERIC,
    "alphanumeric": ALPHA_NUMERIC,
    "alphanumeric_special": ALPHA_NUMERIC_SPECIAL,
}


def get_charset(default=ALPHA_NUMERIC) -> str:
    charset = default

    if "--charset" in sys.argv:
        charset_option = sys.argv[sys.argv.index("--charset") + 1]
        charset_slug = charset_option.lower()
        if charset_slug in CHARSET_SLUGS:
            charset = CHARSET_SLUGS[charset_slug]
        else:
            charset = charset_option

        sys.argv.remove("--charset")
        sys.argv.remove(charset_option)

    return charset


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORDLIST_PATH = os.path.join(SCRIPT_DIR, 'bip39_english.txt')


def get_wordlist():
    with open(WORDLIST_PATH, 'r', encoding='utf-8') as f:
        wordlist = [word.strip() for word in f.readlines()]
    wordlist = [word for word in wordlist if word]  # Remove empty lines
    assert len(wordlist) == 2048
    return wordlist


def generate_string(seed: str, charset: str, length: int) -> str:
    result = []
    charset_length = len(charset)
    current_data = seed

    while len(result) < length:
        hash_object = hashlib.sha256(current_data.encode())
        hex_digest = hash_object.hexdigest()

        for i in range(0, len(hex_digest), 2):
            if len(result) >= length:
                break

            hex_pair = hex_digest[i:i+2]
            index = int(hex_pair, 16) % charset_length
            result.append(charset[index])

        current_data = hex_digest

    return ''.join(result)
