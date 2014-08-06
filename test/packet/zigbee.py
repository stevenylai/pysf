import sys
import re
import time
import select

class Zigbee:
    ZCL_CLUSTER_ID_GEN_ON_OFF = 0x6
    ZCL_CLUSTER_ID_GEN_LEVEL_CONTROL = 0x8

    COMMAND_OFF = 0x00
    COMMAND_ON = 0x01
    COMMAND_LEVEL_MOVE_TO_LEVEL = 0x0

    ZCL_FRAME_CLIENT_SERVER_DIR = 0x00
    ZCL_FRAME_SERVER_CLIENT_DIR = 0x01

    def __init__(self, port):
        from ...core.SFSource import SFSource
        self.end_point = 8
        self.restart()
        self.sf = SFSource(None, port)
        self.sf.open()

    def restart(self):
        self.mac = None
        self.addr = None

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

    def send_command(self, src_ep, cluster_id, cmd, specific, dir, seq, cmd_fmt):
        from ...packet import zigbee_payload
        from ...packet import zigbee
        from ...packet import pkt
        zb_payload = zigbee_payload.Packet(None)
        zb_payload.status = zb_payload.ZB_REQ
        zb_payload.command.src_ep = src_ep
        zb_payload.command.dest.short_addr = self.addr
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
        zb_pkt = zigbee.Packet(None)
        zb_pkt.type = zb_pkt.TYPE_ZB_CLUSTER_COMMAND
        zb_pkt.length = len(zb_payload.packet)
        zb_pkt.payload = zb_payload.packet
        pkt_pkt = pkt.Packet(None)
        pkt_pkt.type = pkt_pkt.TYPE_ZIGBEE
        pkt_pkt.header_length = 0
        pkt_pkt.payload_length = len(zb_pkt.packet)
        pkt_pkt.payload = zb_pkt.packet
        print("Writing:", pkt_pkt.packet)
        self.sf.writePacket(pkt_pkt.packet)

    def unpair(self):
        from ...packet import zigbee_payload
        from ...packet import zigbee
        from ...packet import pkt
        addr_info = zigbee_payload.AddrInfo(None)
        addr_info.mac = self.mac
        addr_info.addr = self.addr
        zb_payload = zigbee_payload.Packet(bytes(len(addr_info.packet) + 1))
        zb_payload.status = zb_payload.ZB_REQ
        zb_payload.addr_info = addr_info.packet
        zb_pkt = zigbee.Packet(None)
        zb_pkt.type = zb_pkt.TYPE_ZB_LEAVE
        zb_pkt.length = len(zb_payload.packet)
        zb_pkt.payload = zb_payload.packet
        pkt_pkt = pkt.Packet(None)
        pkt_pkt.type = pkt_pkt.TYPE_ZIGBEE
        pkt_pkt.header_length = 0
        pkt_pkt.payload_length = len(zb_pkt.packet)
        pkt_pkt.payload = zb_pkt.packet
        print("Writing:", pkt_pkt.packet)
        self.sf.writePacket(pkt_pkt.packet)

    def process_packet(self):
        from ...packet import pkt
        packet = self.sf.readPacket()
        packet = pkt.Packet(packet)
        if packet.type == packet.TYPE_ZIGBEE:
            zb_packet = packet.payload
            if zb_packet.type == zb_packet.TYPE_ZB_RESOLVE:
                self.mac = zb_packet.payload.addr_info.mac
                self.addr = zb_packet.payload.addr_info.addr
                print("New device detected:", hex(self.mac), hex(self.addr))

    def wait_for_addr(self):
        from ...packet import pkt
        print("Waiting for device")
        while True:
            r,w,x = select.select([self.sf], [], [])
            if len(r) > 0:
                self.process_packet()
                if self.mac != None and self.addr != None:
                    break

if __name__ == '__main__':
    from ...packet import zigbee
    tester = Zigbee('localhost:3000')
    while True:
        tester.wait_for_addr()
        while True:
            r,w,x = select.select([sys.stdin], [], [])
            if len(r) > 0:
                line = sys.stdin.readline()
                if line.startswith('on'):
                    tester.on()
                elif line.startswith('off'):
                    tester.off()
                elif line.startswith('level'):
                    m = re.compile('level([0-9]+)').search(line)
                    if m != None:
                        tester.simple_level(int(m.group(1)))
                elif line.startswith('unpair'):
                    tester.unpair()
                    tester.restart()
                    break
                elif line.startswith('quit'):
                    print("Restarting test")
                    tester.restart()
                    break
            
    
