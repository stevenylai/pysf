'''Light device handler'''
from sf.device.zigbee.light import Device
from engel.core.device import interruptable


class Light(Device, interruptable.Device):
    '''Light device class'''
    name = 'light'
    end_point = 1

    def __init__(self, event_loop, bindable='127.0.0.1:3000', key=b''):
        '''Create light'''
        super().__init__(event_loop, bindable, key)
        self.found = None
        self.paired = False

    def filter_packet(self, raw_packet):
        '''Process packet'''
        packet = super().filter_packet(raw_packet)
        if packet is None:
            return None
        if len(self.readers) == 0: # No one is interested
            return None
        zigbee_packet = packet.payload
        if zigbee_packet.type == zigbee_packet.TYPE_RESOLVE and \
           zigbee_packet.payload.type == zigbee_packet.payload.TYPE_ADDR_JOIN:
            found = {
                'mac': zigbee_packet.payload.mac,
                'addr': zigbee_packet.payload.addr
            }
            if self.found is None:
                self.found = found
                self.do_pair(packet.payload.TYPE_PAIR,
                             self.found['mac'], self.found['addr'])
            elif not self.paired:
                if self.found == found:
                    self.paired = True
                    for future in self.readers:
                        future.set_result(self.found)
                    self.readers.clear()
        return None

    @property
    def zigbee_addr(self):
        '''Get zigbee address'''
        from sf.protocol.zigbee import Address
        addr = Address()
        addr.short_addr = self.found['addr']
        addr.mode = addr.ADDR_16BIT
        addr.end_point = self.end_point
        addr.pan_id = 0
        return addr

    def interrupt(self, exc=None):
        '''Process interrupted'''
        self.clear()
        super().interrupt(exc)

    def clear(self):
        '''Clean up'''
        from sf.protocol.zigbee import Payload
        if self.found is not None:
            # Unpair
            self.do_pair(Payload.TYPE_LEAVE,
                         self.found['mac'], self.found['addr'])
            self.do_pair(Payload.TYPE_UNPAIR,
                         self.found['mac'], self.found['addr'])
            # Just to make sure ...
            self.do_pair(Payload.TYPE_UNPAIR,
                         0xFFFFFFFFFFFFFFFF, 0xFFFF)
        self.found = None
        self.paired = False

    def on(self):
        '''Turn on'''
        super().on(self.zigbee_addr, self.end_point, 0, 0)

    def off(self):
        '''Turn off'''
        super().off(self.zigbee_addr, self.end_point, 0, 0)

    def level(self, level, transtime=0):
        '''Change level'''
        super().level(self.zigbee_addr, self.end_point, 0, 0,
                      level, transtime)
