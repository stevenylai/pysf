class Packeter:
    def __init__(self, packet, offset = 0, len = 0):
        self.raw_packet = packet
        self.offset = offset
        if len == 0:
            self.packet = self.raw_packet[offset:]
        else:
            self.packet = self.raw_packet[offset: offset + len]

    def get_field(self, offset, len):
        return self.packet[offset : offset + len]

    def get_int(self, offset, len):
        field = self.get_field(offset, len)
        result = 0
        shift = 0
        for b in field:
            result = result + (b << shift)
            shift = shift + 8
        return result

