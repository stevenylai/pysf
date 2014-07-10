from .types import int
from . import zigbee_simple

class Packet(zigbee_simple.Packet):
    status = int.IntType(0, 1)
    data = int.IntType(1, 1)
