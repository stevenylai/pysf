'''Sim device for testing'''
from engel.core.device import interruptable
from engel.core.device.sim import Device
from engel.core.code_scanner.sim import Scanner
from engel.core.panel.sim import Panel


class Light(Device, interruptable.Device):
    '''Device class'''
    name = 'light'

    def get_sim_data(self, prepared):
        '''Get sim data'''
        if isinstance(prepared, dict) and 'found' in prepared:
            return prepared['found']
        return None

    def on(self):
        '''on'''
        print("Turning on")

    def off(self):
        '''off'''
        print("Turning off")

    def level(self, level, transtime=0):
        print("Changing level to", level, 'with time', transtime)


class Scanner(Scanner, interruptable.Device):
    '''For testing'''
    pass


class Panel(Panel, interruptable.Device):
    '''For testing'''
    pass
