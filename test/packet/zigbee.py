def gen_packet():
    from ...packet import zigbee_simple
    from ...packet import zigbee
    from ...packet import pkt
    zigbee_req = zigbee_simple.Packet(None, 0)
    zigbee_req.status = zigbee_req.ZB_RES_OK
    print(zigbee_req.packet)
    zigbee_packet = zigbee.Packet(bytes(14 + len(zigbee_req.packet)), 0)
    zigbee_packet.mac_addr = 0x0102030405060708
    zigbee_packet.type = zigbee_packet.TYPE_ZB_UNPAIR
    zigbee_packet.seq = 0xE
    zigbee_packet.length = len(zigbee_req.packet)
    zigbee_packet.payload = zigbee_req.packet
    print(zigbee_packet.packet)
    pkt_packet = pkt.Packet(None, 0)
    pkt_packet.type = pkt_packet.TYPE_ZIGBEE
    pkt_packet.header_length = 0
    pkt_packet.payload_length = len(zigbee_packet.packet)
    pkt_packet.payload = zigbee_packet.packet
    return pkt_packet.packet
    
if __name__ == '__main__':
    packet = gen_packet()
    from ...core.SerialSource import SerialSource
    from ...core import SerialProtocol
    SerialProtocol.DEBUG = True
    sf = SerialSource(None, '/dev/ttyS0:115200')
    sf.open()
    sf.writePacket(packet)
    print('Written', packet)
    packet = sf.readPacket()
    print('Read', packet)
    sf.close()
    
