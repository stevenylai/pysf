'''Produce lights on a desktop Linux computer'''
import asyncio
from engel.core.production_line import base


class Production(base.Production):
    '''Production line'''
    @asyncio.coroutine
    def wait_for_light(self):
        '''Wait for a light to join the network'''
        pass

    @asyncio.coroutine
    def control_light(self):
        '''Accept input from panel and test the light via control'''
        pass

    @asyncio.coroutine
    def confirm_light(self):
        '''Notify the server and confirm the production of a light'''
        pass

    @asyncio.coroutine
    def watch_events(self):
        '''Event watcher'''
        from . import settings
        while True:
            panel_input = yield from self.devices['panel'].read()
            if panel_input == settings.BUTTON_STOP:
                self.interrupt()

def start():
    '''Start the production line'''
    from . import build_production
