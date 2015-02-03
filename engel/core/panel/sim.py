'''Simulated panel'''
from ..device import sim
from . import base


class Panel(sim.Device, base.Panel):
    '''Simulated panel'''
    encode = 'utf-8'

    def get_sim_data(self, prepared):
        '''Get sim data'''
        if isinstance(prepared, dict) and 'input' in prepared:
            return bytes(prepared['input'], self.encode)
        return None

    def write(self, output):
        '''Write to panel'''
        print('Written to panel:', output)
