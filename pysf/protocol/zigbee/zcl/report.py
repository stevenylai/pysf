'''ZCL attribute report'''
from . import base


class ReportConfig(base.CommandGen):
    ZCL_SEND_ATTR_REPORTS = 0
    ZCL_EXPECT_ATTR_REPORTS = 1

    def __init__(self, direction=0, attr_id=0, data_type=0,
                 min_interval=0, max_interval=0, timeout=0,
                 threshold=b''):
        '''Create a ZCL report config'''
        from . import base
        self.direction = direction
        self.attr_id = attr_id
        self.data_type = base.ZCL(data_type)
        self.min_interval = min_interval
        self.max_interval = max_interval
        self.threshold = threshold

    def threshold_commands(self, commands):
        '''Generate one-byte commands from threshold value
        and type
        '''
        data = []
        self.data_type.serialize(self.threshold, data)
        for item in data:
            commands.append(self.one_byte(item))

    def get_commands(self):
        '''Convert the report config to a list of ZCL
        commands
        '''
        commands = []
        commands.append(self.one_byte(self.direction))
        commands.append(self.two_byte(self.attr_id))
        if self.direction == self.ZCL_SEND_ATTR_REPORTS:
            commands.append(self.two_byte(self.min_interval))
            commands.append(self.two_byte(self.max_interval))
            self.threshold_commands(commands)
        else:
            commands.append(self.two_byte(self.timeout))
        return commands
