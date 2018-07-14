
def get_blocks(arr, block_size):
    '''
    :param arr: array of some type
    :param block_size: block size to use
    :return: generator of blocks with block size from the given array
    '''
    return (arr[i:i+block_size] for i in range(0, len(arr), block_size))
