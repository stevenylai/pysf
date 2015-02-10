'''Zigbee light command line control'''
from ..control import console
from . import control


class Control(control.Control, console.Control):
    '''Console control class'''
    pass

if __name__ == '__main__':
    from . import Device
    controller = Control(Device)
    controller.listen()
