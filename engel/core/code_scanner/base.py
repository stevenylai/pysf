'''Base and abstract code scanner'''
import asyncio


class Scanner:
    '''Scanner class'''
    def __init__(self, event_loop):
        '''Scanner creator'''
        self.event_loop = event_loop
        self.readers = []

    def read(self):
        '''Read the scanner asynchronously'''
        future = asyncio.Future()
        self.readers.append(future)
        return future
