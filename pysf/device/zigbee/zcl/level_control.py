'''Level control cluster'''
from . import base
CLUSTER_ID = 0x0008
ATTRIBUTES = {
    'current_level': {
        'name': 'ATTRID_LEVEL_CURRENT_LEVEL',
        'id': 0x0000,
    },
}


class Device(base.Device):
    '''ZCL device class which supports level control cluster'''
    COMMAND_LEVEL_MOVE_TO_LEVEL = 0x00

    def move_to_level(self, addr, src_ep, seq, disable_default_rsp,
                      level, transtime=0):
        '''Change level command'''
        from ...protocol.zigbee import command
        level_cmd = command.OneByteCommand()
        level_cmd.one_byte = level
        transtime_cmd = command.TwoByteCommand()
        transtime_cmd.low_byte = transtime & 0xFF
        transtime_cmd.high_byte = transtime >> 8 & 0xFF
        self.zcl_command(addr, src_ep, CLUSTR_ID, self.COMMAND_OFF, 1,
                         command.Packet.ZCL_FRAME_CLIENT_SERVER_DIR, 0, seq,
                         disable_default_rsp, [level_cmd, transtime_cmd])
