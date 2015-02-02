'''Scanner based on Linux evdev'''
import re
import argparse
import logging
import evdev
from . import base

LOGGER = logging.getLogger(__name__)
KEYS = (
    "X^1234567890-XXXqwertzuiopXXXXasdfghjkl"
    "XXXXXyxcvbnmXX/XXXXXXXXXXXXXXXXXXXX"
)
CAPKEYS = (
    "X^!@#$%^&*()_XXXQWERTZUIOPXXXXASDFGHJKL"
    "XXXXXYXCVBNMXX?XXXXXXXXXXXXXXXXXXXX"
)


class Scanner(base.Scanner):
    '''Code scanner class.
    The codes scanned are actually ASCII
    but are converted according to the encoding settings
    '''
    def __init__(self, event_loop, name_pattern, encode='utf-8'):
        '''Create scanner'''
        super().__init__(event_loop)
        self.dev_node = None
        self.encode = encode
        pattern = re.compile(name_pattern)
        devices = map(evdev.InputDevice, evdev.list_devices())
        self.reset()
        for dev in devices:
            if pattern.search(dev.name) is not None:
                self.dev_node = dev.fn
        if self.dev_node is None:
            raise FileNotFoundError(
                "Cannot find scanner with name like " + name_pattern
            )
        else:
            self.device = evdev.device.InputDevice(self.dev_node)

    def reset(self):
        '''Reset the scanner's state'''
        self.readers.clear()
        self.code = ""
        self.lshift = None
        self.rshift = None

    def open(self):
        '''Open scanner for reading'''
        self.event_loop.add_reader(self.device.fileno(), self._process_event)

    def _process_event(self):
        '''Process events. Capture the codes
        and notify the readers if ready
        '''
        event = self.device.read_one()
        if event.type != evdev.ecodes.EV_KEY:
            return None
        if event.code == evdev.ecodes.KEY_LEFTSHIFT:
            self.lshift = evdev.categorize(event)
            return None
        if event.code == evdev.ecodes.KEY_RIGHTSHIFT:
            self.rshift = evdev.categorize(event)
            return None
        keys = KEYS
        if (
            self.lshift is not None and
            self.lshift.keystate == evdev.events.KeyEvent.key_down
        ):
            keys = CAPKEYS
        if (
            self.rshift is not None and
            self.rshift.keystate == evdev.events.KeyEvent.key_down
        ):
            keys = CAPKEYS

        if event.value == evdev.events.KeyEvent.key_down:
            if event.code == evdev.ecodes.KEY_ENTER:
                for future in self.readers:
                    future.set_result(bytes(self.code, self.encode))
                self.reset()
                return
            self.code = self.code + keys[event.code]
            if keys[event.code] == 'X' and event.code != evdev.ecodes.KEY_X:
                LOGGER.warning("Ignoring unexpected code: %s", event.code)

if __name__ == '__main__':
    from . import reader
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        'name', type=str, help='Name of the scanner'
    )
    args = arg_parser.parse_args()
    reader = reader.Reader(Scanner)
    reader.read_forever(args.name)
