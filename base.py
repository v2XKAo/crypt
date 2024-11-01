import sys


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

    return charset
