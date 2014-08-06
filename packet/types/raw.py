from . import base

class RawType(base.Type):
    def __init__(self, offset, max_len):
        super().__init__(offset)
        self.max_len = max_len
        self.length = 0

    def __get__(self, obj, objtype):
        if self.length == 0:
            return b''
        else:
            return obj.packet[self.offset : self.offset + self.length]

    def __set__(self, obj, val):
        self.length = len(val)
        if len(obj.packet) > self.offset + self.length:
            obj.packet = obj.packet[0 : self.offset + self.length]
        elif len(obj.packet) < self.offset + self.length:
            obj.packet = obj.packet + bytes(self.offset + self.length - len(obj.packet))
        super(RawType, self).__set__(obj, val)


    
