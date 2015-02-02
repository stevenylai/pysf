'''Sim device for testing'''
from engel.core.device import interruptable, sim


class Device(sim.Device. interruptable.Device):
    '''Device class'''
    def update(self, data):
        '''Update data'''
        if 'found' in data:
            for future in self.readers:
                future.set_result(data['found'])
            self.readers.clear()
