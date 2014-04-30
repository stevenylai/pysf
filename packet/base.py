class Packeter:
    def __init__(self, packet, offset = 0, len = -1):
        if isinstance(packet, Packeter):
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




