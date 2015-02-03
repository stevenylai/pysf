'''Zigbee device'''


def get_cluster_module(cluster_id):
    '''From a cluster ID get the corresponding
    Python module which implements the cluster
    logic
    '''
    # TODO: we can probably make this more dynamic and automatic
    if cluster_id == 0x0006:
        from .zcl import on_off
        return on_off
    if cluster_id == 0x0008:
        from .zcl import level_control
        return level_control
    return None
