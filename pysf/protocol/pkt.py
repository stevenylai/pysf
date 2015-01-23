'''PKT protocol'''
from ..packet import base, fields


class Packet(base.Packet):
    '''PKT structure'''
     TYPE_RFM_PKT = 0x1
     TYPE_ZIGBEE = 0x10002
