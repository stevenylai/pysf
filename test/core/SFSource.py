import select

if __name__ == '__main__':
    from ...core.SFSource import SFSource
    sf = SFSource(None, '218.191.173.125:3000')
    sf.open()
    while True:
        r,w,x = select.select([sf], [], [])
        if len(r) > 0:
            packet = sf.readPacket()
            print("Packet: ", end="")
            for b in packet:
                print('{0:02X}'.format(b), end="")
            print("")
