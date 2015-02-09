'''Sim device for testing'''
from engel.core.device import interruptable
from engel.core.device.sim import Device
from engel.core.code_scanner.sim import Scanner as SimScanner
from engel.core.panel.sim import Panel as SimPanel


class Light(Device, interruptable.Device):
    '''Device class'''
    name = 'light'

    def get_sim_data(self, prepared):
        '''Get sim data'''
        if isinstance(prepared, dict) and 'found' in prepared:
            return prepared['found']
        return None

    def clear(self):
        '''Clear'''
        print('Cleared')

    def on(self):
        '''on'''
        print("Turning on")

    def off(self):
        '''off'''
        print("Turning off")

    def level(self, level, transtime=0):
        '''Changing level'''
        print("Changing level to", level, 'with time', transtime)


class Scanner(SimScanner, interruptable.Device):
    '''For testing'''
    pass


class Panel(SimPanel, interruptable.Device):
    '''For testing'''
    pass
