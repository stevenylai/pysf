'''Simulated device'''
import asyncio
from . import base


class Device(base.Device):
    '''Sim device class'''
    def __init__(self, event_loop):
        '''Create sim device'''
        super().__init__(event_loop)
        self.prepared_data = None

    def update(self, data):
        '''Update simulated data'''
        self.prepared_data = data
        for future in self.readers:
            future.set_result(self.get_sim_data(self.prepared_data))
        self.readers.clear()

    def get_sim_data(self, prepared):
        '''Get sim data'''
        return prepared

    def read(self):
        '''Read from device'''
        if self.prepared_data is not None:
            prepared = self.get_sim_data(self.prepared_data)
            self.prepared_data = None
            future = asyncio.Future()
            future.set_result(prepared)
            return future
        else:
            return super().read()
