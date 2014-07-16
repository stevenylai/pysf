from . import base
from .types import int
from .types import subpacket

class Packet(base.Packet):
    TYPE_ZB_PAIR = 0
    TYPE_ZB_UNPAIR = 1
    TYPE_ZB_ON = 2
    TYPE_ZB_OFF = 3
    TYPE_ZB_LEVEL = 4

    TYPE_ZB_RESOLVE = 5
    TYPE_ZB_LEAVE = 6
    TYPE_ZB_QUERY_ON_OFF = 7
    TYPE_ZB_QUERY_LEVEL = 8

    addr = int.IntType(0, 2)
    end_point = int.IntType(2, 1)
    type = int.IntType(3, 2)
    length = int.IntType(5, 2)
    payload = subpacket.Subpacket(('type', 'payload'),
                                  {TYPE_ZB_PAIR : 'zigbee_simple',
                                   TYPE_ZB_UNPAIR : 'zigbee_simple',
                                   TYPE_ZB_RESOLVE : 'zigbee_simple',
                                   TYPE_ZB_LEAVE : 'zigbee_simple',
                                   TYPE_ZB_ON : 'zigbee_simple',
                                   TYPE_ZB_OFF : 'zigbee_simple',
                                   TYPE_ZB_LEVEL : 'zigbee_simple',
                                   TYPE_ZB_QUERY_ON_OFF : 'zigbee_simple',
                                   TYPE_ZB_QUERY_LEVEL : 'zigbee_simple'},
                                  7)
