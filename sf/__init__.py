'''PySF package'''


def hex_byte_string(byte_array):
    '''Convert the byte array into hex string'''
    return "".join("\\x%02x" % item for item in byte_array)
