'''ZCL base device'''
from .. import base


class Device(base.Device):
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
        self.zcl_command(addr, src_ep, cluster_id, ZCL_CMD_CONFIG_REPORT, 0,
                         direction, manu_code, seq, disable_default_rsp,
                         cmd_list)

    def zcl_read_attribute(self, src_ep, cluster_id, attributes, direction,
                           seq):
        '''ZCL read attribute'''
        pass
