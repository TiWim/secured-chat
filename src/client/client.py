#! /usr/bin/python2.7
from socket import *
from threading import Thread
from sys import argv
from Queue import Queue
import os.path
import cPickle
import rsa

from cipher.RSA import RSA
from cipher.Plain import Plain
from cipher.DES import ClientDES

ADDR = "127.0.0.1"
PORT = 5000


class Client():
    nick = "guest"
    encryption = ""
    key = ""
    rsaChall = Queue()

    def __init__(self, ADDR, PORT):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect((ADDR, PORT))

        if os.path.isfile("config"):
            with open("config", "r") as liste:
                for elt in liste.readlines():
                    if "nick=" in elt:
                        self.nick = elt.split("nick=")[1].strip()
                    if "authkey=" in elt:
                        self.key = elt.split("authkey=")[1].strip()

    def sendMsg(self, queue):
        while True:
            user_input = raw_input(self.nick + " > ")
            data = self.nick + " " + user_input
            ciphertext = self.encryption.encipher(data)
            parsed = data.split(" ")
            # this method is used only if the client wants to auth with his
            # RSA key
            if "/identify" in data and "RSA" in data:
                self.identify(data, ciphertext)
                continue
            elif "/register" in data and len(parsed) == 3:
                self.sock.send(ciphertext)
                self.generateAuthKey(data)
                continue
            self.sock.send(ciphertext)
            if user_input == "/quit":
                queue.put("close")
                self.close()

    def recvMsg(self, queue):
        while True:

            if not queue.empty():
                self.close()
            data = self.sock.recv(3000)
            if "RSA" in data:
                self.rsaChall.put(data)
                continue
            elif "quit" in data:
                continue
            else:
                data = self.encryption.decipher(data)
            # print "DEBUG", data
            if "newNick:" in data:
                # print "DEBUG", data
                self.nick = data.split(":")[1]
            elif queue.empty():
                print data

    def identify(self, data, ciphertext):
        """
        identification method with RSA key
        client has to give:
        1) his nick
        2) "/identify"
        3) the method [RSA]

        When this method is called, the server send a little challenge
        encrypted with the publickey . The client has to give the answer.
        Ends with "you are authenticated"
        """
        key = ""

        keypath = self.nick + "_private.pem"
        if os.path.isfile(keypath):
            with open(keypath, 'r') as key_file:
                key = cPickle.loads(key_file.read())

            # send the auth request
            self.sock.send(ciphertext)
            # wait for the challenge (it is possible that there is a need of queue here)
            challenge = self.rsaChall.get(True).split("RSA ")[1]
            plain = rsa.decrypt(challenge, key)
            print plain
            self.sock.send(plain)

        else:
            print "Wrong key path"


    def close(self):
        exit()

    def generateAuthKey(self, data):
        keypass = self.nick + "_private.pem"
        # 2048 bits key generation is very long (4s)

        print "generating a 2048 bits key"
        (pubkey, privkey) = rsa.newkeys(2048, poolsize=8)
        print "key generated"

        # we serialize the key to send it
        to_send = cPickle.dumps(pubkey, -1)
        self.sock.send(to_send)

        # we serialize the key for the storage because it is an object.
        serialize = cPickle.dumps(privkey, -1)
        with open(keypass, 'w') as fichier:
            fichier.write(serialize)
        with open("config", "a") as liste:
            liste.write("authkey=" + keypass + "\n")


if __name__ == "__main__":
    queue = Queue()
#    parser = optparse.OptionParser()
#    parser.add_option('-p', dest=PORT, help='modulus', type='int')
#    parser.add_option('-a', dest=ADDR, help='public exponent', type='int')
    if len(argv) == 2:
        try:
            PORT = int(argv[1])
        except:
            pass
    if len(argv) == 3:
        try:
#            ADDR = argv[1]
            PORT = int(argv[1])
        except:
            pass

    client = Client(ADDR, PORT)

    # encryption
    if "DES" in argv:
        client.sock.send("DES")
        client.encryption = ClientDES()
    elif "PLAIN" in argv:
        client.sock.send("PLAIN")
        client.encryption = Plain()
    else:
        client.sock.send("RSA")
        client.encryption = RSA()

    client.encryption.generateKey(client.sock)

    # start Threads for listening and receiving messages
    Thread(target=client.sendMsg, args=(queue,)).start()

    # creating a second thread for this task is not necessary
    client.recvMsg(queue)

    client.sock.shutdown()
    client.sock.close()
    print "closing client"
