import select

if __name__ == '__main__':
    from ...core.SerialSource import SerialSource
    sf = SerialSource(None, '/dev/ttyS0:9600')
    sf.open()
    while True:
        try:
            r,w,x = select.select([sf], [], [])
        except KeyboardInterrupt:
            break
        if len(r) > 0:
            packet = sf.readPacket()
            print("Packet: ", end="")
            for b in packet:
                print('{0:02X}'.format(b), end="")
            print("")
    sf.close()
