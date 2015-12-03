#! /usr/bin/python
import rsa
from Cipher import Cipher
import cPickle


class RSA(Cipher):

    ownpubkey = ""
    clientPubkey = ""
    ownprivkey = ""

    def encipher(self, data):
        print "encypher", self.clientPubkey
        return rsa.encrypt(data, self.clientPubkey)

    def decipher(self, data):
#        answer = ""
        print "decipher", self.ownprivkey
#        try:        # print "data", data
        answer = rsa.decrypt(data, self.ownprivkey)

#        except:
#        print "Exception in RSA.decipher()!"
        return answer

    def generateKey(self, sock):
        """
        We generate here keys for encryption.
        bash wrapper? // not a good idea, because we have to transform keys.
        2048 bits key generation can be very long (4s)
        """
        print "generating a 2048 bits key"
        (self.ownpubkey, self.ownprivkey) = rsa.newkeys(2048, poolsize=8)
        print "key generated"
        print self.ownpubkey, self.ownprivkey
        # we serialize the key to be able to send it. (str is not good because
        # we can't parse it at end point)
        to_send = cPickle.dumps(self.ownpubkey, -1)
        sock.send(to_send)

        self.clientPubkey = cPickle.loads(sock.recv(3000))
        print "Ending key exchange"
