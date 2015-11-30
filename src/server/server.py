from socket import *
import errno
from threading import Thread
from sys import argv
from session.Spectator import Spectator
from session.Admin import Admin
from Queue import Queue

from cipher.RSA import RSA
from cipher.DES import DES
from cipher.Plain import Plain

# global variables
addr = "127.0.0.1"
port = 5000
maxClients = 20

class Server():
    """
    Server is multi threaded. It means that the object is shared between different threads.
    """

    liste = []

    def __init__(self, addr, port):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind((addr, port))

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
            for element in self.liste:
                ciphertext = element.encryption.encipher(output)
                try:
                    element.clientSock.send(ciphertext)
                except IOError as err:
                    print err
                    self.liste.remove(element)

    def recvMsg(self, client, queue):
        """
        client send message to server
        Here, we have to check its rights to know what to do from the message.
        """

        sock = client.clientSock

        while True:

            response = sock.recv(3000)
            data = ""
#            try:
            data = client.encryption.decipher(response)
 #           except Exception as err:
  #              print "error:", err
   #             self.close(client)
            data = data.split(" ")
            #  print client.level

            if len(data) == 1:
                continue
            #2 and data[1] == "/comm":
            #    pass
            elif len(data) >= 2  and data[1] == "/identify":
                sock.send(client.identify(data))
                # change Session class
                if client.level == 10:
                    self.liste.remove(client)
                    client = Admin(client)
                    self.addClient(client)

            elif data[0] == "/register" and len(data) == 3:
                result = client.register(data[1], data[2])
            elif data[1] == "/nick":
                sock.send("newNick:" + data[2])
                queue.put(str(" " + data[0] + " is now known as " + data[2]).split(" "))
            elif data[1] == "/quit":
                self.close(client)
            elif data[1] == "/ban" and client.level > 5 and len(data) == 3:
                queue.put(str(" " + data[2] + " has been banned").split(" "))
                client.ban(data[2])
            elif client.level > 0:
                queue.put(data)
            else:
                sock.send("You have no right to talk!")


    def echo(self, clientSock):
        while True:
            data = clientSock.recv(200)
            print data
            clientSock.send(200)

    def accept(self):
        clientSock, address = self.sock.accept()
        return Spectator(clientSock, address)

    def listen(self, numclients):
        self.numClients = numclients
        self.sock.listen(numclients)

    def printMsg(self):
        pass

    def addClient(self, client):
        self.liste.append(client)

    def close(self, client):
        """
        not working yet
        """
        print "recv close"
        client.clientSock.send("OK\n")
        client.clientSock.close()
        self.liste.remove(client)
        exit()


if __name__ == "__main__":

    if len(argv) == 2:
        port = int(argv[1])
    elif len(argv) == 3:
        addr = argv[1]
        port = int(argv[2])

    server = Server(addr, port)
    server.listen(maxClients)
    queue = Queue()

    Thread(target=server.sendMsg, args=(queue,)).start()

    print "Waiting for clients on port", port

    # main thread waiting for clients
    while len(server.liste) <= maxClients:
        client = server.accept()
        print "New client", client.address
        method = client.clientSock.recv(20)
        # begin cipher process here
        print method
        if method == "DES":
            client.encryption = DES()
        elif method == "RSA":
            client.encryption = RSA()
        else:
            continue

        client.encryption.generateKey(client.clientSock)

        # launch new thread for messages reception
        Thread(target=server.recvMsg, args=(client, queue,)).start()

        server.addClient(client)
