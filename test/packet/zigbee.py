import sys
import re
import time
import select
import argparse

class ZigbeeReportConfig:
    ZCL_SEND_ATTR_REPORTS = 0
    ZCL_EXPECT_ATTR_REPORTS = 1

    direction = 0
    attr_id = 0
    type = 0
    min_interval = 0
    max_interval = 0
    timeout = 0
    threshold = b''

class Zigbee:
    ZCL_CLUSTER_ID_GEN_ON_OFF = 0x6
    ZCL_CLUSTER_ID_GEN_LEVEL_CONTROL = 0x8

    ZCL_CMD_READ = 0x00
    ZCL_CMD_CONFIG_REPORT = 0x06
    COMMAND_OFF = 0x00
    COMMAND_ON = 0x01
    COMMAND_LEVEL_MOVE_TO_LEVEL = 0x0

    ZCL_FRAME_CLIENT_SERVER_DIR = 0x00
    ZCL_FRAME_SERVER_CLIENT_DIR = 0x01

    def __init__(self, port, key = b''):
        from ...core.SFSource import SFSource
        self.end_point = 1
        self.addr_list = []
        self.addr_sel = -1
        self.sf = SFSource(None, port)
        self.key = key
        self.sf.open(self.key)

    def restart(self):
        self.addr_list.clear()
        self.addr_sel = -1

    def on(self):
        self.send_command(self.end_point, self.ZCL_CLUSTER_ID_GEN_ON_OFF,
                          self.COMMAND_ON, 1, self.ZCL_FRAME_CLIENT_SERVER_DIR,
                          1, b'')

    def off(self):
        self.send_command(self.end_point, self.ZCL_CLUSTER_ID_GEN_ON_OFF,
                          self.COMMAND_OFF, 1, self.ZCL_FRAME_CLIENT_SERVER_DIR,
                          1, b'')

    def level(self, command, seq, level, transtime):
        cmd_fmt = bytes([level, transtime & 0xFF, transtime >> 8])
        self.send_command(self.end_point, self.ZCL_CLUSTER_ID_GEN_LEVEL_CONTROL,
                          command, 1, self.ZCL_FRAME_CLIENT_SERVER_DIR,
                          seq, cmd_fmt)

    def simple_level(self, level):
        self.level(self.COMMAND_LEVEL_MOVE_TO_LEVEL, 1, level, 0)

    def simple_send_read(self, cluster_id, attrs):
        self.send_read(self.end_point, cluster_id, attrs, self.ZCL_FRAME_CLIENT_SERVER_DIR, 0)

    def send_read(self, src_ep, cluster_id, attrs, dir, seq):
        buf = []
        for attr in attrs:
            buf.append(attr & 0xFF)
            buf.append(attr >> 8)
        buf = bytes(buf)
        #print(buf)
        self.send_command(src_ep, cluster_id, self.ZCL_CMD_READ, 0, dir, seq, buf)

    def send_config_report_cmd(self, cluster_id, cfg_reports, dir, seq):
        from ...packet import zigbee_payload
        from ...packet import zigbee
        cmd_buf = []
        for config in cfg_reports:
            cmd_buf.append(config.direction)
            cmd_buf.append(config.attr_id & 0xFF)
            cmd_buf.append(config.attr_id >> 8 & 0xFF)
            if config.direction == config.ZCL_SEND_ATTR_REPORTS:
                cmd_buf.append(config.min_interval & 0xFF)
                cmd_buf.append(config.min_interval >> 8 & 0xFF)
                cmd_buf.append(config.max_interval & 0xFF)
                cmd_buf.append(config.max_interval >> 8 & 0xFF)
                cmd_buf += [b for b in config.threshold]
            else:
                cmd_buf.append(config.timeout & 0xFF)
                cmd_buf.append(config.timeout >> 8 & 0xFF)
        self.send_command(self.end_point, cluster_id, self.ZCL_CMD_CONFIG_REPORT, 0, dir, seq, bytes(cmd_buf))

    def write_zigbee_payload(self, payload, type):
        from ...packet import zigbee
        from ...packet import pkt
        zb_pkt = zigbee.Packet(None)
        zb_pkt.type = type
        zb_pkt.length = len(payload.packet)
        zb_pkt.payload = payload.packet
        pkt_pkt = pkt.Packet(None)
        pkt_pkt.type = pkt_pkt.TYPE_ZIGBEE
        pkt_pkt.header_length = 0
        pkt_pkt.payload_length = len(zb_pkt.packet)
        pkt_pkt.payload = zb_pkt.packet
        print(time.time(), "Writing:", pkt_pkt.packet)
        self.sf.writePacket(pkt_pkt.packet)

    def send_command(self, src_ep, cluster_id, cmd, specific, dir, seq, cmd_fmt):
        from ...packet import zigbee_payload
        from ...packet import zigbee
        zb_payload = zigbee_payload.Packet(None)
        zb_payload.status = zb_payload.ZB_REQ
        zb_payload.command.src_ep = src_ep
        zb_payload.command.dest.short_addr = self.addr_list[self.addr_sel][1]
        zb_payload.command.dest.end_point = src_ep
        zb_payload.command.dest.mode = zb_payload.command.dest.ADDR_16BIT
        zb_payload.command.pan_id = 0
        zb_payload.command.cluster_id = cluster_id
        zb_payload.command.command_id = cmd
        zb_payload.command.specific = specific
        zb_payload.command.direction = dir
        zb_payload.command.disable_default_rsp = 0
        zb_payload.command.manu_code = 0
        zb_payload.command.seq = 1
        zb_payload.command.cmd_fmt_len = len(cmd_fmt)
        zb_payload.command.cmd_fmt = cmd_fmt
        #print(zb_payload.packet)
        self.write_zigbee_payload(zb_payload, zigbee.Packet.TYPE_ZB_CLUSTER_COMMAND)

    def resolve(self, mac):
        from ...packet import zigbee_payload
        from ...packet import zigbee
        addr_info = zigbee_payload.AddrInfo(None)
        addr_info.mac = mac
        addr_info.addr = 0
        zb_payload = zigbee_payload.Packet(bytes(len(addr_info.packet) + 1))
        zb_payload.status = zb_payload.ZB_REQ
        zb_payload.addr_info = addr_info.packet
        self.write_zigbee_payload(zb_payload, zigbee.Packet.TYPE_ZB_RESOLVE)

    def pair(self, type):
        from ...packet import zigbee_payload
        addr_info = zigbee_payload.AddrInfo(None)
        addr_info.mac = self.addr_list[self.addr_sel][0]
        addr_info.addr = self.addr_list[self.addr_sel][1]
        zb_payload = zigbee_payload.Packet(bytes(len(addr_info.packet) + 1))
        zb_payload.status = zb_payload.ZB_REQ
        zb_payload.addr_info = addr_info.packet
        self.write_zigbee_payload(zb_payload, type)

    def bind(self, cluster_id):
        from ...packet import zigbee_payload
        from ...packet import zigbee
        bind = zigbee_payload.ZigbeeBind(None)
        bind.mac = self.addr_list[self.addr_sel][0]
        bind.addr = self.addr_list[self.addr_sel][1]
        bind.end_point = self.end_point
        bind.type = bind.TYPE_BIND_BIND
        bind.cluster_id = cluster_id
        zb_payload = zigbee_payload.Packet(bytes(len(bind.packet) + 1))
        zb_payload.status = zb_payload.ZB_REQ
        zb_payload.bind = bind.packet
        self.write_zigbee_payload(zb_payload, zigbee.Packet.TYPE_ZB_BIND)

    def report_on_off(self, min, max):
        from ...packet import zigbee_payload
        config = ZigbeeReportConfig()
        config.direction = config.ZCL_SEND_ATTR_REPORTS
        config.attr_id = zigbee_payload.ZigbeeAttr.ATTRID_ON_OFF
        config.min_interval = min
        config.max_interval = max
        self.send_config_report_cmd(self.ZCL_CLUSTER_ID_GEN_ON_OFF, [config], self.ZCL_FRAME_CLIENT_SERVER_DIR, 0)

    def report_level(self, min, max):
        from ...packet import zigbee_payload
        config = ZigbeeReportConfig()
        config.direction = config.ZCL_SEND_ATTR_REPORTS
        config.attr_id = zigbee_payload.ZigbeeAttr.ATTRID_LEVEL_CURRENT_LEVEL
        config.min_interval = min
        config.max_interval = max
        self.send_config_report_cmd(self.ZCL_CLUSTER_ID_GEN_LEVEL_CONTROL, [config], self.ZCL_FRAME_CLIENT_SERVER_DIR, 0)

    def process_packet(self):
        from ...packet import pkt
        packet = self.sf.readPacket()
        packet = pkt.Packet(packet)
        if packet.type == packet.TYPE_ZIGBEE:
            zb_packet = packet.payload
            if zb_packet.type == zb_packet.TYPE_ZB_RESOLVE:
                new_addr = (zb_packet.payload.addr_info.mac, zb_packet.payload.addr_info.addr)
                if new_addr[0] not in [a[0] for a in self.addr_list]:
                    self.addr_list.append(new_addr)
                    self.addr_sel = len(self.addr_list) - 1
                else:
                    cur_idx = [a[0] for a in self.addr_list].index(new_addr[0])
                    self.addr_list.remove(self.addr_list[cur_idx])
                    self.addr_list.insert(cur_idx, new_addr)
                if zb_packet.payload.addr_info.type == zb_packet.payload.addr_info.TYPE_ADDR_JOIN:
                    type_str = 'join'
                else:
                    type_str = 'resolve'
                print(time.time(), type_str, "device:", hex(new_addr[0]), hex(new_addr[1]))
            elif zb_packet.type == zb_packet.TYPE_ZB_ATTR_READ or zb_packet.type == zb_packet.TYPE_ZB_ATTR_REPORT:
                resp = zb_packet.payload.resp
                self.process_read(resp, zb_packet)

    def process_read(self, resp, zb_packet):
        from ...packet import zigbee_payload
        if resp.src.mode != resp.src.ADDR_16BIT:
            return
        if resp.num_attr == 0:
            return
        header = str(time.time())
        if zb_packet.type == zb_packet.TYPE_ZB_ATTR_READ:
            header += " read "
        elif zb_packet.type == zb_packet.TYPE_ZB_ATTR_REPORT:
            header += " report "
        attr_data = resp.attr_data
        if resp.cluster_id == self.ZCL_CLUSTER_ID_GEN_ON_OFF:
            for i in range(0, resp.num_attr):
                attr = zigbee_payload.ZigbeeAttr(attr_data)
                if attr.attr_id == attr.ATTRID_ON_OFF:
                    on_off = (attr.get_data() & 0xFF)
                    print(header, "on_off for", hex(resp.src.short_addr), on_off)
                attr_data = attr_data[attr.get_length():]
        elif resp.cluster_id == self.ZCL_CLUSTER_ID_GEN_LEVEL_CONTROL:
            for i in range(0, resp.num_attr):
                attr = zigbee_payload.ZigbeeAttr(attr_data)
                if attr.attr_id == attr.ATTRID_LEVEL_CURRENT_LEVEL:
                    level = (attr.get_data() & 0xFF)
                    print(header, "level for", hex(resp.src.short_addr), level)
                attr_data = attr_data[attr.get_length():]

    def display_current_devs(self):
        print('_______________________________')
        i = 0
        for item in self.addr_list:
            if i != self.addr_sel:
                print('|  ' + str(i) + ': ' + hex(item[0]) + ', ' + hex(item[1]))
            else:
                print('|* ' + str(i) + ': ' + hex(item[0]) + ', ' + hex(item[1]))
            i += 1

    def wait_for_addr(self):
        from ...packet import pkt
        print("Waiting for device")
        while True:
            r,w,x = select.select([self.sf], [], [])
            if len(r) > 0:
                self.process_packet()
                if len(self.addr_list) > 0:
                    break

