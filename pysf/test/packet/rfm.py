import time
import select
import argparse

class RfmSocket:
    def __init__(self, host, key=b''):
        from ...core.SFSource import SFSource
        self.sf = SFSource(None, host)
        self.key = key

    def print_raw_packet(self, packet):
        print("PKT type:", hex(packet.type),
              "header len:", packet.header_length,
              "payload len:", packet.payload_length)

    def print_rfm_socket(self, packet):
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

    def listen(self):
        self.sf.open(self.key)
        while True:
            r,w,x = select.select([self.sf], [], [])
            if len(r) > 0:
                packet = self.sf.readPacket()
                print("Raw packet:", packet)
                packet = pkt.Packet(packet)
                self.print_rfm_socket(packet)

    def write(self, packet):
        print("Writing", packet)
        self.sf.writePacket(packet)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rfm socket listener.')
    parser.add_argument('hub', metavar='ip:port', type=str, nargs='?',
                        default='127.0.0.1:3000', help='ip:port of the hub running sf')
    parser.add_argument('--key', metavar='bind_secret', type=str, nargs='?',
                        default='', help='bind secret of the hub running sf')
    args = parser.parse_args()
    tester = RfmSocket(args.hub, bytes(args.key, 'utf-8'))
    tester.listen()

