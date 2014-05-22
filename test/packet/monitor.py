import re
import sys
import select
import argparse
import logging
import logging.handlers

class Monitor:
    def __init__(self, hub, key=b'', socket=0x181818):
        from ...core.SFSource import SFSource
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter(fmt='%(asctime)s:%(levelname)s - %(message)s', datefmt='%m/%d/%Y %H:%M:%S')

        log_filename = hub
        m = re.compile('[^:]+').search(hub)
        if m != None:
            log_filename = m.group()

        file_handler = logging.handlers.RotatingFileHandler(log_filename + '_' + hex(socket) + '.log',
                                                            maxBytes=1024*1024*32, backupCount=4)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        self.sf = SFSource(None, hub)
        self.key = key
        self.socket = socket

    def get_packet_string(self, packet):
        buffer = ""
        if packet == None:
            return buffer
        else:
            for b in packet.packet:
                buffer = buffer + '{0:02X} '.format(b)
            return buffer

    def socket_match(self, rfm_packet):
        if self.socket == 0x181818:
            return True
        return rfm_packet.src == self.socket or rfm_packet.dest == self.socket

    def monitor(self):
        from ...packet import pkt
        self.logger.info("Start monitoring")
        self.sf.open(self.key)
        while True:
            r,w,x = select.select([self.sf], [], [])
            if len(r) > 0:
                packet_raw = self.sf.readPacket()
                packet = pkt.Packet(packet_raw)
                if self.socket_match(packet.payload):
                    self.logger.info("RFM src: 0x%06x, type: 0x%02x, dest: 0x%06x, payload: %s",
                                     packet.payload.src,
                                     packet.payload.type,
                                     packet.payload.dest,
                                     self.get_packet_string(packet.payload.payload))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Monitor socket(s) from a hub.')
    parser.add_argument('hub', metavar='ip:port', type=str, nargs=1,
                        help='ip:port of the hub running sf')
    parser.add_argument('--key', metavar='bind_secret', type=str, nargs=1,
                        help='bind secret to access the hub')
    parser.add_argument('--socket', metavar='rf_addr', type=str, nargs=1,
                        help='rf_addr of the socket to be monitored')
    args = parser.parse_args()

    hub = None
    if args.hub != None:
        hub = args.hub[0]

    key = b''
    if args.key != None:
        key = bytes(args.key[0], 'utf-8')

    socket = 0x181818
    if args.socket != None:
        try:
            socket = int(args.socket[0])
        except:
            try:
                socket = int(args.socket[0], 8)
            except:
                socket = int(args.socket[0], 16)
            
    print(hub, socket, key)
    if hub != None:
        monitor = Monitor(hub, key, socket)
        monitor.monitor()
