'''Zigbee light command line control'''
import asyncio
from ..control import console
from . import control


class Control(control.Control, console.Control):
    '''Console control class'''
    pass

if __name__ == '__main__':
    from . import Device
    controller = Control(Device)
    controller.create_device()
    controller.device.open()
    if not controller.console_on_thread:
        controller.event_loop.run_until_complete(
            controller.process_packets()
        )
    else:
        controller.event_loop.run_until_complete(
            asyncio.wait(
                [
                    controller.process_packets(),
                    controller.event_loop.run_in_executor(
                        None, controller.read_input_thread
                    )
                ]
            )
        )
