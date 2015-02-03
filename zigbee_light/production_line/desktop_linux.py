'''Produce lights on a desktop Linux computer'''
import asyncio
from engel.core.production_line import base

BUTTON_STOP = b's'
BUTTON_CONFIRM = b'c'
BUTTON_ON = b'n'
BUTTON_OFF = b'f'


class Production(base.Production):
    '''Production line'''
    @asyncio.coroutine
    def wait_for_light(self):
        '''Wait for a light to join the network'''
        self.light_info = yield from self.devices['light'].read()
        return 'control_light'

    @asyncio.coroutine
    def control_light(self):
        '''Accept input from panel and test the light via control'''
        button_pressed = None
        while button_pressed != BUTTON_CONFIRM:
            button_pressed = yield from self.devices['panel'].read()
            if button_pressed == BUTTON_ON:
                self.devices['light'].on()
            elif button_pressed == BUTTON_OFF:
                self.devices['light'].off()
            elif button_pressed == BUTTON_CONFIRM:
                return 'confirm_light'

    @asyncio.coroutine
    def confirm_light(self):
        '''Notify the server and confirm the production of a light'''
        # TODO: access server
        print("Confirming", self.light_info)
        return 'wait_for_light'

    def interrupt(self, exc=None):
        '''Interrupt the line'''
        self.state = 'wait_for_light'
        super().interrupt(exc)

    @asyncio.coroutine
    def watch_events(self):
        '''Event watcher'''
        while not self.stopped:
            panel_input = yield from self.devices['panel'].read()
            if panel_input == BUTTON_STOP:
                self.interrupt()
