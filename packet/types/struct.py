import importlib
from . import base

_parent_package = __name__.split('.', 1)[0] + '.packet'

class Struct(base.Type):
    def __init__(self, cls, offset, length):
        super().__init__(offset, length)
        self.cls = cls
    
    def __get__(self, obj, objtype):
        return self.cls(obj.packet[self.offset : self.offset + self.length], 0, self.length)

