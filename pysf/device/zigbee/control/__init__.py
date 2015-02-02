'''Zigbee controller'''
import functools


def device_selected(func):
    '''Decorator to ensure the device is selected'''
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        '''wrapper'''
        self = args[0]
        if self.current_device is None:
            print('Device not selected')
            return None
        else:
            return func(*args, **kwargs)
    return wrapper
