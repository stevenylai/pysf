'''RFM device packet'''


def addr_match(addr1, addr2):
    '''Test if the two RFM addr matches'''
    from ...protocol import rfm
    if addr1 == rfm.Payload.ADDR_RFM_BCAST \
       or addr2 == rfm.Payload.ADDR_RFM_BCAST:
        return True
    else:
        return addr1 == addr2
