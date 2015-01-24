'''Packet field module'''
import math


class PacketField:
    '''Packet field descriptor'''
    def __init__(self, length=None, offset=None, name=None):
        self.offset = offset
        self.length = length
        self.name = name
        self.last_field = False

    def __get__(self, instance, cls):
        raw_packet = instance.get_raw_packet()
        if self.length is not None:
            return raw_packet[self.offset: self.offset + self.length]
        else:
            return raw_packet[self.offset:]

    def __set__(self, instance, value):
        instance.set_raw_packet(self.offset, value, self.last_field)


class PacketSelector(PacketField):
    '''Packet selector'''
    @classmethod
    def get_packet_cls(cls, parent):
        '''Get the packet class'''
        from . import base
        return base.Packet

    def __get__(self, instance, cls):
        pkt_cls = self.get_packet_cls(instance)
        pkt = pkt_cls(parent=instance, offset=self.offset,
                      length=self.length)
        pkt.last_field = self.last_field
        return pkt

    def __set__(self, instance, value):
        from . import base
        if not isinstance(value, base.Packet):
            raise ValueError('Must use a packet to set to selector')
        raw_packet = value.get_raw_packet()
        super().__set__(instance, raw_packet)


class Integer2Bytes(PacketField):
    '''Integer packet field'''
    def __get__(self, instance, cls):
        raw_packet = super().__get__(instance, cls)
        result = 0
        shift = 0
        for item in raw_packet:
            result += (item << shift)
            shift += 8
        return result

    def __set__(self, instance, value):
        result = []
        for i in range(0, self.length):
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
        if self.length is not None:
            max = math.pow(8, self.length + 1)
            if value > max:
                raise ValueError("Must be <= %s" % max)
        super().__set__(instance, value)
