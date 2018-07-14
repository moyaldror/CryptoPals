from utils import single_byte_xor_breaker
from resources import RESOURCES_PATH

with open(RESOURCES_PATH + '4.txt', 'r') as f:
    ciphers = f.readlines()

max_printables = 0
single_xor_line = None
for cipher in ciphers:
    cipher = cipher.strip()

    decrypted_text, key, dec_printables = single_byte_xor_breaker(hex_str=cipher)
    if dec_printables > max_printables:
        single_xor_line, max_printables = decrypted_text, dec_printables

print(single_xor_line)
assert(single_xor_line == b'Now that the party is jumping\n')