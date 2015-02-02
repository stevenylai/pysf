'''Basic light control module'''
import importlib
from ..control import base, device_selected


class Control(base.Control):
    '''Control class for zigbee lights'''
    parent_pkg_name = __name__.split('.', 1)[0] + '.device.zigbee.zcl'

    def cluster_module_from_name(self, cluster):
        '''Get cluster module from its name (e.g. on_off)
        '''
        try:
            return importlib.import_module(
                '.' + cluster, self.parent_pkg_name
            )
        except ImportError as exc:
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
