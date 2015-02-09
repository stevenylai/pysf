'''Zigbee console (command line) controller'''
import asyncio
import re
import os
import sys
from ... import listen


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
        super().create_device()
        self.event_loop.add_reader(sys.stdin,
                                   self.zigbee_console_command)
