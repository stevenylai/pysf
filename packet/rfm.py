from . import base

class Packeter(base.Packeter):
    RFM_SRC = (0, 3)
    RFM_DEST = (4, 3)
    RFM_TYPE = (3, 1)
    RFM_LENGTH = (7, 1)
    RFM_PAYLOAD = 8

    @property
    def type(self):
        return self.get_int(self.RFM_TYPE[0], self.RFM_TYPE[1])

    @property
    def length(self):
        return self.get_int(self.RFM_LENGTH[0], self.RFM_LENGTH[1])

    @property
    def src(self):
        return self.get_int(self.RFM_SRC[0], self.RFM_SRC[1])

    @property
    def dest(self):
        return self.get_int(self.RFM_DEST[0], self.RFM_DEST[1])

    @property
    def payload(self):
        return self.packet[self.RFM_PAYLOAD:]
