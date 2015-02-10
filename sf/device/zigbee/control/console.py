'''Zigbee console (command line) controller'''
import re
import os
import sys
import asyncio
from . import base


def _convert_args(arg):
    '''Convert string arg to different types
    according to their pattern
    '''
    match = re.compile('^[0-9]+$').search(arg)
    if match is not None:
        return int(arg)
    match = re.compile('^0[xX][0-9A-Fa-f]+').search(arg)
    if match is not None:
        return int(arg, 16)
    return arg


class Control(base.Control):
    '''Zigbee console controller class.
    In addition to monitoring the zigbee packets,
    this controller will also monitor input from
    stdin and process those inputs as control commands
    '''
    def __init__(self, device_cls):
        '''Create a Zigbee base controller'''
        super().__init__(device_cls)
        self.console_on_thread = False

    def read_input_thread(self):
        '''Wait for input from user and process them in a loop'''
        while True:
            line = sys.stdin.readline().strip(os.linesep)
            if line == 'quit':
                for future in self.device.readers:
                    future.set_exception(InterruptedError('Stop'))
                break
            self.zigbee_console_command(line)

    def read_input_event(self):
        '''Wait for input from user and process them in a loop'''
        line = sys.stdin.readline().strip(os.linesep)
        self.zigbee_console_command(line)

    def zigbee_console_command(self, line):
        '''Process Zigbee commands from console'''
        match = re.compile('^[0-9]+$').search(line)
        if match is not None:
            control_idx = int(match.group())
            if control_idx < len(self.device_list):
                self.current_control = control_idx
                self.zigbee_list_changed()
            return
        args = []
        for match in re.compile('[^ \t]+').finditer(line):
            args.append(_convert_args(match.group()))
        if len(args) < 1:
            return
        if hasattr(self, args[0]):
            func = getattr(self, args[0])
            if not callable(func):
                print("Command not callable:", args[0])
            else:
                func(*args[1:])
        else:
            print("Command not avail:", args[0])

    def create_device(self):
        '''Create device for control'''
        self.device = self.device_cls(self.event_loop)
        parser = self.device.cmdline_parser()
        parser.add_argument(
            '--thread', action='store_true',
            help='If the input is read on a separate thread (for Windows)'
        )
        args = self.device.cmdline_parsed()
        self.console_on_thread = args.thread
        if not self.console_on_thread:
            self.event_loop.add_reader(sys.stdin.fileno(),
                                       self.read_input_event)

    def listen(self):
        '''Listen to the device'''
        self.create_device()
        self.device.open()
        if not self.console_on_thread:
            self.event_loop.run_until_complete(
                self.process_packets()
            )
        else:
            self.event_loop.run_until_complete(
                asyncio.wait(
                    [
                        self.process_packets(),
                        self.event_loop.run_in_executor(
                            None, self.read_input_thread
                        )
                    ]
                )
            )
