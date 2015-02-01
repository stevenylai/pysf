'''Device base class'''
import re
import argparse
import asyncio


class Device:
    '''Base device abstraction using asyncio'''
    def __init__(self, event_loop, bindable='127.0.0.1:3000', key=b''):
        '''Device creation'''
        from ..core.SFSource import SFSource
        self.event_loop = event_loop
        self.sf = SFSource(None, bindable)
        self.key = key
        self.arg_parser = argparse.ArgumentParser()
        self.readers = []

    def cmdline_parser(self):
        '''Get the command line parser'''
        self.arg_parser.add_argument(
            '--bindable', metavar='ip:port', type=str,
            help='ip:port of the bindable device running sf'
        )
        self.arg_parser.add_argument(
            '--key', metavar='bind_secret', type=str,
            help='bind_secret of the bindable device running sf'
        )
        return self.arg_parser

    def cmdline_parsed(self):
        '''Get the parsed cmdline args'''
        from ..core.SFSource import SFSource
        args = self.arg_parser.parse_args()
        if args.bindable is not None:
            self.sf = SFSource(None, args.bindable)
        if args.key is not None:
            self.key = bytes(args.key, 'utf-8')
        return args

    def filter_packet(self, packet):
        '''Filter packet. This method can be overridden
        to return packets which are not raw or to return
        None for packets which are not of interest
        '''
        return packet

    def _read_sf_packet(self):
        '''Read SF packet'''
        packet = self.sf.readPacket()
        packet = self.filter_packet(packet)
        if packet is not None:
            for future in self.readers:
                future.set_result(packet)
            self.readers.clear()

    def open(self):
        '''Open the device'''
        self.sf.open(self.key)
        self.event_loop.add_reader(self.sf.fileno(), self._read_sf_packet)

    def close(self):
        '''Close the device'''
        self.sf.close()
        for future in self.readers:
            future.set_exception(EOFError('Connection closed'))
        self.readers.clear()

    def write(self, packet):
        '''Write a packet to device'''
        self.sf.writePacket(packet)

    def read(self):
        '''Read from device'''
        read_future = asyncio.Future()
        self.readers.append(read_future)
        return read_future

    def packet_string(self, packet):
        '''Packet string'''
        return packet
