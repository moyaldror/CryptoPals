from codecs import encode
from random import randint, _urandom

from utils.cipher_utils import AesCbc, AesEcb, detect_ecb_line

enc_options = [(AesEcb, 'AES ECB'), (AesCbc, 'AES CBC')]


def detect_ecb_or_cbc(cipher_text, block_size):
    '''
    :param cipher_text: cipher text we want to figure out its encryption mode as bytes string
    :param block_size: block size used
    :return: encryption mode detected - 'AES ECB' or 'AES CBC'
    '''
    unique_blocks, a, b = detect_ecb_line(cipher_text=[encode(cipher_text, 'hex')])

    if unique_blocks and unique_blocks < (len(cipher_text) // block_size):
        return enc_options[0][1]
    else:
        return enc_options[1][1]


def random_key_ecb_enc_dec(prefix_text, postfix_text):
    '''
    :param prefix_text: bytes string to pre-append to each call to encrypt
    :param postfix_text: bytes string to post-append to each call to encrypt
    :return: enc - encryption function, dec - decryption function
    '''
    key = _urandom(16)
    aes = AesEcb(key=key, iv=None)

    def encrypt(plain_text):
        return aes.encrypt(plain_text=prefix_text + plain_text + postfix_text)

    return encrypt, aes.decrypt


def encryption_oracle(user_input):
    '''
    :param user_input: user input as bytes string
    :return: the encryption method detected and the actual encryption used as a tuple
    '''
    block_size = 16

    def random_encrypt_data():
        key = _urandom(block_size)
        iv = _urandom(block_size)
        encryption, encryption_str = enc_options[randint(0, 1)]
        data_to_encrypt = b''.join([_urandom(randint(5, 10)), user_input, _urandom(randint(5, 10))])

        return encryption(key=key, iv=iv).encrypt(plain_text=data_to_encrypt), encryption_str

    enc_data, enc_used = random_encrypt_data()
    return detect_ecb_or_cbc(cipher_text=enc_data, block_size=block_size), enc_used
