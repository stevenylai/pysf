'''ZCL base functions'''


class ZCL:
    '''ZCL data type class'''
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

    def __init__(self, data_type):
        '''Create a ZCL data with type'''
        self.data_type = data_type

    def get_length(self):
        '''Get the length according to the type'''
        if self.data_type in {
            self.ZCL_DATATYPE_DATA8, self.ZCL_DATATYPE_BOOLEAN,
            self.ZCL_DATATYPE_BITMAP8, self.ZCL_DATATYPE_INT8,
            self.ZCL_DATATYPE_UINT8, self.ZCL_DATATYPE_ENUM8
        }:
            return 1
        elif self.data_type in {
        self.ZCL_DATATYPE_DATA16, self.ZCL_DATATYPE_BITMAP16,
        self.ZCL_DATATYPE_UINT16, self.ZCL_DATATYPE_INT16,
        self.ZCL_DATATYPE_ENUM16, self.ZCL_DATATYPE_SEMI_PREC,
        self.ZCL_DATATYPE_CLUSTER_ID, self.ZCL_DATATYPE_ATTR_ID
        }:
            return 2
        elif self.data_type in {
        self.ZCL_DATATYPE_DATA24, self.ZCL_DATATYPE_BITMAP24,
        self.ZCL_DATATYPE_UINT24, self.ZCL_DATATYPE_INT24
        }:
            return 3
        elif self.data_type in {
        self.ZCL_DATATYPE_DATA32, self.ZCL_DATATYPE_BITMAP32,
        self.ZCL_DATATYPE_UINT32, self.ZCL_DATATYPE_INT32,
        self.ZCL_DATATYPE_SINGLE_PREC, self.ZCL_DATATYPE_TOD,
        self.ZCL_DATATYPE_DATE, self.ZCL_DATATYPE_UTC,
        self.ZCL_DATATYPE_BAC_OID
        }:
            return 4
        elif self.data_type in {
        self.ZCL_DATATYPE_UINT40, self.ZCL_DATATYPE_INT40
        }:
            return 5
        elif self.data_type in {
        self.ZCL_DATATYPE_UINT48, self.ZCL_DATATYPE_INT48
        }:
            return 6
        elif self.data_type in {
        self.ZCL_DATATYPE_UINT56, self.ZCL_DATATYPE_INT56
        }:
            return 7
        elif self.data_type in {
        self.ZCL_DATATYPE_DOUBLE_PREC, self.ZCL_DATATYPE_IEEE_ADDR,
        self.ZCL_DATATYPE_UINT64, self.ZCL_DATATYPE_INT64
        }:
            return 8
        elif self.data_type in {
        self.ZCL_DATATYPE_128_BIT_SEC_KEY
        }:
            return 16
        elif self.data_type in {
        self.ZCL_DATATYPE_NO_DATA, self.ZCL_DATATYPE_UNKNOWN
        }:
            return 0
        else:
            return 0

    def is_analog(self):
        '''Check if the type is analog data type'''
        if self.data_type in {
            self.ZCL_DATATYPE_UINT8,
            self.ZCL_DATATYPE_UINT16,
            self.ZCL_DATATYPE_UINT24,
            self.ZCL_DATATYPE_UINT32,
            self.ZCL_DATATYPE_UINT40,
            self.ZCL_DATATYPE_UINT48,
            self.ZCL_DATATYPE_UINT56,
            self.ZCL_DATATYPE_UINT64,
            self.ZCL_DATATYPE_INT8,
            self.ZCL_DATATYPE_INT16,
            self.ZCL_DATATYPE_INT24,
            self.ZCL_DATATYPE_INT32,
            self.ZCL_DATATYPE_INT40,
            self.ZCL_DATATYPE_INT48,
            self.ZCL_DATATYPE_INT56,
            self.ZCL_DATATYPE_INT64,
            self.ZCL_DATATYPE_SEMI_PREC,
            self.ZCL_DATATYPE_SINGLE_PREC,
            self.ZCL_DATATYPE_DOUBLE_PREC,
            self.ZCL_DATATYPE_TOD,
            self.ZCL_DATATYPE_DATE,
            self.ZCL_DATATYPE_UTC,
        }:
            return True
        else:
            return False

    def serialize(self, data, buf_list):
        '''Serialize the data according in the data
        and append the resulting byte list to buf_list
        '''
        if self.data_type in {
            self.ZCL_DATATYPE_DATA8,
            self.ZCL_DATATYPE_BOOLEAN,
            self.ZCL_DATATYPE_BITMAP8,
            self.ZCL_DATATYPE_INT8,
            self.ZCL_DATATYPE_UINT8,
            self.ZCL_DATATYPE_ENUM8,
        }:
            buf_list.append(data[0: 1])
        elif self.data_type in {
        self.ZCL_DATATYPE_DATA16,
        self.ZCL_DATATYPE_BITMAP16,
        self.ZCL_DATATYPE_UINT16,
        self.ZCL_DATATYPE_INT16,
        self.ZCL_DATATYPE_ENUM16,
        self.ZCL_DATATYPE_SEMI_PREC,
        self.ZCL_DATATYPE_CLUSTER_ID,
        self.ZCL_DATATYPE_ATTR_ID,
        }:
            buf_list.append(data[0: 2])
        elif self.data_type in {
        self.ZCL_DATATYPE_DATA24,
        self.ZCL_DATATYPE_BITMAP24,
        self.ZCL_DATATYPE_UINT24,
        self.ZCL_DATATYPE_INT24,
        }:
            buf_list.append(data[0: 3])
        elif self.data_type in {
        self.ZCL_DATATYPE_DATA32,
        self.ZCL_DATATYPE_BITMAP32,
        self.ZCL_DATATYPE_UINT32,
        self.ZCL_DATATYPE_INT32,
        self.ZCL_DATATYPE_SINGLE_PREC,
        self.ZCL_DATATYPE_TOD,
        self.ZCL_DATATYPE_DATE,
        self.ZCL_DATATYPE_UTC,
        self.ZCL_DATATYPE_BAC_OID,
        }:
            buf_list.append(data[0: 4])
        elif self.data_type == self.ZCL_DATATYPE_UINT40:
            buf_list.append(data[0: 5])
        elif self.data_type == self.ZCL_DATATYPE_UINT48:
            buf_list.append(data[0: 6])
        elif self.data_type == self.ZCL_DATATYPE_IEEE_ADDR:
            buf_list.append(data[0: 8])
        elif self.data_type in {
        self.ZCL_DATATYPE_CHAR_STR,
        self.ZCL_DATATYPE_OCTET_STR,
        }:
            str_len = data[0]
            buf_list.append(data[0: str_len + 1])
        elif self.data_type in {
        self.ZCL_DATATYPE_LONG_CHAR_STR,
        self.ZCL_DATATYPE_LONG_OCTET_STR,
        }:
            str_len = data[0] + (data[1] << 8)
            buf_list.append(data[0: str_len + 2])
        elif self.data_type == self.ZCL_DATATYPE_128_BIT_SEC_KEY:
            buf_list.append(data[0: 16])
        return buf_list


class CommandGen:
    '''Command generator base class'''
    def one_byte(self, value):
        '''One byte command'''
        from .. import command
        cmd = command.OneByteCommand()
        cmd.one_byte = value
        return cmd

    def two_byte(self, value):
        '''Two byte command'''
        from .. import command
        cmd = command.TwoByteCommand()
        cmd.low_byte = value & 0xFF
        cmd.high_byte = value >> 8 & 0xFF
        return cmd
