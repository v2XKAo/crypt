
import secrets

from base import CHARSET_SLUGS, get_charset, ALPHA_NUMERIC_SPECIAL


def generate_password(charset: str, length=16) -> str:
    return ''.join(secrets.choice(charset) for _ in range(length))


if __name__ == "__main__":
    import sys

    if "--help" in sys.argv:
        print(
            "Usage: python generate_password.py <length> [--charset <charset_slug | charset>]")
        print("Available charset slugs:")
        for slug, charset in CHARSET_SLUGS.items():
            print(f"  {slug}: {charset}")
        sys.exit(0)

    charset = get_charset(ALPHA_NUMERIC_SPECIAL)

    output_length = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    output_string = generate_password(charset, output_length)
    print(output_string)
