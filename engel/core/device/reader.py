'''Device reader'''
import asyncio


class Reader:
    '''Reader class'''
    def __init__(self, device_cls):
        '''Create reader'''
        self.device_cls = device_cls
        self.device = None
        self.event_loop = asyncio.get_event_loop()

    def read_forever(self, *args, **kwargs):
        '''Read the device forever'''
        self.device = self.device_cls(self.event_loop, *args, **kwargs)
        self.device.open()
        self.event_loop.run_until_complete(self._do_read_forever())

    def emit_result(self, result):
        '''Process the read result'''
        print('Read:', result)

    @asyncio.coroutine
    def _do_read_forever(self, *args, **kwargs):
        '''The main coroutine for reading the codes async'''
        while True:
            result = yield from self.device.read()
            self.emit_result(result)
