'''Listen to RFM sockets'''
import asyncio
from . import Device as Base
from ....protocol import rfm


class Device(Base):
    '''Socket listener'''
    def __init__(self, event_loop, bindable='127.0.0.1:3000', key=b''):
        '''Create socket listener'''
        super().__init__(event_loop, bindable, key)
        self.listened = rfm.Payload.ADDR_RFM_BCAST

    def cmdline_parser(self):
        '''Get command parser for socket listener'''
        super().cmdline_parser()
        self.arg_parser.add_argument(
            '--monitored', metavar='monitored', type=str,
            help='RFM address (hex) of the socket to be monitored',
        )
        return self.arg_parser

    def cmdline_parsed(self):
        '''Get the parsed cmdline args'''
        args = super().cmdline_parsed()
        if args.monitored is not None:
            try:
                self.listened = int(args.monitored, 16)
            except ValueError:
                pass
        return args

    def filter_packet(self, raw_packet):
        '''RFM address-based filtering'''
        packet = super().filter_packet(raw_packet)
        if packet is None:
            return packet
        else:
            from .. import addr_match
            rfm_packet = packet.payload
            if self.listened == rfm.Payload.ADDR_RFM_BCAST:
                return packet
            elif (
                rfm_packet.src == self.listened or
                rfm_packet.dest == self.listened
            ):
                return packet
            else:
                return None

if __name__ == '__main__':
    from ... import listen
    listener = listen.Listener(Device)
    listener.listen()
