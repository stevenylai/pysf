'''Zigbee light device'''
import time
from ..zcl import on_off, level_control


class Device(on_off.Device, level_control.Device):
    '''Light with on/off and level control clusters'''
    end_point = 1

    def __init__(self, event_loop, bindable='127.0.0.1:3000', key=b''):
        '''Create light device.
        Add attributes to support smooth level commands
        '''
        super().__init__(event_loop, bindable, key)
        self.current_level = 0
        self.initial_level = 0
        self.move_level_upward = False
        self.move_start_at = None

    def attribute_read(self, zigbee_packet, is_read, attribute):
        '''Print it out'''
        current = time.time()
        if is_read:
            print(int(current), hex(zigbee_packet.payload.src.short_addr),
                  'read', attribute)
        else:
            print(int(current), hex(zigbee_packet.payload.src.short_addr),
                  'report', attribute)
        return True

    def extract_read(self, zigbee_packet):
        '''Extract read. Update current_level if possible'''
        extracted = super().extract_read(zigbee_packet)
        if extracted is not None:
            for item in extracted:
                if 'current_level' in item:
                    self.current_level = item['current_level']
                    break
        return extracted
