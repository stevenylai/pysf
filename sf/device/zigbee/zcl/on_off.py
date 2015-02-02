'''On/off cluster'''
from . import base
CLUSTER_ID = 0x0006
ATTRIBUTES = {
    'on_off': {
        'name': 'ATTRID_ON_OFF',
        'id': 0x0000,
    },
}


class Device(base.Device):
    '''ZCL device class which supports on/off cluster'''
    COMMAND_OFF = 0x00
    COMMAND_ON = 0x01

    def on(self, addr, src_ep, seq, disable_default_rsp):
        '''Turn on'''
        from ....protocol.zigbee import command
        self.zcl_command(addr, src_ep, CLUSTER_ID, self.COMMAND_ON, 1,
                         command.Packet.ZCL_FRAME_CLIENT_SERVER_DIR,
                         0, seq, disable_default_rsp, [])

    def off(self, addr, src_ep, seq, disable_default_rsp):
        '''Turn off'''
        from ....protocol.zigbee import command
        self.zcl_command(addr, src_ep, CLUSTER_ID, self.COMMAND_OFF, 1,
                         command.Packet.ZCL_FRAME_CLIENT_SERVER_DIR,
                         0, seq, disable_default_rsp, [])
