import time

class Zigbee:
    def __init__(self, port):
        from ...core.SerialSource import SerialSource
        from ...core import SerialProtocol
        SerialProtocol.DEBUG = True
        self.sf = SerialSource(None, port)
        self.sf.open()
        self.pkt_seq = 0xE
        
    def gen_packet(self, type, dest, end_point=0xFF, zigbee_req=None):
        from ...packet import zigbee_simple
        from ...packet import zigbee
        from ...packet import pkt
        if zigbee_req == None:
            zigbee_req = zigbee_simple.Packet(None, 0)
            zigbee_req.status = zigbee_req.ZB_REQ
            #print(zigbee_req.packet)
        zigbee_packet = zigbee.Packet(bytes(14 + len(zigbee_req.packet)), 0)
        zigbee_packet.mac_addr = dest
        zigbee_packet.end_point = end_point
        zigbee_packet.type = type
        zigbee_packet.seq = self.pkt_seq
        self.pkt_seq += 1
        zigbee_packet.length = len(zigbee_req.packet)
        zigbee_packet.payload = zigbee_req.packet
        #print(zigbee_packet.packet)
        pkt_packet = pkt.Packet(None, 0)
        pkt_packet.type = pkt_packet.TYPE_ZIGBEE
        pkt_packet.header_length = 0
        pkt_packet.payload_length = len(zigbee_packet.packet)
        pkt_packet.payload = zigbee_packet.packet
        return pkt_packet.packet

    def send_and_read(self, packet):
        self.sf.writePacket(packet)
        print('Written', packet)
        for i in range(0, 2):
            packet = self.sf.readPacket()
            print('Read', packet)

    def pair(self, dest):
        from ...packet import zigbee
        packet = self.gen_packet(zigbee.Packet.TYPE_ZB_PAIR, dest)
        self.send_and_read(packet)

    def unpair(self, dest):
        from ...packet import zigbee
        packet = self.gen_packet(zigbee.Packet.TYPE_ZB_UNPAIR, dest)
        self.send_and_read(packet)

    def on(self, dest, ep):
        from ...packet import zigbee
        packet = self.gen_packet(zigbee.Packet.TYPE_ZB_ON, dest, ep)
        self.send_and_read(packet)

    def off(self, dest, ep):
        from ...packet import zigbee
        packet = self.gen_packet(zigbee.Packet.TYPE_ZB_OFF, dest, ep)
        self.send_and_read(packet)

    def level(self, dest, ep, level):
        from ...packet import zigbee
        from ...packet import zigbee_onebyte
        payload = zigbee_onebyte.Packet(None, 0)
        payload.status =  payload.ZB_REQ
        payload.data = level
        packet = self.gen_packet(zigbee.Packet.TYPE_ZB_LEVEL, dest, ep, payload)
        self.send_and_read(packet)

if __name__ == '__main__':
    test_dest = 0x00124B000205F44C
    zigbee = Zigbee('/dev/ttyS0:115200')
    #zigbee.pair(test_dest)
    #time.sleep(10)
    zigbee.on(test_dest, 8)
    #zigbee.level(test_dest, 8, 12)
