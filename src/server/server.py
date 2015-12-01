from socket import *
from threading import Thread
from sys import argv
from Queue import Queue

from session.Spectator import Spectator
from session.Admin import Admin

from cipher.RSA import RSA
from cipher.DES import DES
from cipher.Plain import Plain

# global variables
ADDR = "127.0.0.1"
PORT = 5000
MAX_CLIENTS = 20


class Server():
    """
    Server is multi threaded. It means that the object is shared between different threads.
    """
    liste = []

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
        listening = True

        while listening:
            response = sock.recv(3000)
            data = ""
            data = client.encryption.decipher(response)
            data = data.split(" ")

            if len(data) == 1:
                # not concerned here by these packets
                continue

            elif len(data) >= 2 and data[1] == "/identify":
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
                listening = False

            elif data[1] == "/ban" and client.level > 5 and len(data) == 3:
                queue.put(str(" " + data[2] + " has been banned").split(" "))
                client.ban(data[2])

            elif client.level > 3:
                queue.put(data)

            else:
                sock.send("You have no right to talk!")

        self.close(client)

    def accept(self):
        clientSock, ADDRess = self.sock.accept()
        return Spectator(clientSock, ADDRess)

    def listen(self, numclients):
        self.numClients = numclients
        self.sock.listen(numclients)

    def addClient(self, client):
        self.liste.append(client)

    def close(self, client):
        """
        not working yet
        """
        print "recv close"
        client.clientSock.send("OK")
        client.clientSock.close()
        self.liste.remove(client)
        exit()


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
    while len(server.liste) <= MAX_CLIENTS:
        client = server.accept()
        print "New client", client.ADDRess
        method = client.clientSock.recv(20)

        # begin cipher process here
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
