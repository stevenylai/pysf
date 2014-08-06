from . import base
from .types import int
from .types import struct
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
    mac = int.IntType(0, 8)
    addr = int.IntType(8, 2)

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
    
class Packet(base.Packet):
    ZB_REQ = 0
    ZB_RES_OK = 1
    ZB_RES_UNKNOWN_CMD = 2
    ZB_RES_TOO_MANY_PAIRED = 3
    ZB_RES_NETWORK_ERROR = 4

    status = int.IntType(0, 1)
    addr_info = struct.Struct(AddrInfo, 'addr_info', 1, 10)
    command = struct.Struct(ZigbeeCommand, 'command', 1, 88)
    #command = raw.RawType(1, 88)

if __name__ == '__main__':
    p = Packet(b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b')
    print(p.status)
    print(hex(p.addr_info.mac), hex(p.addr_info.addr))
