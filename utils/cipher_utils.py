from Crypto.Cipher import AES
from utils.arrays_utils import get_blocks
from utils.hex_utils import hex_to_bytes, xor_strings
from utils.pkcs7 import pad, unpad
from sys import maxsize


default_aes_block_size = 16


def detect_ecb_line(cipher_text):
    '''
    :param cipher_text: hexdecimal bytes string or string
    :return: number of unique blocks, line number and the cipher it self as a tuple
    '''
    min_unique_blocks = maxsize
    cipher_res = None
    cipher_line = 0

    for line_number, cipher in enumerate(cipher_text):
        if isinstance(cipher, bytes):
            cipher = cipher.decode('utf-8')
        unique_blocks = len(set(get_blocks(arr=hex_to_bytes(cipher.strip()), block_size=default_aes_block_size)))
        if unique_blocks < min_unique_blocks:
            min_unique_blocks = unique_blocks
            cipher_res = bytes(cipher.strip(), 'utf-8')
            cipher_line = line_number + 1

    return min_unique_blocks, cipher_line, cipher_res


def encrypt_ecb(plain_text, key):
    return AES.new(key=key, mode=AES.MODE_ECB).encrypt(plain_text)


def decrypt_ecb(cipher_text, key):
    return AES.new(key=key, mode=AES.MODE_ECB).decrypt(cipher_text)


class AesEcb(object):
    def __init__(self, key, iv):
        self.__key = key

    def encrypt(self, plain_text):
        return AES.new(key=self.__key, mode=AES.MODE_ECB).encrypt(pad(data=plain_text, block_size=AES.block_size))

    def decrypt(self, cipher_text):
        return unpad(data=AES.new(key=self.__key, mode=AES.MODE_ECB).decrypt(cipher_text))

    def __repr__(self):
        return 'AES ECB'

    def __str__(self):
        return 'AES ECB'


class AesCbc(object):
    def __init__(self, key, iv):
        self.__key = key
        self.__iv = iv

    def __block_encrypt_ecb(self, plain_text):
        return encrypt_ecb(plain_text=plain_text, key=self.__key)

    def __block_decrypt_ecb(self, cipher_text):
        return decrypt_ecb(cipher_text=cipher_text, key=self.__key)

    def encrypt(self, plain_text):
        data = pad(data=plain_text, block_size=AES.block_size)
        cipher = []
        iv = self.__iv
        for block in get_blocks(arr=data, block_size=AES.block_size):
            iv = self.__block_encrypt_ecb(plain_text=xor_strings(iv, block))
            cipher.append(iv)

        return b''.join(cipher)

    def decrypt(self, cipher_text):
        plain = []
        iv = self.__iv
        for block in get_blocks(arr=cipher_text, block_size=AES.block_size):
            plain.append(hex_to_bytes(xor_strings(iv, self.__block_decrypt_ecb(cipher_text=block))))
            iv = block

        plain[len(plain) - 1] = unpad(data=plain[len(plain) - 1])
        return b''.join(plain)

    def __repr__(self):
        return 'AES CBC'

    def __str__(self):
        return 'AES CBC'
