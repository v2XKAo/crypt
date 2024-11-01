from base import get_charset, CHARSET_SLUGS, generate_string


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
