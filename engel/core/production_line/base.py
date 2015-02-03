'''Base production line'''
import asyncio


class Production:
    '''Production base class'''
    def __init__(self, event_loop, device_table, initial_state):
        '''Create production line.
        device_table is a dictionary containing the states and
        the corresponding devices. At the top level of the dictionary,
        are the states' names as the key.
        Then for each state, there is a dictionary of the following
        structure:
        {
            'active': [list of active device for that state],
            'wait': [list of devices which need to be waited for]
        }
        '''
        self.event_loop = event_loop
        self.device_table = device_table
        self.state = initial_state
        self.stopped = False
        self.active_devices = []
        self.devices = {}
        for item in self.device_table.values():
            self.devices[item.name] = item

    @asyncio.coroutine
    def change_state(self, new_state):
        '''Change the state'''
        if new_state in self.device_table:
            self.active_devices = self.device_table[new_state]['active']
        self.state = new_state
        state_handler = getattr(self, new_state)
        next_state = yield from state_handler()
        return next_state

    def interrupt(self, exc=None):
        '''Interrupt the production'''
        for device in self.active_devices:
            device.interrupt(exc)

    @asyncio.coroutine
    def watch_events(self):
        '''Event watcher'''
        pass

    @asyncio.coroutine
    def start(self):
        '''Start production'''
        next_state = self.state
        while not self.stopped:
            try:
                next_state = yield from self.change_state(next_state)
            except InterruptedError:
                next_state = self.state
