from utils import encode_base64, hex_to_bytes

bytes_to_encode = hex_to_bytes('49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d')

expected_result = b'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'

print(encode_base64(hex_bytes=bytes_to_encode), expected_result)
assert(encode_base64(hex_bytes=bytes_to_encode) == expected_result)
