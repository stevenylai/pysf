'''Test the packet (metaclass & descriptors)'''
import unittest
from ..packet import base, fields


class Packet(base.Packet):
    '''Testing packet'''
    field1 = fields.SizedHex(length=2)
    field2 = fields.SizedHex(length=3)
    field3 = fields.PacketField()


class TestPacket(unittest.TestCase):
    '''Test the basic packet functions'''
    def setUp(self):
        self.pkt = Packet(data=b'\x01\x02\x03\x04\x05\x06\07')

    def test_read(self):
        self.assertEqual(self.pkt.field1, 0x0201)
        self.assertEqual(self.pkt.field2, 0x050403)
        self.assertEqual(self.pkt.field3, b'\x06\07')

    def test_write(self):
        # Set a field
        self.pkt.field1 = 0x0100
        self.assertEqual(self.pkt.get_raw_packet(),
                         b'\x00\x01\x03\x04\x05\x06\07')
        # Truncate
        self.pkt.field3 = b'\x08'
        self.assertEqual(self.pkt.get_raw_packet(),
                         b'\x00\x01\x03\x04\x05\x08')
        # Extend
        self.pkt.field3 = b'\x06\x07\x08'
        self.assertEqual(self.pkt.get_raw_packet(),
                         b'\x00\x01\x03\x04\x05\x06\x07\x08')

if __name__ == '__main__':
    unittest.main()
