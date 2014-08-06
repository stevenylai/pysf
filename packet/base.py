class Packet:
    def __init__(self, packet, offset = 0, len = -1):
        if packet == None:
            raw_packet_list = []
            for i in range(0, self.get_length()):
                raw_packet_list.append(b'\x00')
            self.raw_packet = b''.join(raw_packet_list)
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
        max_len = 0
        for item in self.__class__.__dict__.values():
            if isinstance(item, base.Type):
                if item.length > 0 and item.offset + item.length > max_len:
                    max_len = item.offset + item.length
        return max_len

