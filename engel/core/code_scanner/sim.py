'''Simulated scanner'''
from ..device import sim
from . import base


class Scanner(sim.Device, base.Scanner):
    '''Simulated scanner'''
    encode = 'utf-8'

    def update(self, data):
        '''Update simulated data'''
        if isinstance(data, dict) and 'code' in data:
            for future in self.readers:
                future.set_result(bytes(data['code'], self.encode))
