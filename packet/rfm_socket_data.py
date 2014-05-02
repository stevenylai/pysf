from . import base
from .types import int

class Packet(base.Packet):
    voltage = int.IntType(0, 2)
    current = int.IntType(2, 2)
    power = int.IntType(4, 3)
    freq = int.IntType(7, 1)
