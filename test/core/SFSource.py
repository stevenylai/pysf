import select

if __name__ == '__main__':
    from ...core.SFSource import SFSource
    sf = SFSource(None, '192.168.1.29:3000')
    sf.open(b'409927db24ef4da8adcd0ec22d75e7f4')
    while True:
        r,w,x = select.select([sf], [], [])
        if len(r) > 0:
            packet = sf.readPacket()
            print("Packet: ", end="")
            for b in packet:
                print('{0:02X}'.format(b), end="")
            print("")
