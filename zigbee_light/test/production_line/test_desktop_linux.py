'''Testing'''
import os
import unittest
import asyncio
from ...production_line import desktop_linux
from ...core.device import sim
from engel.core.production_line import test
from engel.test.core import test_production


class Production(test.Production, desktop_linux.Production):
    '''Test line with methods overridden'''
    def get_test_data_dir(self):
        '''Get the directory for test cases'''
        return os.path.join(os.path.dirname(__file__), 'desktop_linux')

    @asyncio.coroutine
    def confirm_light(self):
        '''Notify the server and confirm the production of a light'''
        print("Confirming", self.light_info)
        return 'wait_for_light'

    @asyncio.coroutine
    def start(self):
        '''start'''
        yield from super().start()
        self.devices['panel'].update(None)

class TestProduction(test_production.Base):
    '''Production base test case'''
    def setUp(self):
        '''Setup the test production system'''
        super().setUp()
        light = sim.Light(self.event_loop)
        scanner = sim.Scanner(self.event_loop)
        panel = sim.Panel(self.event_loop)
        self.production = Production(
            self.event_loop, {
                'wait_for_light': {'active': [light]},
                'control_light': {'active': [light]},
                'all': [light, scanner, panel],
            }, 'wait_for_light', self
        )

if __name__ == '__main__':
    unittest.main()
