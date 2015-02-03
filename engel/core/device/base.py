'''Base device'''
import asyncio


class Device:
    '''Device class'''
    def __init__(self, event_loop):
        '''Device creator'''
        self.event_loop = event_loop
        self.readers = []

    def open(self):
        '''Open the device'''
        pass

    def read(self):
        '''Read the device asynchronously'''
        future = asyncio.Future()
        self.readers.append(future)
        return future
