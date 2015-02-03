'''Simulated panel'''
from ..device import sim
from . import base


class Panel(sim.Device, base.Panel):
    '''Simulated panel'''
    encode = 'utf-8'

    def update(self, data):
        '''Update simulated data'''
        if isinstance(data, dict) and 'input' in data:
            for future in self.readers:
                future.set_result(bytes(data['input'], self.encode))

    def write(self, output):
        '''Write to panel'''
        print('Written to panel:', output)
