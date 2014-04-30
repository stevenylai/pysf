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

def listen():
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

def gen_packet():
    from ...packet import rfm_socket_data
    from ...packet import rfm
    from ...packet import pkt
    socket_data = rfm_socket_data.Packeter(None, 0)
    socket_data.voltage = 220
    socket_data.current = 0
    socket_data.freq = 50
    socket_data.power = 3000
    print(socket_data.packet)
    rfm_packet = rfm.Packeter(None, 0)
    rfm_packet.dest = 0x181818
    rfm_packet.src = 0xa
    rfm_packet.type = rfm.RFM_SOCKET_DATA
    rfm_packet.payload = socket_data.packet
    rfm_packet.length = 8
    print(rfm_packet.packet)

if __name__ == '__main__':
    #listen()
    gen_packet()
