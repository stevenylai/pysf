'''Zigbee bind packet module'''
from ...packet import base, fields


class Packet(base.Packet):
    '''Bind packet'''
    TYPE_BIND_BIND = 0
    TYPE_BIND_UNBIND = 1
    TYPE_BIND_ACK = 2
    TYPE_BINE_NACK = 3

    type = fields.SizedHex(length=1)
    end_point = fields.SizedHex(length=1)
    cluster_id = fields.SizedHex(length=2)
    mac = fields.SizedHex(length=8)
    addr = fields.SizedHex(length=2)
