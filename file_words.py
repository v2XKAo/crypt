from base import get_wordlist


def file_to_words(filename):
    import struct
    wordlist = get_wordlist()
    with open(filename, 'rb') as f:
        data = f.read()

    # Prepend data length (4 bytes)
    data_length = len(data)
    # 4 bytes, big-endian unsigned int
    data_length_bytes = struct.pack('>I', data_length)
    data_with_length = data_length_bytes + data

    # Convert data to bits
    data_bits = ''.join(f'{byte:08b}' for byte in data_with_length)

    # Pad the bits to multiple of 11 bits
    padding_length = (11 - (len(data_bits) % 11)) % 11
    data_bits += '0' * padding_length

    # Split into 11-bit chunks
    chunks = [data_bits[i:i+11] for i in range(0, len(data_bits), 11)]

    # Map each chunk to a word
    words = [wordlist[int(chunk, 2)] for chunk in chunks]

    return words


def words_to_file(words, output_filename):
    import struct
    wordlist = read_wordlist()
    word_to_index = {word: index for index, word in enumerate(wordlist)}

    # Map words back to bits
    bits = ''.join(f'{word_to_index[word]:011b}' for word in words)

    # Convert bits back to bytes
    # Truncate bits to full bytes (multiple of 8 bits)
    num_full_bytes = len(bits) // 8
    bits = bits[:num_full_bytes * 8]
    data_with_length = int(bits, 2).to_bytes(num_full_bytes, byteorder='big')

    # Extract data length
    data_length_bytes = data_with_length[:4]
    data_length = struct.unpack('>I', data_length_bytes)[0]

    # Extract original data
    data = data_with_length[4:4+data_length]

    # Write to output file
    with open(output_filename, 'wb') as f:
        f.write(data)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Convert a binary file to words and back.')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Subparser for encoding
    encode_parser = subparsers.add_parser(
        'encode', help='Encode a file to words')
    encode_parser.add_argument('input_file', help='Input file to encode')
    encode_parser.add_argument(
        'output_words_file', help='Output file to write words')

    # Subparser for decoding
    decode_parser = subparsers.add_parser(
        'decode', help='Decode words back to file')
    decode_parser.add_argument(
        'input_words_file', help='Input file containing words')
    decode_parser.add_argument(
        'output_file', help='Output file to write decoded data')

    args = parser.parse_args()

    if args.command == 'encode':
        words = file_to_words(args.input_file)
        with open(args.output_words_file, 'w', encoding='utf-8') as f:
            f.write(' '.join(words))
            f.write('\n')  # Newline at the end
    elif args.command == 'decode':
        with open(args.input_words_file, 'r', encoding='utf-8') as f:
            content = f.read().strip().split()
            words = content
        words_to_file(words, args.output_file)
