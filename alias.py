import hashlib
from base import get_charset, CHARSET_SLUGS


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


if __name__ == "__main__":
    import sys

    if "--help" in sys.argv:
        print(
            "Usage: python alias.py <length> [--charset <charset_slug | charset>]")
        print("Available charset slugs:")
        for slug, charset in CHARSET_SLUGS.items():
            print(f"  {slug}: {charset}")
        sys.exit(0)

    charset = get_charset()

    output_length = int(sys.argv[1])
    seed = input("Enter input string: ").strip()

    output_string = generate_string(seed, charset, output_length)
    print(output_string)
