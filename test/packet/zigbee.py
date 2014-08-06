import time
import select

class Zigbee:
    def __init__(self, port):
        from ...core.SFSource import SFSource
        self.restart()
        self.sf = SFSource(None, port)
        self.sf.open()

    def restart(self):
        self.mac = None
        self.addr = None

    def process_packet(self):
        packet = self.sf.readPacket()
        packet = pkt.Packet(packet)
        if packet.type == packet.TYPE_ZIGBEE:
            zb_packet = packet.payload
            if zb_packet.type == zb_packet.TYPE_ZB_RESOLVE:
                self.mac = zb_packet.payload.addr_info.mac
                self.addr = zb_packet.payload.addr_info.addr

    def wait_for_addr(self):
        from ...packet import pkt
        while True:
            r,w,x = select.select([self.sf], [], [])
            if len(r) > 0:
                self.process_packet()
                break

if __name__ == '__main__':
    from ...packet import zigbee
    test_mac = 0x00124B000205F44C
    tester = Zigbee('localhost:3000')
    tester.wait_for_addr()
