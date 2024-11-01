import random
from secrets import randbelow
import sys

# Use a large prime number for the finite field
PRIME = 2**521 - 1  # A large Mersenne prime

def mod_inv(a, p):
    """Compute the modular inverse of a modulo p."""
    return pow(a, -1, p)

def eval_polynomial(coeffs, x, p):
    """Evaluate a polynomial at x with coefficients over a finite field p."""
    y = 0
    for i, coeff in enumerate(coeffs):
        y = (y + coeff * pow(x, i, p)) % p
    return y

def generate_shares(secret_int, m, n, p=PRIME):
    """Generate n shares with threshold m from the secret integer."""
    if m > n:
        raise ValueError("Threshold m cannot be greater than the number of shares n.")

    # Generate random coefficients for the polynomial
    coeffs = [secret_int] + [randbelow(p) for _ in range(m - 1)]

    # Generate n shares
    shares = []
    for i in range(1, n + 1):
        x = i
        y = eval_polynomial(coeffs, x, p)
        shares.append((x, y))
    return shares

def reconstruct_secret(shares, p=PRIME):
    """Reconstruct the secret from shares using Lagrange interpolation."""
    def lagrange_basis(j, x=0):
        numerator = denominator = 1
        xj, yj = shares[j]
        for i, (xi, _) in enumerate(shares):
            if i != j:
                numerator = (numerator * (x - xi)) % p
                denominator = (denominator * (xj - xi)) % p
        return (yj * numerator * mod_inv(denominator, p)) % p

    k = len(shares)
    secret = sum(lagrange_basis(j) for j in range(k)) % p
    return secret

def int_to_bytes(i):
    """Convert an integer to bytes with fixed length to preserve leading zeros."""
    byte_length = (PRIME.bit_length() + 7) // 8
    return i.to_bytes(byte_length, byteorder='big')

def bytes_to_int(b):
    """Convert bytes to an integer."""
    return int.from_bytes(b, byteorder='big')

def split_secret(secret_bytes, m, n):
    """Split the secret bytes into shares."""
    # Embed the secret length at the beginning (4 bytes)
    secret_length = len(secret_bytes)
    if secret_length >= 2**32:
        raise ValueError("Secret is too long.")

    length_bytes = secret_length.to_bytes(4, byteorder='big')
    secret_with_length = length_bytes + secret_bytes

    # Convert secret to integer
    secret_int = bytes_to_int(secret_with_length)

    if secret_int >= PRIME:
        raise ValueError('Secret integer is too large for the finite field.')

    shares = generate_shares(secret_int, m, n)
    return shares

def recover_secret(shares):
    """Recover the secret bytes from shares."""
    secret_int = reconstruct_secret(shares)

    # Convert integer back to bytes with fixed length
    secret_bytes = int_to_bytes(secret_int)

    # Extract the original secret length
    if len(secret_bytes) < 4:
        raise ValueError("Invalid secret data.")

    length_bytes = secret_bytes[:4]
    secret_length = int.from_bytes(length_bytes, byteorder='big')

    # Extract the original secret
    secret_data = secret_bytes[4:4 + secret_length]

    return secret_data

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Shamir\'s Secret Sharing for binary data.')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Subparser for splitting the secret
    split_parser = subparsers.add_parser('split', help='Split a secret into shares')
    split_parser.add_argument('secret_file', help='File containing the secret to split')
    split_parser.add_argument('m', type=int, help='Minimum number of shares to reconstruct the secret')
    split_parser.add_argument('n', type=int, help='Total number of shares to generate')
    split_parser.add_argument('shares_prefix', help='Prefix for the share files')

    # Subparser for recovering the secret
    recover_parser = subparsers.add_parser('recover', help='Recover the secret from shares')
    recover_parser.add_argument('shares', nargs='+', help='Share files to use for recovery')
    recover_parser.add_argument('output_file', help='File to write the recovered secret')

    args = parser.parse_args()

    if args.command == 'split':
        with open(args.secret_file, 'rb') as f:
            secret_bytes = f.read()

        shares = split_secret(secret_bytes, args.m, args.n)

        # Write shares to files
        for idx, (x, y) in enumerate(shares):
            share_filename = f'{args.shares_prefix}_share_{idx+1}.txt'
            with open(share_filename, 'w') as f:
                f.write(f'{x},{y}\n')

        print(f'Successfully created {args.n} shares with threshold {args.m}.')

    elif args.command == 'recover':
        shares = []
        for share_file in args.shares:
            with open(share_file, 'r') as f:
                content = f.read().strip()
                x_str, y_str = content.split(',')
                shares.append((int(x_str), int(y_str)))

        secret_data = recover_secret(shares)

        with open(args.output_file, 'wb') as f:
            f.write(secret_data)

        print(f'Secret successfully recovered and saved to {args.output_file}.')
