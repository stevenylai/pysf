'''SF packet definitions'''
from collections import OrderedDict
from .fields import PacketField


def update_packet(dest, offset, source, truncate):
    '''Update packet dest, with source,
    starting from offset
    '''
    if len(dest) < offset:
        dest = dest + bytes(offset - len(dest)) + source
    else:
        temp = dest[0: offset] + source
        if len(dest) > offset + len(source) and not truncate:
            temp += dest[offset + len(source):]
        dest = temp
    return dest


class PacketType(type):
    '''Meta class for packet type'''
    @classmethod
    def __prepare__(cls, name, bases):
        return OrderedDict()

    def __new__(cls, clsname, bases, clsdict):
        from .fields import PacketField
        fields = [key for key, val in clsdict.items()
                  if isinstance(val, PacketField)]
        cur_offset = 0
        for name in fields:
            clsdict[name].name = name
            if clsdict[name].offset is None:
                clsdict[name].offset = cur_offset
            else:
                cur_offset = clsdict[name].offset
            if clsdict[name]._length is not None:
                cur_offset += clsdict[name]._length
            if fields.index(name) == len(fields) - 1:
                clsdict[name].last_field = True
            else:
                clsdict[name].last_field = False
        clsobj = super().__new__(cls, clsname, bases, dict(clsdict))
        return clsobj


class Packet(metaclass=PacketType):
    '''Packet base class'''
    def __init__(self, parent=None, data=None, offset=None, length=None):
        self.parent = parent
        if self.parent is None:
            if data is None:
                self.packet = b''
            else:
                self.packet = data
            self.last_field = True
        else:
            self.last_field = False
        self.offset = offset
        if self.offset is None:
            self.offset = 0
        self._length = length

    def get_raw_packet(self):
        '''Get the raw packet as byte array'''
        if self.parent is None:
            return self.packet
        else:
            raw_packet = self.parent.get_raw_packet()
            if self.offset is None:
                raise ValueError('Packet offset not initialized')
            if self._length is None:
                return raw_packet[self.offset:]
            else:
                return raw_packet[self.offset: self.offset + self._length]

    def set_raw_packet(self, offset, packet, truncate):
        '''Set the raw packet'''
        if self.parent is None:
            self.packet = update_packet(self.packet, offset, packet, truncate)
        else:
            if self.offset is None:
                raise ValueError('Packet offset not initialized')
            raw_packet = self.get_raw_packet()
            raw_packet = update_packet(
                raw_packet, offset, packet, truncate
            )
            self.parent.set_raw_packet(self.offset, raw_packet,
                                       self.last_field)

    def __len__(self):
        if self._length is not None:
            return self._length
        else:
            return len(self.get_raw_packet())


class BarePayload(Packet):
    '''Bare payload'''
    raw = PacketField()
