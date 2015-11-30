#! /usr/bin/python
import rsa
from Cipher import Cipher
import cPickle

class Plain(Cipher):

    ownprivkey = ""
    ownpubkey = ""

    def __init__(self):
        pass

    def encipher(self, data):
        return data

    def decipher(self, data):
        return data

    def generateKey(self, sock):
        pass
