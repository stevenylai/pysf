'''Zigbee protocol package'''
from ...packet import base, fields


class ZigbeePayload(fields.PacketSelector):
    '''Zigbee sub-payload'''
    def get_packet_cls(self, parent):
        '''Get packet class according to paren't type'''
        if parent.type in {parent.TYPE_PAIR, parent.TYPE_UNPAIR,
                           parent.TYPE_RESOLVE, parent.TYPE_LEAVE}:
            from . import addr_info
            return addr_info.Packet
        if parent.type in {parent.TYPE_BIND}:
            from . import bind
            return bind.Packet
        if parent.type in {parent.TYPE_CLUSTER_COMMAND}:
            from . import command
            return command.Packet
        if parent.type in {parent.TYPE_ATTR_READ, parent.TYPE_ATTR_REPORT}:
            from . import attribute
            return attribute.Packet


class Payload(base.Packet):
    '''Zigbee top-level payload'''
    TYPE_PAIR = 0
    TYPE_UNPAIR = 1
    TYPE_RESOLVE = 2
    TYPE_LEAVE = 3
    TYPE_BIND = 4
    TYPE_CLUSTER_COMMAND = 5
    TYPE_ATTR_READ = 6
    TYPE_ATTR_REPORT = 7

    STATUS_REQ = 0
    STATUS_OK = 1
    STATUS_UNKNOWN_CMD = 2
    STATUS_TOO_MANY_PAIRED = 3
    STATUS_NETWORK_ERROR = 4

    type = fields.SizedHex(length=2)
    length = fields.SizedHex(length=2)
    status = fields.SizedHex(length=1)
    payload = ZigbeePayload()


class Address(base.Packet):
    '''Zigbee adress'''
    ADDR_NOT_PRESENT = 0
    ADDR_GROUP = 1
    ADDR_16BIT = 2
    ADDR_64BIT = 3
    ADDR_BROADCAST = 15

    short_addr = fields.SizedHex(length=2, offset=0)
    mac = fields.SizedHex(length=8, offset=0)
    mode = fields.SizedHex(length=1)
    end_point = fields.SizedHex(length=1)
    pan_id = fields.SizedHex(length=2)


class AddressField(fields.PacketSelector):
    '''Address selector'''
    def __init__(self, length=None, offset=None, name=None):
        super().__init__(length, offset, name)
        self._length = 12

    def get_packet_cls(self, parent):
        return Address
