from . import base

class Array(base.Type):
    def __init__(self, cls, name, offset, count):
        self.cls = cls
        test_pkt = self.cls(None)
        super().__init__(offset, test_pkt.get_length() * count)
        self.name = name
        self.unit_length = test_pkt.get_length()
        self.count = count
        self.sub_packets = None

    def generate_packet(self, obj):
        self.sub_packets = []
        cur_offset = 0
        for i in range(0, self.count):
            new_pkt = self.cls(obj.packet, self.offset + cur_offset, self.unit_length)
            cur_offset = cur_offset + self.unit_length
            self.sub_packets.append(new_pkt)
        return self.sub_packets

    def __get__(self, obj, objtype):
        return self.generate_packet(obj)

