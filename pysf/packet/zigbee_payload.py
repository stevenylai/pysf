from . import base
from .types import int
from .types import struct
from .types import array
from .types import raw

class ZigbeeAddr(base.Packet):
    ADDR_NOT_PRESENT = 0
    ADDR_GROUP = 1
    ADDR_16BIT = 2
    ADDR_64BIT = 3
    ADDR_BROADCAST = 15

    short_addr = int.IntType(0, 2)
    mac = int.IntType(0, 8)
    mode = int.IntType(8, 1)
    end_point = int.IntType(9, 1)
    pan_id = int.IntType(10, 2)

class AddrInfo(base.Packet):
    TYPE_ADDR_JOIN = 0
    TYPE_ADDR_RESOLVE = 1

    type = int.IntType(0, 1)
    mac = int.IntType(1, 8)
    addr = int.IntType(9, 2)

class ZigbeeBind(base.Packet):
    TYPE_BIND_BIND = 0
    TYPE_BIND_UNBIND = 1
    TYPE_BIND_ACK = 2
    TYPE_BINE_NACK = 3

    type = int.IntType(0, 1)
    end_point = int.IntType(1, 1)
    cluster_id = int.IntType(2, 2)
    mac = int.IntType(4, 8)
    addr = int.IntType(12, 2)

class ZigbeeAttr(base.Packet):
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

    attr_id = int.IntType(0, 2)
    status = int.IntType(2, 1)
    data_type = int.IntType(3, 1)

    def get_data(self):
        if self.data_type in [self.ZCL_DATATYPE_DATA8, self.ZCL_DATATYPE_BOOLEAN,
                              self.ZCL_DATATYPE_BITMAP8, self.ZCL_DATATYPE_INT8,
                              self.ZCL_DATATYPE_UINT8, self.ZCL_DATATYPE_ENUM8]:
            return self.packet[4]
        else: #TODO: to be implemented
            return self.packet[4:]

    def get_length(self):
        total_len = 4
        if self.data_type in [self.ZCL_DATATYPE_DATA8, self.ZCL_DATATYPE_BOOLEAN,
                              self.ZCL_DATATYPE_BITMAP8, self.ZCL_DATATYPE_INT8,
                              self.ZCL_DATATYPE_UINT8, self.ZCL_DATATYPE_ENUM8]:
            total_len += 1
        elif self.data_type in [self.ZCL_DATATYPE_DATA16, self.ZCL_DATATYPE_BITMAP16,
                                self.ZCL_DATATYPE_UINT16, self.ZCL_DATATYPE_INT16,
                                self.ZCL_DATATYPE_ENUM16, self.ZCL_DATATYPE_SEMI_PREC,
                                self.ZCL_DATATYPE_CLUSTER_ID, self.ZCL_DATATYPE_ATTR_ID]:
            total_len += 2
        elif self.data_type in [self.ZCL_DATATYPE_DATA24, self.ZCL_DATATYPE_BITMAP24,
                                self.ZCL_DATATYPE_UINT24, self.ZCL_DATATYPE_INT24]:
            total_len += 3
        elif self.data_type in [self.ZCL_DATATYPE_DATA32, self.ZCL_DATATYPE_BITMAP32,
                                self.ZCL_DATATYPE_UINT32, self.ZCL_DATATYPE_INT32,
                                self.ZCL_DATATYPE_SINGLE_PREC, self.ZCL_DATATYPE_TOD,
                                self.ZCL_DATATYPE_DATE, self.ZCL_DATATYPE_UTC,
                                self.ZCL_DATATYPE_BAC_OID]:
            total_len += 4
        elif self.data_type in [self.ZCL_DATATYPE_UINT40, self.ZCL_DATATYPE_INT40]:
            total_len += 5
        elif self.data_type in [self.ZCL_DATATYPE_UINT48, self.ZCL_DATATYPE_INT48]:
            total_len += 6
        elif self.data_type in [self.ZCL_DATATYPE_UINT56, self.ZCL_DATATYPE_INT56]:
            total_len += 7
        elif self.data_type in [self.ZCL_DATATYPE_DOUBLE_PREC, self.ZCL_DATATYPE_IEEE_ADDR,
                                self.ZCL_DATATYPE_UINT64, self.ZCL_DATATYPE_INT64]:
            total_len += 8
        elif self.data_type in [self.ZCL_DATATYPE_128_BIT_SEC_KEY]:
            total_len += 16
        elif self.data_type in [self.ZCL_DATATYPE_NO_DATA, self.ZCL_DATATYPE_UNKNOWN]:
            total_len += 0
        return total_len

class ZigbeeCommand(base.Packet):
    src_ep = int.IntType(0, 1)
    dest = struct.Struct(ZigbeeAddr, 'dest', 1, 12)
    cluster_id = int.IntType(13, 2)
    command_id = int.IntType(15, 1)
    specific = int.IntType(16, 1)
    direction = int.IntType(17, 1)
    disable_default_rsp = int.IntType(18, 1)
    manu_code = int.IntType(19, 2)
    seq = int.IntType(21, 1)
    cmd_fmt_len = int.IntType(22, 2)
    cmd_fmt = raw.RawType(24, 64)

class ZigbeeRead(base.Packet):
    event = int.IntType(0, 1)
    status = int.IntType(1, 1)
    frame_control = int.IntType(2, 1)
    manu_code = int.IntType(3, 2)
    seq = int.IntType(5, 1)
    command_id = int.IntType(6, 1)
    cluster_id = int.IntType(7, 2)
    src = struct.Struct(ZigbeeAddr, 'src', 9, 12)
    end_point = int.IntType(21, 1)
    num_attr = int.IntType(22, 1)
    attr_data = raw.RawType(23, 64)

class Packet(base.Packet):
    ZB_REQ = 0
    ZB_RES_OK = 1
    ZB_RES_UNKNOWN_CMD = 2
    ZB_RES_TOO_MANY_PAIRED = 3
    ZB_RES_NETWORK_ERROR = 4

    status = int.IntType(0, 1)
    addr_info = struct.Struct(AddrInfo, 'addr_info', 1, 11)
    bind = struct.Struct(ZigbeeBind, 'bind', 1, 14)
    command = struct.Struct(ZigbeeCommand, 'command', 1, 88)
    resp = struct.Struct(ZigbeeRead, 'resp', 1, 47)

if __name__ == '__main__':
    p = Packet(b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b')
    print(p.status)
    print(hex(p.addr_info.mac), hex(p.addr_info.addr))
