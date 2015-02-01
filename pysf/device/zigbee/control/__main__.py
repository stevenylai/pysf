'''Run base control from console'''
from ..base import Device
from . import base, console


class Control(base.Control, console.Control):
    '''Base console control'''
    pass


controller = Control(Device)
controller.listen()
