import time

class Zigbee:
    def __init__(self, port):
        from ...core.SerialSource import SerialSource
        from ...core import SerialProtocol
        SerialProtocol.DEBUG = True
        self.sf = SerialSource(None, port)
        self.sf.open()

    def gen_packet(self, type, dest, **kwargs):
        from ...packet import zigbee_simple
        from ...packet import zigbee
        from ...packet import pkt
        zigbee_req = zigbee_simple.Packet(None, 0)
        zigbee_req.status = zigbee_req.ZB_REQ
        if 'mac' in kwargs:
            zigbee_req.mac = kwargs['mac']
        if 'data' in kwargs:
            zigbee_req.data = kwargs['data']
        #print('req', zigbee_req.packet)
        zigbee_packet = zigbee.Packet(bytes(14 + len(zigbee_req.packet)), 0)
        zigbee_packet.addr = dest
        if 'end_point' in kwargs:
            zigbee_packet.end_point = kwargs['end_point']
        else:
            zigbee_packet.end_point = 0xFF
        zigbee_packet.type = type
        zigbee_packet.length = len(zigbee_req.packet)
        zigbee_packet.payload = zigbee_req.packet
        #print('zigbee', zigbee_packet.packet)
        pkt_packet = pkt.Packet(None, 0)
        pkt_packet.type = pkt_packet.TYPE_ZIGBEE
        pkt_packet.header_length = 0
        pkt_packet.payload_length = len(zigbee_packet.packet)
        pkt_packet.payload = zigbee_packet.packet
        return pkt_packet.packet

    def send_and_read(self, packet):
        self.sf.writePacket(packet)
        print('Written', packet)
        for i in range(0, 1):
            packet = self.sf.readPacket()
            print('Read', packet)

    def pair(self, dest):
        from ...packet import zigbee
        packet = self.gen_packet(zigbee.Packet.TYPE_ZB_PAIR, 0x0, mac=dest)
        self.send_and_read(packet)

    def unpair(self, dest):
        from ...packet import zigbee
        packet = self.gen_packet(zigbee.Packet.TYPE_ZB_UNPAIR, 0x0, mac=dest)
        self.send_and_read(packet)

    def resolve(self, dest):
        from ...packet import zigbee
        packet = self.gen_packet(zigbee.Packet.TYPE_ZB_RESOLVE, 0x0, mac=dest)
        self.send_and_read(packet)

    def leave(self, dest, mac):
        from ...packet import zigbee
        packet = self.gen_packet(zigbee.Packet.TYPE_ZB_LEAVE, dest, mac=mac)
        self.send_and_read(packet)

    def on(self, dest, ep):
        from ...packet import zigbee
        packet = self.gen_packet(zigbee.Packet.TYPE_ZB_ON, dest, end_point=ep)
        self.send_and_read(packet)

    def off(self, dest, ep):
        from ...packet import zigbee
        packet = self.gen_packet(zigbee.Packet.TYPE_ZB_OFF, dest, end_point=ep)
        self.send_and_read(packet)

    def level(self, dest, ep, level):
        from ...packet import zigbee
        packet = self.gen_packet(zigbee.Packet.TYPE_ZB_LEVEL, dest, end_point=ep, data=level)
        self.send_and_read(packet)

if __name__ == '__main__':
    test_mac = 0x00124B000205F44C
    test_addr = 0x3F73
    zigbee = Zigbee('/dev/ttyS0:115200')
    #zigbee.pair(test_mac)
    #zigbee.resolve(test_mac)
    #zigbee.leave(test_addr, test_mac)
    #zigbee.unpair(test_mac)
    #time.sleep(10)
    #zigbee.off(test_addr, 8)
    zigbee.level(test_addr, 8, 100)
    print("Finished")
