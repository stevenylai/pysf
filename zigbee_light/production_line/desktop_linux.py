'''Produce lights on a desktop Linux computer'''
import asyncio
import pprint
import copy
import json
import aiohttp
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
        print('Device found:', self.light_info)
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
                break
        self.devices['light'].clear()
        return 'confirm_light'

    @asyncio.coroutine
    def submit_light(self, code):
        '''Submit the light info'''
        from . import settings
        payload = copy.copy(settings.ZIGBEE_LIGHT_PARAMS)
        payload['device_data'] = json.dumps(
            {
                'label': code,
                'mac': self.light_info['mac']
            }
        )
        print("Submitting to ", settings.ZIGBEE_LIGHT_URL, "with", payload)
        resp = yield from aiohttp.request(
            'post', settings.ZIGBEE_LIGHT_URL, params=payload
        )
        resp_text = yield from resp.text()
        return resp_text

    @asyncio.coroutine
    def confirm_light(self):
        '''Notify the server and confirm the production of a light'''
        code = yield from self.devices['scanner'].read()
        result = yield from self.submit_light(code.decode('utf-8'))
        print("Confirmed:", pprint.pformat(self.light_info, indent=1),
              code.decode('utf-8'), "Result:", result)
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


def start(scanner_name):
    '''Start the line'''
    from ..core.device import light
    from engel.core.code_scanner import evdev
    from engel.core.panel import console

    event_loop = asyncio.get_event_loop()
    # light = light.Light(event_loop, bindable='192.168.1.47:3000')
    light = light.Light(event_loop)
    light.open()
    scanner = evdev.Scanner(event_loop, scanner_name)
    scanner.open()
    panel = console.Panel(event_loop)
    panel.open()
    production = Production(
        event_loop, {
            'wait_for_light': {'active': [light]},
            'control_light': {'active': [light]},
            'confirm_light': {'active': [scanner]},
            'all': [light, scanner, panel],
        }, 'wait_for_light'
    )
    event_loop.run_until_complete(
        asyncio.wait(
            [production.start(),
             production.watch_events()],
            loop=event_loop
        )
    )

if __name__ == '__main__':
    start('OKE Electron Company')
