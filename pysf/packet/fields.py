'''Packet field module'''
import math


def byte_to_int(data):
    '''Convert a byte array of data to an integer'''
    result = 0
    shift = 0
    for item in data:
        result += (item << shift)
        shift += 8
    return result


class PacketField:
    '''Packet field descriptor'''
    def __init__(self, length=None, offset=None, name=None):
        self.offset = offset
        self._length = length
        self.name = name
        self.last_field = False

    def __get__(self, instance, cls):
        raw_packet = instance.get_raw_packet()
        if self._length is not None:
            return raw_packet[self.offset: self.offset + self._length]
        else:
            return raw_packet[self.offset:]

    def __set__(self, instance, value):
        instance.set_raw_packet(self.offset, value,
                                (self.last_field and instance.last_field))


class PacketSelector(PacketField):
    '''Packet selector'''
    def get_packet_cls(self, parent):
        '''Get the packet class'''
        from . import base
        return base.Packet

    def __get__(self, instance, cls):
        pkt_cls = self.get_packet_cls(instance)
        pkt = pkt_cls(parent=instance, offset=self.offset,
                      length=self._length)
        pkt.last_field = self.last_field
        return pkt

    def __set__(self, instance, value):
        from . import base
        if isinstance(value, base.Packet):
            raw_packet = value.get_raw_packet()
            super().__set__(instance, raw_packet)
        elif isinstance(value, bytes):
            super().__set__(instance, value)
        else:
            raise ValueError('Must use a packet/byte array to set to selector')


class PacketListSelector(PacketSelector):
    '''Packet list selector will get a list of packets instead of just one'''
    def __get__(self, instance, cls):
        pkt_cls = self.get_packet_cls(instance)
        parent = instance
        raw_packet = parent.get_raw_packet()
        raw_packet = raw_packet[self.offset:]
        packets = []
        self._length = 0
        sub_offset = 0
        for i in range(0, parent.num_attr):
            pkt = pkt_cls(parent=parent,
                          offset=sub_offset + self.offset)
            if i == parent.num_attr - 1:
                pkt.last_field = self.last_field
            self._length += len(pkt)
            packets.append(pkt)
        return packets

    def __set__(self, instance, value):
        if not isinstance(value, list):
            raise ValueError('Must set with a list of packets')
        raw_packet_list = []
        self._length = 0
        for pkt in value:
            raw_packet_list.append(pkt.get_raw_packet())
            self._length += len(pkt)
        super().__set__(instance, b''.join(raw_packet_list))


class Integer2Bytes(PacketField):
    '''Integer packet field'''
    def get_raw_packet(self, instance, cls):
        '''Get raw packet'''
        return super().__get__(instance, cls)

    def __get__(self, instance, cls):
        raw_packet = self.get_raw_packet(instance, cls)
        return byte_to_int(raw_packet)

    def __set__(self, instance, value):
        result = []
        for i in range(0, self._length):
            result.append(bytes([value % 256]))
            value = value >> 8
        super().__set__(instance, b''.join(result))

class Typed(PacketField):
    '''Typed packet field'''
    ty = object

    def __set__(self, instance, value):
        if not isinstance(value, self.ty):
            raise TypeError('Expected %s' % self.ty)
        super().__set__(instance, value)


class NonNegative(PacketField):
    '''Non-negative packet field'''
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError('Must be >= 0')
        super().__set__(instance, value)


class PosInteger(Typed, NonNegative, Integer2Bytes):
    '''Positive integer field'''
    ty = int


class SizedHex(PosInteger):
    '''Sized hex field'''
    def __set__(self, instance, value):
        if self._length is not None:
            max = math.pow(256, self._length)
            if value >= max:
                raise ValueError("Must be < %s" % max)
        super().__set__(instance, value)
