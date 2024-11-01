import math
from base import get_wordlist, generate_string, get_charset, ALPHA_NUMERIC_SPECIAL

wordlist = get_wordlist()

# generate a secret string from 12/16 random words/characters from wordlist


def generate_pass(words: list[str], charset: str, length: int) -> str:
    words = [word.strip() for word in words]
    for word in words:
        if word not in wordlist:
            print(f"ERROR: Word '{word}' is not valid.")
            exit(1)

    seed_string = ' '.join(words)
    return generate_string(seed_string, charset, length)


def input_words() -> list[str]:
    print("Enter the words: (leave an empty line to finish)")
    words = []
    while True:
        try:
            word = input().strip()
        except EOFError:
            break
        if not word:
            break
        words.append(word)
    return words


if __name__ == '__main__':
    import sys

    if '--help' in sys.argv:
        print(
            'Usage: python words_pass.py [length] [--charset <charset_slug | charset>]')
        sys.exit(0)

    charset = get_charset(ALPHA_NUMERIC_SPECIAL)
    words = input_words()

    default_length = math.ceil(11 * len(words) / math.log2(len(charset)))
    length = int(sys.argv[1]) if len(sys.argv) > 1 else default_length

    password = generate_pass(words, charset, length)
    print(password)
