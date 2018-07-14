from utils import decode_base64, decrypt_ecb, encrypt_ecb, hex_to_bytes
from resources import RESOURCES_PATH

with open(RESOURCES_PATH + '7.txt', 'r') as f:
    lines = f.readlines()

key = b'YELLOW SUBMARINE'
encrypted_data = hex_to_bytes(decode_base64(b''.join(bytes(line.strip(), 'utf-8') for line in lines)))
print(decrypt_ecb(key=key, cipher_text=encrypted_data).decode('utf-8'))

test_str = b'GANAN    GIDEL    DAGAN    BAGAN'
assert(decrypt_ecb(key=key, cipher_text=encrypt_ecb(key=key, plain_text=test_str)) == test_str)