'''Zigbee console (command line) controller'''
import re
import os
import sys
import threading
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
        self.input_thread = None

    def read_input(self):
        '''Wait for input from user and process them in a loop'''
        while True:
            self.zigbee_console_command()

    def zigbee_console_command(self):
        '''Process Zigbee commands from console'''
        line = sys.stdin.readline().strip(os.linesep)
        match = re.compile('^[0-9]+$').search(line)
        if match is not None:
            control_idx = int(match.group())
            if control_idx < len(self.device_list):
                self.current_control = control_idx
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
                                       self.zigbee_console_command)
        else:
            self.input_thread = threading.Thread(target=self.read_input)
            self.input_thread.start()
