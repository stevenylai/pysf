from . import base

class Packeter(base.Packeter):
    PKT_TYPE = (0, 4)
    PKT_HEADER_LEN = (4, 2)
    PKT_PAYLOAD_LEN = (6, 2)
    PKT_PAYLOAD = 8

    @property
    def type(self):
        return self.get_int(self.PKT_TYPE[0], self.PKT_TYPE[1])

    @property
    def payload_length(self):
        return self.get_int(self.PKT_PAYLOAD_LEN[0], self.PKT_PAYLOAD_LEN[1])

    @property
    def header_length(self):
        return self.get_int(self.PKT_HEADER_LEN[0], self.PKT_HEADER_LEN[1])

    @property
    def payload(self):
        return self.packet[self.PKT_PAYLOAD:]
