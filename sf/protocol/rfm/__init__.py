'''RFM protocol'''
from ...packet import base, fields


def toggled_type(rfm_type):
    '''Toggle rfm type'''
    return rfm_type ^ 0x80


class RfmPayload(fields.PacketSelector):
    '''RFM payload'''
    def get_packet_cls(self, parent):
        '''Get payload packet class'''
        if parent.type == parent.TYPE_SOCKET_POWER:
            from . import socket_power
            return socket_power.Packet
        elif parent.type == parent.TYPE_SOCKET_STATUS or \
        toggled_type(parent.type) == parent.TYPE_SOCKET_STATUS:
            from . import socket_status
            return socket_status.Packet
        else:
            return base.BarePayload


class Payload(base.Packet):
    '''RFM payload'''
    ADDR_RFM_BCAST = 0x181818
    TYPE_SOCKET_POWER = 0x26
    TYPE_SOCKET_STATUS = 0x20
    TYPE_EXIST = 0x10

    src = fields.SizedHex(length=3)
    type = fields.SizedHex(length=1)
    dest = fields.SizedHex(length=3)
    length = fields.SizedHex(length=1)
    payload = RfmPayload()


class Header(base.Packet):
    '''RFM header'''
    RFM_HEADER_RSSI = 0
    type = fields.SizedHex(length=1)
    rssi = fields.SizedHex(length=1)
