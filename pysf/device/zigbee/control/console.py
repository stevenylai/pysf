'''Zigbee console (command line) controller'''
import asyncio
import re
import os
import sys
from ... import listen


class Control(listen.Listener):
    '''Zigbee console controller class.
    In addition to monitoring the zigbee packets,
    this controller will also monitor input from
    stdin and process those inputs as control commands
    '''
    def zigbee_console_command(self):
        '''Process Zigbee commands from console'''
        line = sys.stdin.readline().strip(os.linesep)
        args = []
        for match in re.compile('[^ \t]+').finditer(line):
            args.append(match.group())
        if hasattr(self, args[0]):
            func = getattr(self, args[0])
            if not callable(func):
                print("Unknown command:", line)
            else:
                func(*args[1:])
        else:
            print("Unknown command:", line)

    def create_device(self):
        '''Create device for control'''
        super().create_device()
        self.event_loop.add_reader(sys.stdin.fileno(),
                                   self.zigbee_console_command)
