'''ZCL attribute read'''
from . import base


class Read(base.CommandGen):
    '''ZCL read commands'''
    def __init__(self, attrs):
        '''Create a read command'''
        self.attrs = attrs

    def get_commands(self):
        '''Get read commands'''
        commands = []
        for attr in self.attrs:
            commands.append(self.two_byte(attr))
        return commands
