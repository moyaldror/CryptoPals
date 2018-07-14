from utils import pad

data_to_pad = b'YELLOW SUBMARINE'
block_size = 20

print(pad(data=data_to_pad, block_size=block_size))
assert(pad(data=data_to_pad, block_size=block_size) == b'YELLOW SUBMARINE\x04\x04\x04\x04')