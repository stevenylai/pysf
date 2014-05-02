#
# Copyright (c) 2005-2006
#      The President and Fellows of Harvard College.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the University nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE UNIVERSITY AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE UNIVERSITY OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#
# Author: Geoffrey Mainland <mainland@eecs.harvard.edu>
#
import hashlib

VERSION = "U"
SUBVERSION = " "

PLATFORM_UNKNOWN = 0

class SFProtocolException(Exception):
    def __init__(self, *args):
        self.args = args

class SFProtocol:
    def __init__(self, ins, outs):
        self.ins = ins
        self.outs = outs
        self.platform = None

    def digest(self, message, key):
        hasher = hashlib.sha256()
        hasher.update(key)
        hasher.update(message)
        digest = hasher.digest()

        hasher = hashlib.sha256()
        hasher.update(digest)
        return hasher.digest()

    def auth_client(self, key):
        print("Auth client")
        challenge = b''
        item = self.ins.read(1)
        while item != b'\x00':
            challenge = challenge + item
            item = self.ins.read(1)
        print("Challenge:", challenge, "Digest:", self.digest(challenge, key))

        self.outs.write(self.digest(challenge, key))

    def open(self, key):
        self.outs.write(bytes(VERSION + SUBVERSION, 'utf-8'))
        partner = self.ins.read(2).decode('utf-8')
        if partner[0] != VERSION:
            print ("SFProtocol : version error")
            raise SFProtocolException("protocol version error")

	# Actual version is min received vs our version
        # ourversion = partner[1] & 0xff
        
        if self.platform == None:
            self.platform = PLATFORM_UNKNOWN

        self.auth_client(key)
        print("Client authed")
        # In tinyox-1.x, we then exchanged platform information

        # the tinyos-2.x serial forwarder doesn't do that, so the
        # connection is all set up at this point.


    def readPacket(self):
        size_l = self.ins.read(1)
        size_h = self.ins.read(1)
        size = ord(size_h) << 8 | ord(size_l)
        packet = self.ins.read(size)
        return packet

    def writePacket(self, packet):
        if len(packet) > 65535:
            raise SFProtocolException("packet too long")

        self.outs.write(bytes(chr(len(packet) & 0xFF), 'utf-8'))
        self.outs.write(bytes(chr(len(packet) >> 8), 'utf-8'))
        self.outs.write(packet)
        self.outs.flush()
        
