class Packet:
    def __init__(self, packet, offset = 0, len = -1):
        if packet == None:
            self.raw_packet = b''
            for i in range(0, self.get_length()):
                self.raw_packet = self.raw_packet + b'\x00'
            self.parent_packet = None
        elif isinstance(packet, Packet):
            self.raw_packet = packet.packet
            self.parent_packet = packet
        else:
            self.raw_packet = packet
            self.parent_packet = None
        self.offset = offset
        if len < 0:
            self.packet = self.raw_packet[offset:]
        else:
            self.packet = self.raw_packet[offset: offset + len]
        #print("Raw packet", self.raw_packet, "packet", self.packet)

    def get_length(self):
        from .types import base
        total_len = 0
        for item in self.__class__.__dict__.values():
            if isinstance(item, base.Type):
                if item.length > 0:
                    total_len = total_len + item.length
        return total_len

