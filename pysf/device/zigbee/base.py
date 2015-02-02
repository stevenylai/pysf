'''Zigbee base device'''
from . import Device as Base


def get_cluster_module(cluster_id):
    '''From a cluster ID get the corresponding
    Python module which implements the cluster
    logic
    '''
    # TODO: we can probably make this more dynamic and automatic
    if cluster_id == 0x0006:
        from .zcl import on_off
        return on_off
    if cluster_id == 0x0008:
        from .zcl import level_control
        return level_control
    return None


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
