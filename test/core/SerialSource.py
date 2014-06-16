import time
import select

def dump_packet(packet):
    print("Packet: ", end="")
    for b in packet:
        print('{0:02X}'.format(b), end="")
    print("")

def test_read(sf):
    while True:
        try:
            r,w,x = select.select([sf], [], [])
        except KeyboardInterrupt:
            break
        if len(r) > 0:
            packet = sf.readPacket()
            dump_packet(packet)

def test_write(sf):
    counter = 0
    while True:
        packet = bytes([counter for i in range(0, 4)])
        print("Sending: ", end="")
        dump_packet(packet)
        sf.writePacket(packet)
        counter = (counter + 1) % 256
        time.sleep(1)
        
def test_echo(sf):
    counter = 0
    while True:
        packet = bytes([counter for i in range(0, 4)])
        print("Sending: ", end="")
        dump_packet(packet)
        sf.writePacket(packet)
        r,w,x = select.select([sf], [], [])
        if len(r) > 0:
            packet = sf.readPacket()
            print("Reading back: ", end="")
            dump_packet(packet)
        counter = counter + 1
        break


if __name__ == '__main__':
    from ...core.SerialSource import SerialSource
    from ...core import SerialProtocol
    SerialProtocol.DEBUG = True
    sf = SerialSource(None, '/dev/ttyS0:9600')
    sf.open()
    test_write(sf)
    sf.close()
