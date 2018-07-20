from operator import itemgetter

from utils.arrays_utils import get_blocks
from utils.hex_utils import hex_to_bytes, bytes_to_hex, xor_strings, hamming_distance
from utils.misc import CONSTANTS


def count_printables(src_str):
    '''
    :param src_str: string to process
    :return: number of printable characters
    '''
    printable_chars = 0
    for c in src_str:
        if c in bytes(CONSTANTS.printables, 'utf-8'):
            printable_chars += 1

    return printable_chars


def single_byte_xor_breaker(hex_str):
    '''
    :param hex_str: hexadecimal encoded and single byte XORed string
    :return: the decryption, the single byte key and number of printable characters as a tuple
    '''
    key_byte = 0
    hex_bytes = hex_to_bytes(hex_str)

    max_printables = 0
    for i in range(256):
        temp_str = bytes([i])*len(hex_bytes)

        dec_printables = count_printables(xor_strings(temp_str, hex_bytes))
        if dec_printables > max_printables:
            max_printables, key_byte = dec_printables, i

    return xor_strings(bytes([key_byte]) * len(hex_bytes), hex_bytes), key_byte, max_printables


def repeated_key_xor(plain_text, key):
    '''
    :param plain_text: plain text to encrypt as bytes string
    :param key: key to encrypt with as bytes string
    :return: encrypted message as byte string
    '''
    def build_repeated_xor_key(key, plain_text_len):
        return b''.join([key] * ((plain_text_len // len(key)) + (plain_text_len % len(key))))

    return bytes_to_hex(xor_strings(plain_text, build_repeated_xor_key(key=key, plain_text_len=len(plain_text))))


def repeated_key_xor_breaker(cipher_text):
    '''
    :param cipher_text: cipher text as hexadecimal bytes string
    :return: decryption of the cipher text as bytes string
    '''
    def find_key_size(cipher_text, start_range, end_range):
        distances = []
        for key_size in range(start_range, end_range):
            blocks = list(get_blocks(arr=cipher_text, block_size=key_size))
            hamming_distance_sum = 0
            for b1, b2 in zip(blocks[::2], blocks[1::2]):
                hamming_distance_sum += hamming_distance(b1, b2)
            distances.append((key_size, ((hamming_distance_sum/len(blocks)/2)/key_size)))

        return sorted(distances, key=itemgetter(1))[0]

    key = []
    cipher_text_hex_bytes = hex_to_bytes(cipher_text)
    key_size = find_key_size(cipher_text=cipher_text_hex_bytes, start_range=2, end_range=41)[0]
    blocks = [list(block) for block in get_blocks(arr=cipher_text_hex_bytes, block_size=key_size)
              if len(block) == key_size]

    for block in zip(*blocks):
        key.append(single_byte_xor_breaker(bytes_to_hex(bytes([x for x in block])))[1])

    return hex_to_bytes(repeated_key_xor(plain_text=hex_to_bytes(cipher_text), key=bytes(key))), bytes(key)


if __name__ == '__main__':
    str_to_break = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
    print(single_byte_xor_breaker(str_to_break))
    str_to_encrypt = b'Burning \'em, if you ain\'t quick and nimble\nI go crazy when I hear a cymbal'*100
    key = b'ICE'
    print(repeated_key_xor_breaker(cipher_text=repeated_key_xor(plain_text=str_to_encrypt, key=key))[:len(str_to_encrypt)//100])
    assert(repeated_key_xor_breaker(cipher_text=repeated_key_xor(plain_text=str_to_encrypt, key=key)) == str_to_encrypt)
