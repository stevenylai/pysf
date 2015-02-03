'''Base panel'''
from ..device import base


class Panel(base.Device):
    '''Base panel class'''
    name = 'panel'

    def write(self, output):
        '''Write to panel'''
        pass
