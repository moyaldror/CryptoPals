from utils import AesCbc, decode_base64, hex_to_bytes
from resources import RESOURCES_PATH

with open(RESOURCES_PATH + '10.txt', 'r') as f:
    lines = f.readlines()

key = b'YELLOW SUBMARINE'
iv = b'\x00'*16

encrypted_data = hex_to_bytes(decode_base64(b''.join(bytes(line.strip(), 'utf-8') for line in lines)))
aes = AesCbc(key=key, iv=iv)

print(aes.decrypt(cipher_text=encrypted_data).decode('utf-8'))
assert(aes.decrypt(cipher_text=encrypted_data).decode('utf-8').startswith('I\'m back and'))