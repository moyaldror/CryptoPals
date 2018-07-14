from base64 import b64encode
from utils.arrays_utils import get_blocks
from utils.hex_utils import hex_byte_to_bin, bin_str_to_hex, hex_to_bytes
from utils.misc import CONSTANTS

BASE64_TBL = ''.join([*CONSTANTS.ABC, *CONSTANTS.abc, *CONSTANTS.numbers, '+', '/'])


def base64_char_to_bin(base64_char):
    '''
    :param base64_char: valid base64 character
    :return: string with the binary representation (6 chars long)
    '''
    return bin(BASE64_TBL.index(base64_char))[2:].zfill(6)


def pad_base64_bytes(hex_bytes):
    '''
    :param hex_bytes: byte string that contains hexadecimal numbers
    :return: the byte string with 1 or 2 padded bytes (bytes are 0)
    '''
    pad = 3 - (len(hex_bytes) % 3) if len(hex_bytes) % 3 != 0 else 0
    return hex_bytes + bytes([0] * pad), pad


def encode_base64(hex_bytes):
    '''
    :param hex_bytes: bytes string that contains hexadecimal numbers
    :return: byte string base64 representation of the input hex bytes
    '''
    ret = b''
    bytes_in_block = 3
    padded, padded_bytes = pad_base64_bytes(hex_bytes=hex_bytes)
    bits_encode = 0

    for block in get_blocks(arr=padded, block_size=bytes_in_block):
        bin_arr = ''.join([hex_byte_to_bin(block[i]) for i in range(bytes_in_block)])
        for bin_block in get_blocks(arr=bin_arr, block_size=6):
            ret += bytes(BASE64_TBL[int(bin_block, 2)], 'utf-8') if bits_encode <= (len(padded)*8 - (padded_bytes*8))\
                else bytes('=', 'utf-8')

            bits_encode += 6

    return ret


def decode_base64(base64_bytes):
    '''
    :param base64_bytes: base64 bytes string
    :return: bytes string of the decoded base64 bytes in hexadecimal
    '''
    chars_in_block = 4
    ret = b''

    for block in get_blocks(arr=base64_bytes, block_size=chars_in_block):
        bin_bits_to_trim = block.count(b'=') * 2
        bin_arr = ''.join([base64_char_to_bin(base64_char=chr(c)) for c in block if c != ord('=')])
        bin_arr = bin_arr[:len(bin_arr) - bin_bits_to_trim]
        for bin_block in get_blocks(arr=bin_arr, block_size=8):
            ret += bin_str_to_hex(bin_str=bin_block)

    return ret


if __name__ == '__main__':
    print(BASE64_TBL)
    hex_str = '20814804c1767293b99f1d9cab3b'
    hex_bytes = hex_to_bytes(hex_str)
    padded_hex_bytes = pad_base64_bytes(hex_bytes)
    base64_encoded = encode_base64(hex_bytes)
    base64_decoded = decode_base64(base64_encoded)

    results = [hex_str, hex_bytes, padded_hex_bytes, base64_encoded, base64_decoded]

    for i, res in enumerate(results):
        print(i, res)

    assert(base64_encoded == b64encode(hex_bytes))
    assert(base64_decoded == bytes(hex_str, 'utf-8'))

