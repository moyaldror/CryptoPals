from utils import encryption_oracle


enc_detected, enc_used = encryption_oracle(user_input=b'a'*100)
print('Encryption detected:', enc_detected, '\nEncryption used:', enc_used)
assert(enc_detected == enc_used)