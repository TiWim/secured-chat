#! /usr/bin/python
import rsa
from Cipher import Cipher
import cPickle


class RSA(Cipher):

    ownpubkey = ""
    clientPubkey = ""
    ownprivkey = ""

    def encipher(self, data):
        return rsa.encrypt(data, self.clientPubkey)

    def decipher(self, data):
        return rsa.decrypt(data, self.ownprivkey)

    def generateKey(self, sock):
        """
        We generate here keys for encryption.
        bash wrapper? // not a good idea, because we have to transform keys.
        2048 bits key generation can be very long (4s)
        """
        print "generating a 2048 bits key"
        (self.ownpubkey, self.ownprivkey) = rsa.newkeys(2048, poolsize=8)
        print "key generated"

        # we serialize the key to be able to send it. (str is not good because
        # we can't parse it at end point)
        to_send = cPickle.dumps(self.ownpubkey, -1)
        sock.send(to_send)

        self.clientPubkey = cPickle.loads(sock.recv(3000))
        print "Ending key exchange"
