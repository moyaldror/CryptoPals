from codecs import encode
from random import randint, _urandom
from utils.cipher_utils import AesCbc, AesEcb, detect_ecb_line


enc_options = [(AesEcb, 'AES ECB'), (AesCbc, 'AES CBC')]


def detect_ecb_or_cbc(cipher_text):
    unique_blocks, a, b = detect_ecb_line(cipher_text=[encode(cipher_text, 'hex')])
    if unique_blocks < (len(cipher_text) // 16):
        return enc_options[0][1]
    else:
        return enc_options[1][1]


def encryption_oracle(user_input):
    '''
    :param user_input: user input as bytes string
    :return: the encryption method detected and the actual encryption used as a tuple
    '''
    def random_encrypt_data():
        key = _urandom(16)
        iv = _urandom(16)
        encryption, encryption_str = enc_options[randint(0, 1)]
        data_to_encrypt = b''.join([_urandom(randint(5, 10)), user_input, _urandom(randint(5, 10))])

        return encryption(key=key, iv=iv).encrypt(plain_text=data_to_encrypt), encryption_str

    enc_data, enc_used = random_encrypt_data()
    return detect_ecb_or_cbc(cipher_text=enc_data), enc_used
