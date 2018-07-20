from utils import xor_strings, bytes_to_hex

str1 = '1c0111001f010100061a024b53535009181c'
str2 = '686974207468652062756c6c277320657965'

expected_res = b'746865206b696420646f6e277420706c6179'


print(bytes_to_hex(xor_strings(str1, str2)), expected_res)
assert(bytes_to_hex(xor_strings(str1, str2)) == expected_res)