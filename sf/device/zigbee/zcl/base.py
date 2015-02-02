'''ZCL base device'''
# Note that we cannot do the following because
# base already has the Device name:
# from .. import base
# class Device(base.Device):
#     ...
from ..base import Device as ZigbeeDevice


class Device(ZigbeeDevice):
    '''ZCL base device class'''
    ZCL_CMD_READ = 0x00
    ZCL_CMD_CONFIG_REPORT = 0x06

    def do_bind(self, bind_type, mac, addr, end_point, cluster_id):
        '''Bind/unbind'''
        packet = self.gen_packet()
        packet.payload.type = packet.payload.TYPE_BIND
        packet.payload.payload.type = bind_type
        packet.payload.payload.end_point = end_point
        packet.payload.payload.cluster_id = cluster_id
        packet.payload.payload.mac = mac
        packet.payload.payload.addr = addr
        self.send_packet(packet)

    def zcl_command(self, addr, src_ep, cluster_id, command_id, specific,
                    direction, manu_code, seq, disable_default_rsp, cmd_list):
        '''ZCL command'''
        packet = self.gen_packet()
        packet.payload.type = packet.payload.TYPE_CLUSTER_COMMAND
        packet.payload.payload.src_ep = src_ep
        packet.payload.payload.dest = addr
        packet.payload.payload.cluster_id = cluster_id
        packet.payload.payload.command_id = command_id
        packet.payload.payload.specific = specific
        packet.payload.payload.direction = direction
        packet.payload.payload.manu_code = manu_code
        packet.payload.payload.seq = seq
        packet.payload.payload.disable_default_rsp = disable_default_rsp
        total_len = 0
        for cmd in cmd_list:
            total_len += len(cmd)
        packet.payload.payload.cmd_fmt_len = total_len
        packet.payload.payload.cmd_fmt = cmd_list
        self.send_packet(packet)

    def zcl_config_report(self, cfg_reports, addr, src_ep, cluster_id,
                          direction, manu_code, seq, disable_default_rsp):
        '''ZCL configure report'''
        cmd_list = []
        for report in cfg_reports:
            cmd_list.extend(report.get_commands())
        self.zcl_command(addr, src_ep, cluster_id, self.ZCL_CMD_CONFIG_REPORT,
                         0, direction, manu_code, seq, disable_default_rsp,
                         cmd_list)

    def zcl_read_attribute(self, attributes, addr, src_ep, cluster_id,
                           direction, manu_code, seq, disable_default_rsp):
        '''ZCL read attribute'''
        cmd_list = []
        for item in attributes:
            cmd_list.extend(item.get_commands())
        self.zcl_command(addr, src_ep, cluster_id, self.ZCL_CMD_READ, 0,
                         direction, manu_code, seq, disable_default_rsp,
                         cmd_list)

    def extract_read(self, zigbee_packet):
        '''Process read attribute
        The parameter here must be an
        attribute packet.

        The function will return the processed
        data in JSON format
        '''
        from ....protocol.zigbee.zcl import ZCL
        from .. import get_cluster_module
        attr_pkt = zigbee_packet.payload
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

    def attribute_read(self, is_read, attribute):
        '''Process the read attribute.
        Override to implement custom logics
        if this method returns True, then
        the coresponding read/report packet will not
        be notified again
        '''
        return False

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
            attr = self.extract_read(zigbee_packet)
            if self.attribute_read(
                (
                    True if zigbee_packet.type == zigbee_packet.TYPE_ATTR_READ
                    else False
                ), attr
            ):
                return None
        return packet
