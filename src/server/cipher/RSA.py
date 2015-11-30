#! /usr/bin/python
import rsa
from Cipher import Cipher
import cPickle

class RSA(Cipher):

    ownpubkey = ""

    def __init__(self):
        pass

    def encipher(self, data):
        return rsa.encrypt(data, self.pubkey)

    def decipher(self, data):
        answer = ""
        try:        # print "data", data
            answer = rsa.decrypt(data, self.privkey)
        except:
            print "Exception in RSA.decipher()!"
        return answer

    def generateKey(self, sock):
        # bash wrapper?
        # 2048 bits key generation is very long (4s)
        print "generating a 2048 bits key"
        (self.ownpubkey, self.privkey) = rsa.newkeys(2048, poolsize=8)
        print "key generated"
        to_send=cPickle.dumps(self.ownpubkey, -1)
        sock.send(to_send)
        self.pubkey = cPickle.loads(sock.recv(3000))
        print "Ending key exchange"
