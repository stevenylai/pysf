'''Simulated scanner'''
from ..device import sim
from . import base


class Scanner(sim.Device, base.Scanner):
    '''Simulated scanner'''
    encode = 'utf-8'

    def get_sim_data(self, prepared):
        '''Get sim data'''
        if isinstance(prepared, dict) and 'code' in prepared:
            return prepared['code']
        return None
