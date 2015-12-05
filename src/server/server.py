#! /usr/bin/python2.7
from socket import *
from threading import Thread
from sys import argv
from Queue import Queue

from User import User

from cipher.RSA import RSA
from cipher.DES import DES
from cipher.Plain import Plain

# global variables
ADDR = "127.0.0.1"
PORT = 5000
MAX_CLIENTS = 20


class Server():
    """
    Server is multi threaded. It means that the object is shared between
    different threads.
    """
    userList = []

    def __init__(self, ADDR, PORT):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind((ADDR, PORT))

    def sendMsg(self, queue):
        """
        server send message to all
        """
        while True:
            # We wait until someone send a message
            # the queue is blocking

            data = queue.get(True)
            output = "\r" + data[0] + " |"
            data.remove(data[0])
            for elt in data:
                output += " " + elt
            for element in self.userList:
                ciphertext = element.encryption.encipher(output)
                try:
                    element.clientSock.send(ciphertext)
                except IOError as err:
                    print err
                    self.userList.remove(element)

    def accept(self):
        clientSock, address = self.sock.accept()
        return User(clientSock, address)

    def listen(self, numclients):
        self.numClients = numclients
        self.sock.listen(numclients)

    def addClient(self, client):
        self.userList.append(client)


if __name__ == "__main__":

    if len(argv) == 2:
        PORT = int(argv[1])
    elif len(argv) == 3:
        ADDR = argv[1]
        PORT = int(argv[2])

    server = Server(ADDR, PORT)
    server.listen(MAX_CLIENTS)
    queue = Queue()

    Thread(target=server.sendMsg, args=(queue,)).start()

    print "Waiting for clients on port", PORT

    # main thread waiting for clients
    while len(server.userList) <= MAX_CLIENTS:
        client = server.accept()
        print "New client", client.address

        # begin cipher process here
        method = client.clientSock.recv(20)
        if method == "DES":
            client.encryption = DES()
        elif method == "PLAIN":
            client.encryption = Plain()
        elif method == "RSA":
            client.encryption = RSA()
        else:
            continue

        client.encryption.generateKey(client.clientSock)

        # launch new thread for messages reception
        Thread(target=client.recvMsg, args=(server.userList, queue,)).start()

        server.addClient(client)
