'''Scanner reader'''
from ..device import reader


class Reader(reader.Reader):
    '''Reader class'''
    def emit_result(self, result):
        '''Process the read result'''
        print('Scanned:', result)
