class Type:
    def __init__(self, offset, length = -1):
        self.offset = offset
        self.length = length

    def __get__(self, obj, objtype):
        if self.length < 0:
            return obj.packet[self.offset : ]
        else:
            return obj.packet[self.offset : self.offset + self.length]

    def __set__(self, obj, val):
        new_packet = b''
        i = 0
        j = 0
        for b in obj.packet:
            if i < self.offset or (self.length >= 0 and i >= self.offset + self.length):
                new_packet = new_packet + bytes([obj.packet[i]])
            else:
                new_packet = new_packet + bytes([val[j]])
                j = j + 1
            i = i + 1
        if self.length < 0:
            while j < len(val):
                new_packet = new_packet + bytes([val[j]])
                j = j + 1
        obj.packet = new_packet
        if obj.parent_packet != None: #Attribute of a sub packet
            print("Changing ", obj.name, "of parent to:", obj.packet)
            obj.parent_packet.__class__.__dict__[obj.name].__set__(obj.parent_packet, obj.packet)
    
