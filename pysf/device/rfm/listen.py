'''Listen to RFM packets'''
from .. import listen

if __name__ == '__main__':
    from . import base
    listener = listen.Listener(base.Device)
    listener.listen()
