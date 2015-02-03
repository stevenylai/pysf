'''Simulated panel'''
from ..device import Sim


class Panel(sim.Device):
    '''Simulated panel'''
    encode = 'utf-8'

    def update(self, data):
        '''Update simulated data'''
        if isinstance(data, dict) and 'input' in data:
            for future in self.readers:
                future.set_result(bytes(data['input'], self.encode))
