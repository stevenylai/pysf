'''Zigbee device'''
from .. import base


class Device(base.Device):
    '''Zigbee base device'''
    def filter_packet(self, raw_packet):
        '''Filter out those non-Zigbee packets'''
        from ...protocol import pkt
        packet = pkt.Packet(data=raw_packet)
        if packet.type == packet.TYPE_ZIGBEE:
            return packet
        return None

    def gen_packet(self):
        '''Generate a Zigbee packet'''
        from ...protocol import pkt
        packet = pkt.Packet()
        packet.type = packet.TYPE_ZIGBEE
        packet.header_length = 0
        return packet

    def send_packet(self, packet):
        '''Send a Zigbee packet'''
        packet.payload.set_length()
        print("Send packet: ", packet.get_raw_packet())
        self.sf.writePacket(packet.get_raw_packet())
