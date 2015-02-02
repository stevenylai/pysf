'''Interrruptable device'''
from . import base


class Device(base.Device):
    '''Interruptable device'''
    def interrupt(self, exc=None):
        '''Interrupt the device with an exception'''
        if exc is None:
            exc = InterruptedError('Interrupted')
        for future in self.readers:
            future.set_exception(exc)
