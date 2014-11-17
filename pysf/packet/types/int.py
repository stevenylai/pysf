from . import base

class IntType(base.Type):
    def __get__(self, obj, objtype):
        packet = super(IntType, self).__get__(obj, objtype)
        result = 0
        shift = 0
        for b in packet:
            result = result + (b << shift)
            shift = shift + 8
        return result

    def __set__(self, obj, val):
        result = []
        for i in range(0, self.length):
            result.append(bytes([val % 256]))
            val = val >> 8
        super(IntType, self).__set__(obj, b''.join(result))
