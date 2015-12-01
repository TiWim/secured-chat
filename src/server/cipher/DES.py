#! /usr/bin/python
from pyDes import *
from Cipher import Cipher


class DH(Cipher):

    def encipher(self, data):
        return self.privkey.encrypt(data)

    def decipher(self, data):
        answer = ""
        try:
            answer = self.privkey.decrypt(data)
        except:
            print "Unexpected error"
        return answer

    def generateKey(self, sock):
        """
        Diffie-Hellman algorithm
        we send g and p to the client and we compute X
        g and p are public parameters
        At the end, we compute K = Y^x = X^y.
        K 8 first bytes will be used for DES encryption
        """
        g, p = 11111111111111111111111111, 22222222222222222222222
        x = 1012

        sock.send(str(g) + " " + str(p))
        Y = int(sock.recv(1024))
        X = str(g ** x % p)
        sock.send(X + "\n")
        key = Y ** x % p

        self.privkey = des(str(key)[:8], CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)


class ClientDH(DH):

    def generateKey(self, sock):
        """
        Diffie-Hellman algorithm
        we receive g and p from the server and we compute Y

        At the end, we compute K = Y^x = X^y.
        K 8 first bytes will be used for DES encryption
        """
        y = 124
        data = sock.recv(1024).split(" ")
        g = int(data[0])
        p = int(data[1])
        Y = (g ** y) % p
        sock.send(str(Y) + "\n")

        X = sock.recv(1024)
        key = int(X) ** y % p

        self.privkey = des(str(key)[:8], CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
