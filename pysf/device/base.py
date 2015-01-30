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

    def read_sf_packet(self):
        '''Read SF packet'''
        packet_raw = self.sf.readPacket()
        print(packet_raw)

    def open(self):
        '''Open the device'''
        self.sf.open(self.key)
        self.event_loop.add_reader(self.sf.fileno(), self.read_sf_packet)

    def close(self):
        '''Close the device'''
        self.sf.close()

    def write(self, packet):
        pass

    def read(self):
        pass

if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    device = Device(event_loop)
    args_parser = device.cmdline_parser()
    device.cmdline_parsed()
    device.open()
    event_loop.run_forever()
