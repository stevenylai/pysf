'''Zigbee protocol testing'''
import unittest
from ...protocol import pkt


class TestZigbee(unittest.TestCase):
    '''Test case'''
    def gen_zigbee(self):
        '''Generate Zigbee packet'''
        packet = pkt.Packet()
        packet.type = packet.TYPE_ZIGBEE
        packet.header_length = 0
        return packet

    def gen_addr_info(self, mac, addr):
        packet = self.gen_zigbee()
        packet.payload.type = packet.payload.TYPE_RESOLVE
        packet.payload.status = packet.payload.STATUS_REQ
        packet.payload.payload.type = packet.payload.payload.TYPE_ADDR_RESOLVE
        packet.payload.payload.mac = mac
        packet.payload.payload.addr = addr
        packet.payload.set_length()
        return packet

    def test_addr_info(self):
        packet = self.gen_addr_info(0x0102030405060708, 0x0102)
        self.assertEqual(b'\x02\x00\x01\x00\x00\x00\x10\x00'
                         b'\x02\x00\x0c\x00'
                         b'\x00'
                         b'\x01\x08\x07\x06\x05\x04\x03\x02\x01\x02\x01',
                         packet.get_raw_packet())

    def gen_attribute(self, attr_list):
        packet = self.gen_zigbee()
        packet.payload.type = packet.payload.TYPE_ATTR_READ
        packet.payload.status = packet.payload.STATUS_OK
        packet.payload.payload.event = 1
        packet.payload.payload.status = 0
        packet.payload.payload.frame_control = 1
        packet.payload.payload.manu_code = 0
        packet.payload.payload.seq = 1
        packet.payload.payload.command_id = 1
        packet.payload.payload.cluster_id = 8
        packet.payload.payload.src.short_addr = 0x1234
        packet.payload.payload.src.mode = 2
        packet.payload.payload.src.end_point = 1
        packet.payload.payload.src.pan_id = 0
        packet.payload.payload.end_point = 1
        packet.payload.payload.num_attr = len(attr_list)
        packet.payload.payload.attr_data = attr_list
        return packet

    def gen_zcl_data(self, data_type, value):
        '''Generate a ZCL attribute data'''
        from ...protocol.zigbee import attribute
        attr = attribute.ZCLData()
        attr.attr_id = 1
        attr.status = 0
        attr.data_type = data_type
        attr.data = value
        return attr

    def test_attribute(self):
        '''Test attribute read/report packet'''
        attr1 = self.gen_zcl_data(0x08, 0x12)
        attr2 = self.gen_zcl_data(0x09, 0x1234)
        packet = self.gen_attribute([attr1, attr2])
        self.assertEqual(b'\x02\x00\x01\x00\x00\x00\x00\x00'
                         b'\x06\x00\x00\x00\x01'
                         b'\x01\x00\x01\x00\x00\x01\x01\x08\x00'
                         b'4\x12\x00\x00\x00\x00\x00\x00\x02\x01\x00\x00'
                         b'\x01\x02'
                         b'\x01\x00\x00\x08\x12'
                         b'\x01\x00\x00\t4\x12',
                         packet.get_raw_packet())

if __name__ == '__main__':
    unittest.main()
