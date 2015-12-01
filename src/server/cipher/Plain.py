#! /usr/bin/python
import rsa
from Cipher import Cipher
import cPickle


class Plain(Cipher):

    def encipher(self, data):
        return data

    def decipher(self, data):
        return data
