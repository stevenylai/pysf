'''Test the packet (metaclass & descriptors)'''
import unittest
from ..packet import base, fields


class Packet(base.Packet):
    '''Testing packet'''
    field1 = fields.Integer(length=2)
    field2 = fields.Integer(length=4)
    field3 = fields.Integer(length=1)


class TestPacket(unittest.TestCase):
    '''Test the basic packet functions'''
    def test_packet(self):
        pkt = Packet(data=b'\x01\x02\x03\x04\x05\x06\07')
        self.assertEqual(pkt.field1, 0x0201)
        self.assertEqual(pkt.field2, 0x06050403)
        self.assertEqual(pkt.field3, 0x07)


if __name__ == '__main__':
    unittest.main()
