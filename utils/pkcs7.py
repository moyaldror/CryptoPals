class BadPaddingException(Exception):
    def __init__(self, padding):
        super().__init__('Bad Padding: {}'.format(padding))


def pad(data, block_size):
    '''
    :param data: data as bytes string
    :param block_size: block size to use
    :return: padded data
    '''
    padding_size = block_size - (len(data) % block_size)
    padding = bytes([padding_size]*padding_size)
    return data + padding


def unpad(data):
    '''
    :param data: data as bytes string
    :return: if data has legal padding the data unpadded, else raise BadPaddingException
    '''
    padding_size = data[len(data) - 1]
    padding_start_position = len(data) - padding_size
    padding = bytes([padding_size]*padding_size)
    if padding != data[padding_start_position:]:
        raise BadPaddingException(padding=data[padding_start_position:])

    return data[:padding_start_position]
