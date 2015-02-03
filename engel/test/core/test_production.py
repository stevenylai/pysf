'''Test production line'''
import unittest
import asyncio
import os
from ...core.production_line import test


class Base(unittest.TestCase):
    '''Production base test case'''
    def setUp(self):
        '''Setup test'''
        self.event_loop = asyncio.get_event_loop()
        self.production = None

    def test_production(self):
        '''Run the test'''
        if self.production is not None:
            asyncio.wait(
                [self.production.start(),
                 self.production.watch_events()],
                loop=self.event_loop
            )


class Production(test.Production):
    '''Test production line'''
    @asyncio.coroutine
    def dummy_state(self):
        '''Dummy state'''
        pass

    def get_test_data_dir(self):
        '''Get the directory for test cases'''
        return os.path.join(os.path.dirname(__file__), 'test_production')


class TestProduction(Base):
    '''Production base test case'''
    def setUp(self):
        '''Setup test'''
        super().setUp()
        self.production = Production(
            self.event_loop, {}, 'dummy_state', self
        )

if __name__ == '__main__':
    unittest.main()
