'''Zigbee attribute (read/report) packet module'''
from ...packet import base, fields
from . import AddressField


class ZCLDataItem(fields.PacketField):
    '''ZCL data item'''
    def __set__(self, instance, value):
        self._length = len(instance) - 4
        super().__set__(instance, value)

    def __get__(self, instance, cls):
        '''Return the raw bytes because the actual value
        will depend on the data_type field in the parent
        packet
        '''
        raw_packet = instance.get_raw_packet()
        return raw_packet[
            self.offset: self.offset + len(instance)
        ]


class ZCLData(base.Packet):
    '''Individual ZCL data packet'''
    attr_id = fields.SizedHex(length=2)
    status = fields.SizedHex(length=1)
    data_type = fields.SizedHex(length=1)
    data = ZCLDataItem()

    # TODO: we probably need some set/get data functions
    # here to access the data field

    def __len__(self):
        '''Get total length'''
        from .zcl.base import ZCL
        total_len = 4
        attr = ZCL(self.data_type)
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
