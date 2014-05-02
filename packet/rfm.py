from . import base
from .types import int
from .types import subpacket

class Packet(base.Packet):
    ADDR_BCAST = 0x181818
    TYPE_SOCKET_DATA = 0x26
    TYPE_SOCKET_STATUS = 0x20
    TYPE_SOCKET_EXIST = 0x10
    src = int.IntType(0, 3)
    dest = int.IntType(4, 3)
    type = int.IntType(3, 1)
    length = int.IntType(7, 1)
    payload = subpacket.Subpacket(('type', 'payload'),
                                  {TYPE_SOCKET_DATA : 'rfm_socket_data',
                                   TYPE_SOCKET_STATUS : 'rfm_socket_status',
                                   TYPE_SOCKET_EXIST : 'rfm_socket_status'},
                                  8)
