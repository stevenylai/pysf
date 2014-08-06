import importlib
from . import base

_parent_package = __name__.split('.', 1)[0] + '.packet'

class Struct(base.Type):
    def __init__(self, cls, name, offset, length):
        super().__init__(offset, length)
        self.cls = cls
        self.name = name
    
    def __get__(self, obj, objtype):
        new_pkt = self.cls(obj.packet[self.offset : self.offset + self.length], 0, self.length)
        new_pkt.name = self.name
        new_pkt.parent_packet = obj
        return new_pkt

