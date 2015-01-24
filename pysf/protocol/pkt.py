'''PKT protocol'''
from ..packet import base, fields


class PktHeader(fields.PacketSelector):
    '''PKT header'''
    @classmethod
    def get_packet_cls(cls, parent):
        '''Get header packet class'''
        if parent.type == parent.TYPE_RFM:
            if parent.header_length == 0:
                raise ValueError(
                    "RFM Packet header not found because "
                    "header length is 0"
                )
            from . import rfm
            return rfm.Header
        else:
            raise TypeError(
                "Header not defined for type: %s" % parent.type
            )


class PktPayload(fields.PacketSelector):
    '''PKT payload'''
    @classmethod
    def get_packet_cls(cls, parent):
        '''Get payload packet class'''
        self.offset = parent.META_HEADER_LENGTH + \
                      parent.header_length
        if parent.type == parent.TYPE_RFM:
            from . import rfm
            return rfm.Payload
        elif parent.type == parent.TYPE_ZIGBEE:
            from . import zigbee
            return zigbee.Payload
        else:
            raise TypeError(
                "Payload not defined for type: %s" % parent.type
            )

class Packet(base.Packet):
    '''PKT structure'''
     TYPE_RFM = 0x1
     TYPE_ZIGBEE = 0x10002
     META_HEADER_LENGTH = 8

     type = fields.SizedHex(length=4)
     header_length = fields.SizedHex(length=2)
     payload_length = fields.SizedHex(length=2)
     header = PktHeader()
     payload = PktPayload()
