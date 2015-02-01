'''Listen to all raw packets and dump them to the console'''
import asyncio


@asyncio.coroutine
def dump_packets(device):
    '''Dump all packets'''
    while True:
        packet = yield from device.read()
        print(packet)

if __name__ == '__main__':
    from . import base
    event_loop = asyncio.get_event_loop()
    device = base.Device(event_loop)
    args_parser = device.cmdline_parser()
    device.cmdline_parsed()
    device.open()
    event_loop.run_until_complete(dump_packets(device))
