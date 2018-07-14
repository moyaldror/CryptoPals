from utils import repeated_key_xor_breaker, decode_base64
from resources import RESOURCES_PATH

with open(RESOURCES_PATH + '6.txt', 'r') as f:
    lines = f.readlines()

encrypted_data = decode_base64(b''.join(bytes(line.strip(), 'utf-8') for line in lines))
decrypted_text, key = repeated_key_xor_breaker(encrypted_data)
print(decrypted_text.decode('utf-8'), key)
assert(key == b'Terminator X: Bring the noise')