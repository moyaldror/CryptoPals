from codecs import decode, encode
from collections import Counter


def hex_to_bytes(hex_str):
    '''
    :param hex_str: string that contains hexadecimal numbers
    :return: byte string with the hex representation
    '''
    return decode(hex_str, 'hex')

def bytes_to_hex(bytes_str):
    '''
    :param bytes_str: bytes string
    :return: bytes string hex encoded
    '''
    return encode(bytes_str, 'hex')


def hex_byte_to_bin(hex_byte):
    '''
    :param hex_byte: 1 byte hex value
    :return: string with the binary representation (8 chars long)
    '''
    return bin(hex_byte)[2:].zfill(8)


def bin_str_to_hex(bin_str):
    '''
    :param bin_str: string which represent a binary number
    :return: byte string with the hex value
    '''
    return bytes(hex(int(bin_str, 2))[2:].zfill(2), 'utf-8')


def xor_strings(*args):
    '''
    :param args: any number of strings or bytes strings
                 if strings - they must me hexadecimal strings, if bytes strings - all is OK
    :return: bytes strings of the xor of all the arrays (length is as the shortest string)
    '''
    ret = b''
    arrays = []
    for arg in args:
        if not isinstance(arg, bytes) and not isinstance(arg, str):
            raise Exception('Only byte string and strings are acceptable')
        if isinstance(arg, bytes):
            arrays.append(arg)
        else:
            arrays.append(decode(arg, 'hex'))

    for a in zip(*arrays):
        res = 0
        for x in a:
            res ^= x

        ret += bytes([res])

    return ret


def hamming_distance(str1, str2):
    '''
    :param str1: first string
    :param str2: second string
    :return: the hamming distance between the strings (compute against the shortest string)
    '''
    return Counter(''.join([hex_byte_to_bin(b) for b in xor_strings(str1, str2)]))['1']


if __name__ == '__main__':
    print(hamming_distance(b'this is a test', b'wokka wokka!!!'))
    assert(hamming_distance(b'this is a test', b'wokka wokka!!!') == 37)