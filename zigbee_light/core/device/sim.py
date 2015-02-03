'''Sim device for testing'''
from engel.core.device import interruptable, sim


class Device(sim.Device. interruptable.Device):
    '''Device class'''
    name = 'light'

    def update(self, data):
        '''Update data'''
        if isinstance(data, dict) and 'found' in data:
            for future in self.readers:
                future.set_result(data['found'])
            self.readers.clear()
