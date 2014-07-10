from . import base
from .types import int
from .types import subpacket

class Packet(base.Packet):
    TYPE_ZB_PAIR = 0
    TYPE_ZB_UNPAIR = 1
    TYPE_ZB_ON = 2
    TYPE_ZB_OFF = 3
    TYPE_ZB_LEVEL = 4
    mac_addr = int.IntType(0, 8)
    end_point = int.IntType(8, 1)
    type = int.IntType(9, 2)
    seq = int.IntType(11, 2)
    length = int.IntType(13, 2)
    payload = subpacket.Subpacket(('type', 'payload'),
                                  {TYPE_ZB_PAIR : 'zigbee_simple',
                                   TYPE_ZB_UNPAIR : 'zigbee_simple',
                                   TYPE_ZB_ON : 'zigbee_simple',
                                   TYPE_ZB_OFF : 'zigbee_simple',
                                   TYPE_ZB_LEVEL : 'zigbee_simple'},
                                  15)
