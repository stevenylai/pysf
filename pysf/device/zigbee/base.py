'''Zigbee base device'''
from . import Device as Base


class Device(Base):
    '''Zigbee device for some basic
    functions including:

    * pair/unpair
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
