'''Basic light control module'''
import time
import importlib
from ..control import base, device_selected


class Control(base.Control):
    '''Control class for zigbee lights'''
    parent_pkg_name = __name__.split('.', 1)[0] + '.device.zigbee.zcl'
    LEVEL_STEP = 10  # Amount of level changes per second

    def cluster_module_from_name(self, cluster):
        '''Get cluster module from its name (e.g. on_off)
        '''
        try:
            return importlib.import_module(
                '.' + cluster, self.parent_pkg_name
            )
        except ImportError:
            return None

    @property
    def current_addr(self):
        '''Get current device address'''
        from ....protocol.zigbee import Address
        addr = Address()
        addr.short_addr = self.current_device['addr']
        addr.mode = addr.ADDR_16BIT
        addr.end_point = self.device.end_point
        addr.pan_id = 0
        return addr

    @device_selected
    def bind(self, cluster):
        '''Bind'''
        cluster_pkg = self.cluster_module_from_name(cluster)
        print("Cluster to bind:", cluster, cluster_pkg)
        if cluster_pkg is None:
            return
        from ....protocol.zigbee import bind
        self.device.do_bind(
            bind.Packet.TYPE_BIND_BIND,
            self.current_device['mac'],
            self.current_device['addr'],
            self.device.end_point, cluster_pkg.CLUSTER_ID
        )

    @device_selected
    def read(self, cluster):
        '''Read'''
        from ....protocol.zigbee.zcl import read
        from ....protocol.zigbee import command
        cluster_pkg = self.cluster_module_from_name(cluster)
        if cluster_pkg is None:
            return
        attr_id_list = [
            attr['id'] for attr in cluster_pkg.ATTRIBUTES.values()
        ]
        reader = read.Read(attr_id_list)
        self.device.zcl_read_attribute(
            [reader], self.current_addr, self.device.end_point,
            cluster_pkg.CLUSTER_ID,
            command.Packet.ZCL_FRAME_CLIENT_SERVER_DIR, 0, 0, 1
        )

    @device_selected
    def on(self):
        '''Turn on'''
        self.device.on(self.current_addr, self.device.end_point, 1, 0)

    @device_selected
    def off(self):
        '''Turn off'''
        self.device.off(self.current_addr, self.device.end_point, 1, 0)

    @device_selected
    def level(self, level, transtime=0):
        '''Change level'''
        self.device.move_to_level(self.current_addr, self.device.end_point,
                                  0, 0,
                                  level, transtime)

    @device_selected
    def lvu(self):
        '''Turn the brightness up'''
        if self.device.current_level < 255:
            delta = (255 - self.device.current_level) / self.LEVEL_STEP
            self.device.initial_level = self.device.current_level
            self.device.move_start_at = time.time()
            self.device.move_level_upward = True
            self.level(255, int(delta))

    @device_selected
    def lvd(self):
        '''Turn the brightness down'''
        if self.device.current_level > 0:
            delta = self.device.current_level / self.LEVEL_STEP
            self.device.initial_level = self.device.current_level
            self.device.move_start_at = time.time()
            self.device.move_level_upward = False
            self.level(0, int(delta))

    @device_selected
    def lvs(self):
        '''Stop brightness changes'''
        if self.device.move_start_at is not None:
            stopped = time.time()
            elapsed = stopped - self.device.move_start_at
            delta = elapsed * self.LEVEL_STEP
            if self.device.move_level_upward:
                if self.device.initial_level + delta < 255:
                    final_level = int(self.device.initial_level + delta)
                else:
                    final_level = 255
            else:
                if self.device.initial_level - delta > 0:
                    final_level = int(self.device.initial_level - delta)
                else:
                    final_level = 0
            self.level(final_level)
            self.device.move_start_at = None
