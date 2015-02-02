'''Zigbee light device'''
from ..zcl import on_off, level_control


class Device(on_off.Device, level_control.Device):
    '''Light with on/off and level control clusters'''
    end_point = 1

    def attribute_read(self, is_read, attribute):
        '''Print it out'''
        if is_read:
            print('read', attribute)
        else:
            print('report', attribute)
        return True
