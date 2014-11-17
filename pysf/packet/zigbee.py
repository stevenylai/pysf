from . import base
from .types import int
from .types import subpacket

class Packet(base.Packet):
    TYPE_ZB_PAIR = 0
    TYPE_ZB_UNPAIR = 1
    TYPE_ZB_RESOLVE = 2
    TYPE_ZB_LEAVE = 3
    TYPE_ZB_BIND = 4

    TYPE_ZB_CLUSTER_COMMAND = 5
    TYPE_ZB_ATTR_READ = 6
    TYPE_ZB_ATTR_REPORT = 7
    TYPE_ZB_CFG_REPORT = 8

    type = int.IntType(0, 2)
    length = int.IntType(2, 2)
    payload = subpacket.Subpacket(('type', 'payload'),
                                  {TYPE_ZB_PAIR : 'zigbee_payload',
                                   TYPE_ZB_UNPAIR : 'zigbee_payload',
                                   TYPE_ZB_RESOLVE : 'zigbee_payload',
                                   TYPE_ZB_LEAVE : 'zigbee_payload',
                                   TYPE_ZB_BIND : 'zigbee_payload',
                                   TYPE_ZB_ATTR_READ : 'zigbee_payload',
                                   TYPE_ZB_ATTR_REPORT : 'zigbee_payload',
                                   TYPE_ZB_CLUSTER_COMMAND : 'zigbee_payload'},
                                  4)
