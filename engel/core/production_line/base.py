'''Base production line'''
import asyncio


class Production:
    '''Production base class'''
    def __init__(self, event_loop, device_table, initial_state):
        '''Create production line'''
        self.event_loop = event_loop
        self.device_table = device_table
        self.initial_state = initial_state
        self.active_devices = []
        self.devices = {}
        for item in self.device_table.values():
            self.devices[item.name] = item

    @asyncio.coroutine
    def change_state(self, new_state):
        '''Change the state'''
        self.active_devices = self.device_table[new_state]['devices']
        self.state = new_state
        state_handler = getattr(self, new_state)
        yield from state_handler()

    def interrupt(self, exc=None):
        '''Interrupt the production'''
        for device in self.active_devices:
            device.interrupt(exc)

    @asyncio.coroutine
    def start(self):
        '''Start production'''
        yield from self.change_state(self.initial_state)
