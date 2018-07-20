from random import choice, _urandom

from utils import AesEcb

users = ['root', 'admin', 'oper', 'user']


def kv_to_dict(kv):
    if isinstance(kv, bytes):
        kv = kv.decode('utf-8')
    return {kv[0]: kv[1] for kv in [token.split('=') for token in kv.split('&')]}


def dict_to_kv(dict):
    res = []
    for k, v in dict.items():
        res.append('='.join([k, v]))

    return bytes('&'.join(res), 'utf-8')


def profile_for(email):
    email = email.replace('=', '').replace('&', '')
    return dict_to_kv({
        'email': email,
        'uid': '%d' % (len(email) - 1),
        'role': choice(users)
    })


def profile_enc_dec():
    key = _urandom(16)
    aes = AesEcb(key=key, iv=None)

    def encrypt(plain_text):
        return aes.encrypt(plain_text=plain_text)

    def decrypt(cipher_text):
        return kv_to_dict(kv=aes.decrypt(cipher_text=cipher_text))

    return encrypt, decrypt


# using the following email address the encoded profile will look like
# email=foo12@bar.com&uid=13&role= which is exactly 2 block long
# once we have the encrypted profile we will replace the last block to encrypted admin

profile = None
while True:
    profile = profile_for(email='foo12@bar.com')
    if not profile.endswith(b'admin'):
        break

admin_profile = None
while True:
    admin_profile = profile_for(email='foo11@bar.com')
    if admin_profile.endswith(b'admin'):
        break


enc, dec = profile_enc_dec()

enc_profile = enc(plain_text=profile)
enc_admin_profile = enc(plain_text=admin_profile)[16*2:]
print(dec(cipher_text=enc_profile[:16*2] + enc_admin_profile))
assert(dec(cipher_text=enc_profile[:16*2] + enc_admin_profile) ==
       {'email': 'foo12@bar.com', 'uid': '12', 'role': 'admin'})