from utils import repeated_key_xor

str_to_encrypt = b'Burning \'em, if you ain\'t quick and nimble\nI go crazy when I hear a cymbal'
key = b'ICE'

expected_res = b'0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272' \
               b'a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f'

res = repeated_key_xor(plain_text=str_to_encrypt, key=key)
print(res, expected_res)
assert(res == expected_res)