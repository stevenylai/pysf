import importlib
from . import base

_parent_package = __name__.split('.', 1)[0] + '.packet'

class Subpacket(base.Type):
    def __init__(self, name, type_table, offset, length = -1):
        super().__init__(offset, length)
        self.name = name
        self.type_table = type_table

    def __get__(self, obj, objtype):
        type_key = obj.__class__.__dict__[self.name[0]].__get__(obj, objtype)
        if type_key not in self.type_table:
            return None
        else:
            guess_pkg = importlib.import_module("." + self.type_table[type_key], _parent_package)
            guess_cls = getattr(guess_pkg, 'Packeter')
            packet = guess_cls(obj, self.offset, self.length)
            packet.name = self.name[1]
            return packet
