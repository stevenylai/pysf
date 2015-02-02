'''Scanner reader'''
import asyncio


class Reader:
    '''Reader class'''
    def __init__(self, scanner_cls):
        '''Create reader'''
        self.scanner_cls = scanner_cls
        self.scanner = None
        self.event_loop = asyncio.get_event_loop()

    def read_forever(self, *args, **kwargs):
        '''Read the scanner forever'''
        self.scanner = self.scanner_cls(self.event_loop, *args, **kwargs)
        self.scanner.open()
        self.event_loop.run_until_complete(self._do_read_forever())

    @asyncio.coroutine
    def _do_read_forever(self, *args, **kwargs):
        while True:
            code = yield from self.scanner.read()
            print(code)
