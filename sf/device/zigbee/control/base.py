'''Zigbee base controller'''
from ... import listen


class Control(listen.Listener):
    '''Zigbee base control for:

    * on/off
    * resolve address

    '''
    def __init__(self, device_cls):
        '''Create a Zigbee base controller'''
        super().__init__(device_cls)
        self.device_list = []
        self.current_control = 0

    def process_zigbee_packet(self, zigbee_packet):
        '''Process Zigbee packet'''
        print(zigbee_packet.get_raw_packet())

    def zigbee_list_changed(self):
        '''Invoked when there's any change to the
        Zigbee device list
        '''
        print('_______________________________')
        i = 0
        for i in range(0, len(self.device_list)):
            if i != self.current_control:
                print('|', i, hex(self.device_list[i]['mac']),
                      hex(self.device_list[i]['addr']))
            else:
                print('|*', i, hex(self.device_list[i]['mac']),
                      hex(self.device_list[i]['addr']))

    def add_zigbee(self, new_dev, addr_info):
        '''Add a new Zigbee device to the device list'''
        if new_dev['mac'] not in [dev['mac'] for dev in self.device_list]:
            self.device_list.append(new_dev)
            self.current_control = len(self.device_list) - 1
        else:
            cur_idx = [
                dev['mac'] for dev in self.device_list
            ].index(new_dev['mac'])
            self.device_list.remove(self.device_list[cur_idx])
            self.device_list.insert(cur_idx, new_dev)
        self.zigbee_list_changed()

    def post_process_packet(self, packet):
        '''Post process packet'''
        zigbee_packet = packet.payload
        if zigbee_packet.type == zigbee_packet.TYPE_RESOLVE:
            new_dev = {
                'mac': zigbee_packet.payload.mac,
                'addr': zigbee_packet.payload.addr,
            }
            self.add_zigbee(new_dev, zigbee_packet.payload)
        self.process_zigbee_packet(zigbee_packet)

    @property
    def current_device(self):
        '''Get current device'''
        if self.current_control < 0 or \
           self.current_control >= len(self.device_list):
            return None
        else:
            return self.device_list[self.current_control]

    def resolve(self, mac):
        '''Resolve a device zigbee address'''
        self.device.resolve(mac)

    def pair(self):
        '''Pair a device'''
        from ....protocol import zigbee
        if self.current_device is not None:
            self.device.do_pair(
                zigbee.Payload.TYPE_PAIR, self.current_device['mac'],
                self.current_device['addr']
            )

    def unpair(self):
        '''Unpair a device'''
        from ....protocol import zigbee
        if self.current_device is not None:
            self.device.do_pair(
                zigbee.Payload.TYPE_LEAVE, self.current_device['mac'],
                self.current_device['addr']
            )
            self.device.do_pair(
                zigbee.Payload.TYPE_UNPAIR, self.current_device['mac'],
                self.current_device['addr']
            )
            self.device_list.remove(self.device_list[self.current_control])
            if self.current_control > 0:
                self.current_control -= 1
            self.zigbee_list_changed()
