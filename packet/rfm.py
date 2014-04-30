from . import base
from .types import int
from .types import subpacket

RFM_SOCKET_DATA = 0x26
RFM_SOCKET_STATUS = 0x20
RFM_SOCKET_EXIST = 0x10

class Packeter(base.Packeter):
    src = int.IntType(0, 3)
    dest = int.IntType(4, 3)
    type = int.IntType(3, 1)
    length = int.IntType(7, 1)
    payload = subpacket.Subpacket(('type', 'payload'),
                                  {RFM_SOCKET_DATA : 'rfm_socket_data',
                                   RFM_SOCKET_STATUS : 'rfm_socket_status',
                                   RFM_SOCKET_EXIST : 'rfm_socket_status'},
                                  8)
