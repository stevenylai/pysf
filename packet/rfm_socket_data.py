from . import base
from .types import int

class Packeter(base.Packeter):
    voltage = int.IntType(0, 2)
    current = int.IntType(2, 2)
    power = int.IntType(4, 3)
    freq = int.IntType(7, 1)
