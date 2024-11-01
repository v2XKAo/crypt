import secrets

from base import get_wordlist

wordlist = get_wordlist()


def generate_words(length=12):
    wordlist = get_wordlist()
    words = [secrets.choice(wordlist) for i in range(length)]
    return words


if __name__ == '__main__':
    import sys

    if '--help' in sys.argv:
        print('Usage: python generate_words.py <length>')
        sys.exit(0)

    length = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    words = generate_words(length)
    print('\n'.join(words))
