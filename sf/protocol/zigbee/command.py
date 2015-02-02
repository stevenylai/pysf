'''ZCL command packet module'''
from ...packet import base, fields
from . import AddressField


class ZCLCommandData(fields.SizedHex):
    '''ZCL command data'''
    _command_length = 0

    def __init__(self, length=None, offset=None, name=None):
        super().__init__(length, offset, name)
        self._length = 1

    def __set__(self, instance, value):
        instance._length = self._command_length
        super().__set__(instance, value)


class TwoByteCommand(ZCLCommandData):
    '''Two byte command'''
    _command_length = 2


class OneByteCommand(ZCLCommandData):
    '''One byte command'''
    _command_length = 1


class ZCLCommand(base.Packet):
    '''ZCL command packet'''
    one_byte = OneByteCommand(offset=0)
    low_byte = TwoByteCommand(offset=0)
    high_byte = TwoByteCommand()


class ZCLCommandField(fields.PacketListSelector):
    '''ZCL command selector'''
    def get_packet_cls(self, parent):
        '''Get packet class'''
        return ZCLCommand


class Packet(base.Packet):
    '''ZCL command packet'''
    ZCL_FRAME_CLIENT_SERVER_DIR = 0x00
    ZCL_FRAME_SERVER_CLIENT_DIR = 0x01

    src_ep = fields.SizedHex(length=1)
    dest = AddressField()
    cluster_id = fields.SizedHex(length=2)
    command_id = fields.SizedHex(length=1)
    specific = fields.SizedHex(length=1)
    direction = fields.SizedHex(length=1)
    disable_default_rsp = fields.SizedHex(length=1)
    manu_code = fields.SizedHex(length=2)
    seq = fields.SizedHex(length=1)
    cmd_fmt_len = fields.SizedHex(length=2)
    cmd_fmt = ZCLCommandField()
