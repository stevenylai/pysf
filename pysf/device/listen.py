'''Listen to all raw packets and dump them to the console'''
import asyncio


class Listener:
    '''Device listener'''
    def __init__(self, device_cls):
        '''Create listener'''
        self.device_cls = device_cls
        self.device = None
        self.event_loop = asyncio.get_event_loop()

    def emit(self, packet_string):
        '''Emit packet string'''
        print(packet_string)

    @asyncio.coroutine
    def dump_packets(self):
        '''Dump all packets from the device'''
        while True:
            packet = yield from self.device.read()
            self.emit(self.device.packet_string(packet))

    def create_device(self):
        '''Create device for listening'''
        self.device = self.device_cls(self.event_loop)
        self.device.cmdline_parser()
        self.device.cmdline_parsed()

    def listen(self):
        '''Listen to the device'''
        self.create_device()
        self.device.open()
        self.event_loop.run_until_complete(self.dump_packets())

if __name__ == '__main__':
    from . import base
    listener = Listener(base.Device)
    listener.listen()
