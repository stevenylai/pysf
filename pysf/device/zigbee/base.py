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
    if cluster_id = 0x0008:
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

    def extract_read(self, zigbee_packet):
        '''Process read attribute
        The parameter here must be an
        attribute packet.

        The function will return the processed
        data in JSON format
        '''
        from ...protocol.zigbee.zcl import ZCL
        attr_pkt = zigbee_packet.payload.payload
        zcl = get_cluster_module(attr_pkt.cluster_id)
        if zcl is None:  # Unknown cluster
            return None
        extracted_list = []
        for i in range(0, attr_pkt.num_attr):
            attr_item = attr_pkt.attr_data[i]
            accessor = ZCL(attr_item.data_type)
            for name in zcl.ATTRIBUTES.keys():
                if zcl.ATTRIBUTES[name]['id'] == attr_item.attr_id:
                    extracted_list.append(
                        {name: accessor.to_python(attr_item.data)}
                    )
        return extracted_list

    def filter_packet(self, raw_packet):
        '''Filter packets'''
        packet = super().filter_packet(raw_packet)
        if packet is None:
            return packet
        zigbee_packet = packet.payload
        if zigbee_packet.type in {
            zigbee_packet.TYPE_ATTR_READ,
            zigbee_packet.TYPE_ATTR_REPORT
        }:
            self.process_attribute(zigbee_packet)
        return packet
