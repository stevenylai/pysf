'''Listen to RFM packets'''
import asyncio


@asyncio.coroutine
def dump_packets(device):
    '''Dump all packets'''
    while True:
        packet = yield from device.read()
        rfm_packet = packet.payload
        src = rfm_packet.src
        dest = rfm_packet.dest
        rfm_type = rfm_packet.type
        length = rfm_packet.length
        rssi = (
            packet.header.rssi
            if packet.header_length > 0
            and packet.header.type == packet.header.RFM_HEADER_RSSI
            else None
        )
        payload = rfm_packet.payload.get_raw_packet()
        print(
            'src: {src}, type: {type}, dest: {dest}, '
            'rssi: {rssi}, payload: {payload}'.format(
                src=hex(src), type=hex(rfm_type), dest=hex(dest),
                rssi="N/A" if rssi is None else str(rssi),
                payload=payload
            )
        )

if __name__ == '__main__':
    from . import base
    event_loop = asyncio.get_event_loop()
    device = base.Device(event_loop)
    args_parser = device.cmdline_parser()
    device.cmdline_parsed()
    device.open()
    event_loop.run_until_complete(dump_packets(device))
