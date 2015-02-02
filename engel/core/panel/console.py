'''Command line console panel'''
import sys
import os
from . import base


class Panel(base.Panel):
    '''Command line panel'''
    def __init__(self, event_loop, encode='utf-8'):
        '''Create panel'''
        super().__init__(event_loop)
        self.encode = encode

    def read_command(self):
        '''Read command line'''
        line = sys.stdin.readline().strip(os.linesep)
        for future in self.readers:
            future.set_result(bytes(line, self.encode))
        self.readers.clear()

    def open(self):
        '''Open the panel'''
        self.event_loop.add_reader(sys.stdin.fileno(),
                                   self.read_command)

    def write(self, output):
        '''Write to console'''
        sys.stdout.write(output.decode(self.encode))
