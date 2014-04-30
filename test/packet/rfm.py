import select


def dump_pkt(extractor):
    print("pkt type:", extractor.type,
          "header len:", extractor.header_length,
          "payload len:", extractor.payload_length,
          "payload:", extractor.payload)
def dump_rfm(extractor):
    print("src:", hex(extractor.src),
          "type:", hex(extractor.type),
          "dest:", hex(extractor.dest),
          "len:", hex(extractor.length),
          "payload:", extractor.payload)
if __name__ == '__main__':
    from ...core.SFSource import SFSource
    from ...packet import pkt
    from ...packet import rfm
    sf = SFSource(None, '192.168.1.33:3000')
    sf.open()
    while True:
        r,w,x = select.select([sf], [], [])
        if len(r) > 0:
            packet = sf.readPacket()
            extractor = pkt.Packeter(packet)
            extractor = rfm.Packeter(extractor.payload)
            dump_rfm(extractor)
