from codecs import encode
from utils import detect_ecb_line, encrypt_ecb
from resources import RESOURCES_PATH

with open(RESOURCES_PATH + '8.txt', 'r') as f:
    lines = f.readlines()

print(detect_ecb_line(cipher_text=lines))
data_to_enc = b'a'*16*16
assert(detect_ecb_line(
    cipher_text=[encode(encrypt_ecb(key=b'B'*16, plain_text=data_to_enc), 'hex').decode('utf-8')])[0] == 1)
