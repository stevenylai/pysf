'''Zigbee base device'''
from .. import base


class Base(base.Device):
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


class Device(Base):
    '''Zigbee device for some basic
    functions including:

    * pair/unpair/leave
    * resolve

    '''
    def do_pair(self, pair_type, mac, addr):
        '''Zigbee pair/unpair'''
        packet = self.gen_packet()
        packet.payload.type = pair_type
        packet.payload.payload.mac = mac
        packet.payload.payload.addr = addr
        self.send_packet(packet)

    def resolve(self, mac):
        '''Zigbee resolve'''
        packet = self.gen_packet()
        packet.payload.type = packet.payload.TYPE_RESOLVE
        packet.payload.status = packet.payload.STATUS_REQ
        packet.payload.payload.type = packet.payload.payload.TYPE_ADDR_RESOLVE
        packet.payload.payload.mac = mac
        packet.payload.payload.addr = 0
        self.send_packet(packet)
