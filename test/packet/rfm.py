import select

def dump_rfm(packet):
    from ...packet import rfm
    print("RFM src:", hex(packet.src),
          "type:", hex(packet.type),
          "dest:", hex(packet.dest),
          "len:", packet.length)
    if packet.type == rfm.RFM_SOCKET_DATA:
        print("Socket voltage:", packet.payload.voltage,
              "current:", packet.payload.current,
              "power:", packet.payload.power,
              "freq:", packet.payload.freq)
    elif packet.type == rfm.RFM_SOCKET_STATUS or packet.type == rfm.RFM_SOCKET_EXIST:
        print("Socket status:", hex(packet.payload.status))

def dump_pkt(packet):
    #print("PKT type:", hex(packet.type),
          #"header len:", packet.header_length,
          #"payload len:", packet.payload_length)
    dump_rfm(packet.payload)

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
            packet = pkt.Packeter(packet)
            dump_pkt(packet)
