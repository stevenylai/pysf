'''Zigbee light device'''
import time
from ..zcl import on_off, level_control


class Device(on_off.Device, level_control.Device):
    '''Light with on/off and level control clusters'''
    end_point = 1

    def attribute_read(self, zigbee_packet, is_read, attribute):
        '''Print it out'''
        current = time.time()
        if is_read:
            print(int(current), hex(zigbee_packet.payload.src.short_addr),
                  'read', attribute)
        else:
            print(int(current), hex(zigbee_packet.payload.src.short_addr),
                  'report', attribute)
            print(zigbee_packet.payload.get_raw_packet())
        return True
