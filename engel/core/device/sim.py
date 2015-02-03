'''Simulated device'''
from . import base


class Device(base.Device):
    '''Sim device class'''
    name = 'device'

    def update(self, data):
        '''Update simulated data'''
        pass
