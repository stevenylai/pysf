'''RFM protocol tesing module'''
import unittest
from ...protocol import pkt


class TestRfm(unittest.TestCase):
    '''RFM unit test'''
    def gen_power(self, rssi=None):
        '''Generate socket power data'''
        packet = pkt.Packet()
        packet.type = packet.TYPE_RFM
        if rssi is None:
            packet.header_length = 0
        else:
            packet.header_length = 2
            packet.header.rssi = rssi
        packet.payload_length = 16
        packet.payload.src = 0x181818
        packet.payload.dest = 0x818181
        packet.payload.payload_length = 8
        packet.payload.type = packet.payload.TYPE_SOCKET_POWER
        packet.payload.payload.voltage = 1
        packet.payload.payload.current = 2
        packet.payload.payload.power = 3
        packet.payload.payload.frequency = 4
        return packet

    def test_read(self):
        packet = self.gen_power()
        pkt.Packet(data=packet.get_raw_packet())
        self.assertEqual(packet.type, packet.TYPE_RFM)
        self.assertEqual(packet.payload.src, 0x181818)
        self.assertEqual(packet.payload.payload.voltage, 1)
        packet = self.gen_power(125)
        pkt.Packet(data=packet.get_raw_packet())
        self.assertEqual(packet.type, packet.TYPE_RFM)
        self.assertEqual(packet.header.rssi, 125)
        self.assertEqual(packet.payload.src, 0x181818)
        self.assertEqual(packet.payload.payload.voltage, 1)

    def test_write(self):
        packet = self.gen_power()
        self.assertEqual(
            packet.get_raw_packet(),
            b'\x01\x00\x00\x00\x00\x00\x10\x00\x18\x18\x18&'
            b'\x81\x81\x81\x08\x01\x00\x02\x00\x03\x00\x00\x04'
        )
        packet = self.gen_power(125)
        self.assertEqual(
            packet.get_raw_packet(),
            b'\x01\x00\x00\x00\x02\x00\x10\x00}\x00\x18\x18\x18&'
            b'\x81\x81\x81\x08\x01\x00\x02\x00\x03\x00\x00\x04'
        )

if __name__ == '__main__':
    unittest.main()
