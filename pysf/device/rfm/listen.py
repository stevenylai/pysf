'''Listen to RFM packets'''
from .. import listen

if __name__ == '__main__':
    from . import base
    listen.listen(base.Device)
