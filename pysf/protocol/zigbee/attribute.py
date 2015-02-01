'''Zigbee attribute (read/report) packet module'''
from ...packet import base, fields
from . import AddressField


class ZCLDataItem(fields.Integer2Bytes):
    '''ZCL data item'''
    def __set__(self, instance, value):
        self._length = len(instance) - 4
        super().__set__(instance, value)

    def get_raw_packet(self, instance, cls):
        '''Get raw packet'''
        raw_packet = super().__get__(instance, cls)
        return raw_packet[
            self.offset: self.offset + instance.get_length()
        ]


class ZCLData(base.Packet):
    '''Individual ZCL data packet'''
    attr_id = fields.SizedHex(length=2)
    status = fields.SizedHex(length=1)
    data_type = fields.SizedHex(length=1)
    data = ZCLDataItem()

    def __len__(self):
        '''Get total length'''
        from .zcl import base
        total_len = 4
        attr = base.ZCL(self.data_type)
        total_len += attr.get_length()
        return total_len


class ZCLDataField(fields.PacketListSelector):
    '''ZCL data selector'''
    def get_packet_cls(self, parent):
        '''Get packet class'''
        return ZCLData


class Packet(base.Packet):
    '''Zigbee attribute (read/report) packet'''
    event = fields.SizedHex(length=1)
    status = fields.SizedHex(length=1)
    frame_control = fields.SizedHex(length=1)
    manu_code = fields.SizedHex(length=2)
    seq = fields.SizedHex(length=1)
    command_id = fields.SizedHex(length=1)
    cluster_id = fields.SizedHex(length=2)
    src = AddressField()
    end_point = fields.SizedHex(length=1)
    num_attr = fields.SizedHex(length=1)
    attr_data = ZCLDataField()
