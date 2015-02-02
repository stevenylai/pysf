'''Log socket packets'''
import re
import sys
import logging
import logging.handlers
from ... import listen


class Listener(listen.Listener):
    '''Log listener'''
    def __init__(self, device_cls):
        '''Create listener'''
        from .listen import Device
        super().__init__(Device)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def create_device(self):
        super().create_device()
        formatter = logging.Formatter(
            fmt='%(asctime)s:%(levelname)s - %(message)s',
            datefmt='%m/%d/%Y %H:%M:%S'
        )
        log_filename = self.device.bindable
        match = re.compile('[^:]+').search(log_filename)
        if match is not None:
            log_filename = match.group()
        file_handler = logging.handlers.RotatingFileHandler(
            log_filename + '_' + hex(self.device.listened) + '.log',
            maxBytes=1024 * 1024 * 32, backupCount=4
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

    def emit(self, packet_string):
        '''Log packet string'''
        self.logger.info("%s", packet_string)

if __name__ == '__main__':
    from . import listen
    listener = Listener(listen.Device)
    listener.listen()
