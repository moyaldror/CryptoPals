from utils import decode_base64, hex_to_bytes, byte_byte_ecb_break

unknown_string = b'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcy' \
                 b'BvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK'

hex_decoded = hex_to_bytes(decode_base64(unknown_string))

print(byte_byte_ecb_break(unknown_str=hex_decoded, hard=True))
assert (byte_byte_ecb_break(unknown_str=hex_decoded, hard=True) == hex_decoded)