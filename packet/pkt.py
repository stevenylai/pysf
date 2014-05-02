from . import base
from .types import int
from .types import subpacket

class Packet(base.Packet):
    TYPE_RFM_PKT = 0x1
    type = int.IntType(0, 4)
    header_length = int.IntType(4, 2)
    payload_length = int.IntType(6, 2)
    payload = subpacket.Subpacket(('type', 'payload'), {1: 'rfm'}, 8)
