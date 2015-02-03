'''Production line for testing'''
import asyncio
import os
import re
import json
from . import base


class Production(base.Production):
    '''Production line for testing'''
    def __init__(self, event_loop, device_table, initial_state, tester=None):
        '''Create a testing line'''
        super().__init__(event_loop, device_table, initial_state)
        self.tester = tester
        self.data_dir = self.get_test_data_dir()
        self.all_cases = sorted([
            d for d in os.listdir(self.data_dir)
            if os.path.isdir(os.path.join(self.data_dir, d))
        ])
        self.current_case_idx = 0

    @property
    def current_data_dir(self):
        '''Get current data dir'''
        return self.all_cases[self.current_case_idx]

    def get_test_data_dir(self):
        '''Get the directory for test cases'''
        return os.path.dirname(__file__)

    def get_state_info(self):
        '''Get the state info'''
        state_info_file = os.path.join(self.current_case_state,
                                       'state_info.json')
        if os.path.isfile(state_info_file):
            with open(state_info_file, 'r') as state_info:
                return json.load(state_info)
        return None

    def load_test_data(self, state):
        '''Load the test data'''
        self.current_case_state = os.path.join(
            self.data_dir, self.current_data_dir, state
        )
        if not os.path.isdir(self.current_case_state):
            return None
        state_info = self.get_state_info()
        data_files = [
            f for f in os.listdir(self.current_case_state)
            if f.endswith('.json') and f != 'state_info.json'
        ]
        for data_file in data_files:
            with open(data_file, 'r') as data_content:
                test_data = json.load(data_content)
            match = re.compile(r'(.+)\.json').search(data_file)
            if match is not None:
                self.devices[match.group(1)].update(test_data)
        if state_info is not None:
            if state_info['finish']:
                self.current_case_idx += 1
                if self.current_case_idx >= len(self.all_cases):
                    self.stopped = True
        return state_info

    @asyncio.coroutine
    def change_state(self, new_state):
        state_info = self.load_test_data(new_state)
        next_state = yield from super().change_state(new_state)
        if state_info is not None and self.tester is not None:
            self.tester.assertEqual(next_state,
                                    state_info['next_state'])
        return next_state
