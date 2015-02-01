'''RFM base device'''
from .. import base


class Device(base.Device):
    '''RFM device base'''
    def filter_packet(self, raw_packet):
        '''Filter out those non-RFM packets'''
        from ...protocol import pkt
        packet = pkt.Packet(data=raw_packet)
        if packet.type == packet.TYPE_RFM:
            return packet
        return None
