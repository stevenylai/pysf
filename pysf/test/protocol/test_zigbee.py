'''Zigbee protocol testing'''
import unittest
from ...protocol import pkt


class TestZigbee(unittest.TestCase):
    '''Test case'''
    def gen_addr_info(self, mac, addr):
        packet = pkt.Packet()
        packet.type = packet.TYPE_ZIGBEE
        packet.header_length = 0
        packet.payload.type = packet.payload.TYPE_RESOLVE
        packet.payload.status = packet.payload.STATUS_REQ
        packet.payload.payload.type = packet.payload.payload.TYPE_ADDR_RESOLVE
        packet.payload.payload.mac = mac
        packet.payload.payload.addr = addr
        packet.payload.length = len(packet.payload.payload) + 1
        packet.payload_length = len(packet.payload)
        return packet

    def test_addr_info(self):
        packet = self.gen_addr_info(0x0102030405060708, 0x0102)
        self.assertEqual(b'\x02\x00\x01\x00\x00\x00\x10\x00'
                         b'\x02\x00\x0c\x00'
                         b'\x00'
                         b'\x01\x08\x07\x06\x05\x04\x03\x02\x01\x02\x01',
                         packet.get_raw_packet())

if __name__ == '__main__':
    unittest.main()
