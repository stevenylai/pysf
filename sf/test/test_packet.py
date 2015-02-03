'''Test the packet (metaclass & descriptors)'''
import unittest
from ..packet import base, fields


class Packet(base.Packet):
    '''Testing packet'''
    field1 = fields.SizedHex(length=2)
    field2 = fields.SizedHex(length=3)
    field3 = fields.PacketField()


class Base(base.Packet):
    '''Base packet'''
    field1 = fields.SizedHex(length=1)
    field2 = fields.SizedHex(length=3)


class Derived(Base):
    '''Derived packet'''
    field3 = fields.SizedHex(length=2)


class Derived2(Base):
    '''Derived packet 2'''
    field4 = fields.SizedHex(length=1)


class MultiDerived(Derived, Derived2):
    '''Mutliple inheritance.
    Note that field3 and field4 will
    share the same offset
    '''
    field5 = fields.SizedHex(length=1)


class TestPacket(unittest.TestCase):
    '''Test the basic packet functions'''
    def setUp(self):
        self.pkt = Packet(data=b'\x01\x02\x03\x04\x05\x06\07')

    def test_read(self):
        '''Access the fields'''
        self.assertEqual(self.pkt.field1, 0x0201)
        self.assertEqual(self.pkt.field2, 0x050403)
        self.assertEqual(self.pkt.field3, b'\x06\07')

    def test_write(self):
        '''Set the fields in the packet'''
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

    def test_inheritance(self):
        '''Inheritance'''
        packet = Derived()
        packet.field1 = 1
        packet.field2 = 2
        packet.field3 = 3
        self.assertEqual(packet.get_raw_packet(),
                         b'\x01\x02\x00\x00\x03\x00')

    def test_multi_inheritance(self):
        '''Multiple inheritance'''
        packet = MultiDerived()
        packet.field1 = 1
        packet.field2 = 2
        packet.field3 = 3
        packet.field4 = 4
        packet.field5 = 5
        self.assertEqual(packet.get_raw_packet(),
                         b'\x01'
                         b'\x02\x00\x00'
                         b'\x04\x00'
                         b'\x05')

if __name__ == '__main__':
    unittest.main()