def read_device(tester):
    while True:
        r,w,x = select.select([tester.sf], [], [])
        if len(r) > 0:
            tester.process_packet()

def test_device(tester):
    from ...packet import zigbee_payload
    from ...packet import zigbee
    while True:
        #tester.wait_for_addr()
        while True:
            r,w,x = select.select([sys.stdin, tester.sf], [], [])
            for port in r:
                if id(port) == id(sys.stdin):
                    line = sys.stdin.readline()
                    if line.startswith('resolve'):
                        m = re.compile(r'resolve[ \t]+([a-fA-FxX0-9]+)').search(line)
                        if m != None:
                            tester.resolve(int(m.group(1), 16))
                    elif line.startswith('on'):
                        tester.on()
                    elif line.startswith('off'):
                        tester.off()
                    elif line.startswith('level'):
                        m = re.compile(r'level[ \t]+([0-9]+)').search(line)
                        if m != None:
                            tester.simple_level(int(m.group(1)))
                    elif line.startswith('report'):
                        m = re.compile(r'report[ \t]+(.+)').search(line)
                        if m != None:
                            if m.group(1) == 'level':
                                tester.report_level(1, 3)
                            elif m.group(1) == 'on_off':
                                tester.report_on_off(70, 80)
                    elif line.startswith('bind'):
                        m = re.compile(r'bind[ \t]+(.+)').search(line)
                        if m != None:
                            if m.group(1) == 'level':
                                tester.bind(tester.ZCL_CLUSTER_ID_GEN_LEVEL_CONTROL)
                            elif m.group(1) == 'on_off':
                                tester.bind(tester.ZCL_CLUSTER_ID_GEN_ON_OFF)
                    elif line.startswith('read'):
                        m = re.compile(r'read[ \t]+([a-zA-Z_]+)').search(line)
                        if m != None:
                            if m.group(1) == 'on_off':
                                tester.simple_send_read(tester.ZCL_CLUSTER_ID_GEN_ON_OFF, [zigbee_payload.ZigbeeAttr.ATTRID_ON_OFF])
                            elif m.group(1) == 'level':
                                tester.simple_send_read(tester.ZCL_CLUSTER_ID_GEN_LEVEL_CONTROL, [zigbee_payload.ZigbeeAttr.ATTRID_LEVEL_CURRENT_LEVEL])
                    elif line.startswith('unpair'):
                        tester.pair(zigbee.Packet.TYPE_ZB_LEAVE)
                        tester.pair(zigbee.Packet.TYPE_ZB_UNPAIR)
                        tester.addr_list.remove(tester.addr_list[tester.addr_sel])
                        tester.addr_sel = 0
                    elif line.startswith('pair'):
                        tester.pair(zigbee.Packet.TYPE_ZB_PAIR)
                    elif line.startswith('quit'):
                        print("Restarting test")
                        tester.restart()
                    elif re.compile('^[0-9]+$').search(line) != None:
                        sel = int(line)
                        if sel < len(tester.addr_list):
                            tester.addr_sel = sel
                elif id(port) == id(tester.sf):
                    tester.process_packet()
                tester.display_current_devs()

if __name__ == '__main__':
    from ...packet import zigbee
    from ...packet import zigbee_payload
    parser = argparse.ArgumentParser(description='Zigbee tester.')
    parser.add_argument('--hub', metavar='ip:port', type=str, nargs='?',
                        default='127.0.0.1:3000', help='ip:port of the hub running sf')
    parser.add_argument('--key', metavar='bind_secret', type=str, nargs='?',
                        default='', help='bind secret of the hub running sf')
    args = parser.parse_args()
    print(args.hub, bytes(args.key, 'utf-8'))
    #tester = Zigbee('192.168.1.26:3000', b'3f2cfb1789a649b1be92fb0a6b2fd0a1')
    tester = Zigbee(args.hub, bytes(args.key, 'utf-8'))
    test_device(tester)
    #read_device(tester)
