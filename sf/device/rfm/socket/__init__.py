'''RFM socket'''
from .. import base
from ....protocol.rfm import toggled_type


class Device(base.Device):
    '''RFM Socket'''
    def filter_packet(self, raw_packet):
        '''Filter out rfm packets which are not related
        to rfm_sockets
        '''
        packet = super().filter_packet(raw_packet)
        if packet is None:
            return packet
        rfm_packet = packet.payload
        if rfm_packet.type in {
                rfm_packet.TYPE_EXIST,
                toggled_type(rfm_packet.TYPE_EXIST),
                rfm_packet.TYPE_SOCKET_POWER,
                toggled_type(rfm_packet.TYPE_SOCKET_POWER),
                rfm_packet.TYPE_SOCKET_STATUS,
                toggled_type(rfm_packet.TYPE_SOCKET_STATUS),
        }:
            return packet
        return None

    def packet_payload_string(self, rfm_packet):
        '''Socket payload string'''
        if rfm_packet.type == rfm_packet.TYPE_SOCKET_POWER:
            return (
                'voltage: {voltage}, current {current}, '
                'power: {power}, frequency: {frequency}'.format(
                    voltage=rfm_packet.payload.voltage,
                    current=rfm_packet.payload.current,
                    power=rfm_packet.payload.power,
                    frequency=rfm_packet.payload.frequency
                )
            )
        elif rfm_packet.type in {
                rfm_packet.TYPE_SOCKET_STATUS,
                toggled_type(rfm_packet.TYPE_SOCKET_STATUS),
        }:
            return 'on_off: {on_off}'.format(
                on_off=rfm_packet.payload.status
            )
        else:
            return super().packet_payload_string(rfm_packet)
