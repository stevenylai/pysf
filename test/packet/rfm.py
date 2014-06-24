import time
import select

def dump_rfm(packet):
    from ...packet import rfm
    print("RFM src:", hex(packet.src),
          "type:", hex(packet.type),
          "dest:", hex(packet.dest),
          "len:", packet.length)
    if packet.type == packet.TYPE_SOCKET_DATA:
        print("Socket voltage:", packet.payload.voltage,
              "current:", packet.payload.current,
              "power:", packet.payload.power,
              "freq:", packet.payload.freq)
    elif packet.type == packet.TYPE_SOCKET_STATUS or packet.type == packet.TYPE_SOCKET_EXIST:
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
            print("Raw packet:", packet)
            packet = pkt.Packet(packet)
            dump_pkt(packet)

def gen_packet():
    from ...packet import rfm_socket_data
    from ...packet import rfm_socket_status
    from ...packet import rfm
    from ...packet import pkt
    socket_data = rfm_socket_data.Packet(None, 0)
    socket_data.voltage = 220
    socket_data.current = 0
    socket_data.freq = 50
    socket_data.power = 3000
    print(socket_data.packet)
    socket_status = rfm_socket_status.Packet(bytes(8), 0)
    socket_status.status = socket_status.STATUS_MANUAL_OFF
    rfm_packet = rfm.Packet(None, 0)
    rfm_packet.dest = 0x181818
    rfm_packet.src = 0x1234
    rfm_packet.type = rfm_packet.TYPE_SOCKET_DATA
    rfm_packet.length = 1
    rfm_packet.payload = socket_status.packet
    print(rfm_packet.packet)
    pkt_packet = pkt.Packet(None, 0)
    pkt_packet.type = pkt_packet.TYPE_RFM_PKT
    pkt_packet.header_length = 0
    pkt_packet.payload_length = len(rfm_packet.packet)
    pkt_packet.payload = rfm_packet.packet
    print(pkt_packet.packet)
    return pkt_packet.packet

def ping_pong(sf_addr, max_retrial):
    from ...core.SFSource import SFSource
    sf = SFSource(None, sf_addr)
    sf.open()
    trial = 0
    passed = False
    while trial < max_retrial and not passed:
        packet = gen_packet()
        sf.writePacket(packet)
        remain = 1.0
        start = time.time()
        while remain > 0 and not passed:
            r,w,x = select.select([sf], [], [], remain)
            if len(r) > 0:
                packet = sf.readPacket()
                print("Raw packet:", packet)
                #Check packet here
            end = time.time()
            remain = remain - (end - start)
        if not passed:
            print("Rerunning test")
            trial += 1
    if not passed:
        print("Failed")
    else:
        print("Succeeded")
    sf.close()

def write():
    from ...core.SFSource import SFSource
    sf = SFSource(None, '192.168.1.33:3000')
    sf.open()
    while True:
        packet = gen_packet()
        print("Writing", packet)
        sf.writePacket(packet)
        time.sleep(1)

if __name__ == '__main__':
    ping_pong('192.168.0.17:3000', 2)
    #listen()
    #gen_packet()
    #write()
