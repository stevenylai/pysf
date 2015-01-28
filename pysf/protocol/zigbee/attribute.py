'''Zigbee attribute (read/report) packet module'''
from ...packet import base, fields
from . import AddressField


class ZCLDataItem(fields.Integer2Bytes):
    '''ZCL data item'''
    def __set__(self, instance, value):
        self._length = instance.get_length() - 4
        super().__set__(instance, value)

    def get_raw_packet(self, instance, cls):
        '''Get raw packet'''
        raw_packet = super().__get__(instance, cls)
        return raw_packet[
            self.offset: self.offset + instance.get_length()
        ]


class ZCLData(base.Packet):
    '''Individual ZCL data packet'''
    ATTRID_ON_OFF = 0
    ATTRID_LEVEL_CURRENT_LEVEL = 0

    ZCL_DATATYPE_NO_DATA = 0x00
    ZCL_DATATYPE_DATA8 = 0x08
    ZCL_DATATYPE_DATA16 = 0x09
    ZCL_DATATYPE_DATA24 = 0x0a
    ZCL_DATATYPE_DATA32 = 0x0b
    ZCL_DATATYPE_DATA40 = 0x0c
    ZCL_DATATYPE_DATA48 = 0x0d
    ZCL_DATATYPE_DATA56 = 0x0e
    ZCL_DATATYPE_DATA64 = 0x0f
    ZCL_DATATYPE_BOOLEAN = 0x10
    ZCL_DATATYPE_BITMAP8 = 0x18
    ZCL_DATATYPE_BITMAP16 = 0x19
    ZCL_DATATYPE_BITMAP24 = 0x1a
    ZCL_DATATYPE_BITMAP32 = 0x1b
    ZCL_DATATYPE_BITMAP40 = 0x1c
    ZCL_DATATYPE_BITMAP48 = 0x1d
    ZCL_DATATYPE_BITMAP56 = 0x1e
    ZCL_DATATYPE_BITMAP64 = 0x1f
    ZCL_DATATYPE_UINT8 = 0x20
    ZCL_DATATYPE_UINT16 = 0x21
    ZCL_DATATYPE_UINT24 = 0x22
    ZCL_DATATYPE_UINT32 = 0x23
    ZCL_DATATYPE_UINT40 = 0x24
    ZCL_DATATYPE_UINT48 = 0x25
    ZCL_DATATYPE_UINT56 = 0x26
    ZCL_DATATYPE_UINT64 = 0x27
    ZCL_DATATYPE_INT8 = 0x28
    ZCL_DATATYPE_INT16 = 0x29
    ZCL_DATATYPE_INT24 = 0x2a
    ZCL_DATATYPE_INT32 = 0x2b
    ZCL_DATATYPE_INT40 = 0x2c
    ZCL_DATATYPE_INT48 = 0x2d
    ZCL_DATATYPE_INT56 = 0x2e
    ZCL_DATATYPE_INT64 = 0x2f
    ZCL_DATATYPE_ENUM8 = 0x30
    ZCL_DATATYPE_ENUM16 = 0x31
    ZCL_DATATYPE_SEMI_PREC = 0x38
    ZCL_DATATYPE_SINGLE_PREC = 0x39
    ZCL_DATATYPE_DOUBLE_PREC = 0x3a
    ZCL_DATATYPE_OCTET_STR = 0x41
    ZCL_DATATYPE_CHAR_STR = 0x42
    ZCL_DATATYPE_LONG_OCTET_STR = 0x43
    ZCL_DATATYPE_LONG_CHAR_STR = 0x44
    ZCL_DATATYPE_ARRAY = 0x48
    ZCL_DATATYPE_STRUCT = 0x4c
    ZCL_DATATYPE_SET = 0x50
    ZCL_DATATYPE_BAG = 0x51
    ZCL_DATATYPE_TOD = 0xe0
    ZCL_DATATYPE_DATE = 0xe1
    ZCL_DATATYPE_UTC = 0xe2
    ZCL_DATATYPE_CLUSTER_ID = 0xe8
    ZCL_DATATYPE_ATTR_ID = 0xe9
    ZCL_DATATYPE_BAC_OID = 0xea
    ZCL_DATATYPE_IEEE_ADDR = 0xf0
    ZCL_DATATYPE_128_BIT_SEC_KEY = 0xf1
    ZCL_DATATYPE_UNKNOWN = 0xff

    attr_id = fields.SizedHex(length=2)
    status = fields.SizedHex(length=1)
    data_type = fields.SizedHex(length=1)
    data = ZCLDataItem()

    def get_length(self):
        '''Get total length'''
        total_len = 4
        if self.data_type in {
                self.ZCL_DATATYPE_DATA8, self.ZCL_DATATYPE_BOOLEAN,
                self.ZCL_DATATYPE_BITMAP8, self.ZCL_DATATYPE_INT8,
                self.ZCL_DATATYPE_UINT8, self.ZCL_DATATYPE_ENUM8
        }:
            total_len += 1
        elif self.data_type in {
        self.ZCL_DATATYPE_DATA16, self.ZCL_DATATYPE_BITMAP16,
        self.ZCL_DATATYPE_UINT16, self.ZCL_DATATYPE_INT16,
        self.ZCL_DATATYPE_ENUM16, self.ZCL_DATATYPE_SEMI_PREC,
        self.ZCL_DATATYPE_CLUSTER_ID, self.ZCL_DATATYPE_ATTR_ID
        }:
            total_len += 2
        elif self.data_type in {
        self.ZCL_DATATYPE_DATA24, self.ZCL_DATATYPE_BITMAP24,
        self.ZCL_DATATYPE_UINT24, self.ZCL_DATATYPE_INT24
        }:
            total_len += 3
        elif self.data_type in {
        self.ZCL_DATATYPE_DATA32, self.ZCL_DATATYPE_BITMAP32,
        self.ZCL_DATATYPE_UINT32, self.ZCL_DATATYPE_INT32,
        self.ZCL_DATATYPE_SINGLE_PREC, self.ZCL_DATATYPE_TOD,
        self.ZCL_DATATYPE_DATE, self.ZCL_DATATYPE_UTC,
        self.ZCL_DATATYPE_BAC_OID
        }:
            total_len += 4
        elif self.data_type in {
        self.ZCL_DATATYPE_UINT40, self.ZCL_DATATYPE_INT40
        }:
            total_len += 5
        elif self.data_type in {
        self.ZCL_DATATYPE_UINT48, self.ZCL_DATATYPE_INT48
        }:
            total_len += 6
        elif self.data_type in {
        self.ZCL_DATATYPE_UINT56, self.ZCL_DATATYPE_INT56
        }:
            total_len += 7
        elif self.data_type in {
        self.ZCL_DATATYPE_DOUBLE_PREC, self.ZCL_DATATYPE_IEEE_ADDR,
        self.ZCL_DATATYPE_UINT64, self.ZCL_DATATYPE_INT64
        }:
            total_len += 8
        elif self.data_type in {
        self.ZCL_DATATYPE_128_BIT_SEC_KEY
        }:
            total_len += 16
        elif self.data_type in {
        self.ZCL_DATATYPE_NO_DATA, self.ZCL_DATATYPE_UNKNOWN
        }:
            total_len += 0
        return total_len


class ZCLDataField(fields.PacketSelector):
    '''ZCL data selector'''
    def get_packet_cls(self, parent):
        '''Get packet class'''
        return ZCLData

    def __get__(self, instance, cls):
        '''Get attribute data.
        This one will return as list of ZCLData
        '''
        parent = instance
        raw_packet = parent.get_raw_packet()
        raw_packet = raw_packet[self.offset:]
        packets = []
        self._length = 0
        sub_offset = 0
        for i in range(0, parent.num_attr):
            pkt = ZCLData(parent=parent,
                          offset=sub_offset + self.offset)
            if i == parent.num_attr - 1:
                pkt.last_field = self.last_field
            self._length += pkt.get_length()
            packets.append(pkt)
        return packets

    def __set__(self, instance, value):
        '''Set ZCL data list.
        The input here must be a list of ZCLData
        '''
        if not isinstance(value, list):
            raise ValueError('Must set with a list of packets')
        raw_packet_list = []
        self._length = 0
        for pkt in value:
            raw_packet_list.append(pkt.get_raw_packet())
            self._length += pkt.get_length()
        super().__set__(instance, b''.join(raw_packet_list))


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
