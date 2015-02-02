'''RFM base device'''
from .. import base


class Device(base.Device):
    '''Base RFM device'''
    def filter_packet(self, raw_packet):
        '''Filter out those non-RFM packets'''
        from ...protocol import pkt
        packet = pkt.Packet(data=raw_packet)
        if packet.type == packet.TYPE_RFM:
            return packet
        return None

    def packet_payload_string(self, rfm_packet):
        '''RFM packet payload string'''
        return rfm_packet.payload.get_raw_packet()

    def packet_string(self, packet):
        '''RFM packet string'''
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
        payload = self.packet_payload_string(rfm_packet)
        return (
            'src: {src}, type: {type}, dest: {dest}, '
            'rssi: {rssi}, payload: {payload}'.format(
                src=hex(src), type=hex(rfm_type), dest=hex(dest),
                rssi="N/A" if rssi is None else str(rssi),
                payload=payload
            )
        )
