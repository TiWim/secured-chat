from socket import *
from threading import Thread
from sys import argv
from Queue import Queue
import os.path

from cipher.RSA import RSA
from cipher.Plain import Plain
from cipher.DES import ClientDES

ADDR = "127.0.0.1"
PORT = 5000


class Client():
    nick = "guest"
    encryption = ""

    def __init__(self, ADDR, PORT):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect((ADDR, PORT))

        if os.path.isfile("config"):
            with open("config", "r") as liste:
                for elt in liste.readlines():
                    if "nick=" in elt:
                        self.nick = elt.split("nick=")[1].strip()

    def sendMsg(self, queue):
        while True:
            data = raw_input(self.nick + " > ")

            ciphertext = self.encryption.encipher(self.nick + " " + data)

            self.sock.send(ciphertext)
            if data == "/quit":
                queue.put("close")
                self.close()

    def recvMsg(self, queue):
        while True:

            if not queue.empty():
                self.close()
            data = self.encryption.decipher(self.sock.recv(3000))

            if "newNick:" in data:
                self.nick = data.split(":")[1]
            elif queue.empty():
                print "<", data

    def close(self):
        exit()


if __name__ == "__main__":
    queue = Queue()

    if len(argv) == 2:
        try:
            PORT = int(argv[1])
        except:
            pass
    if len(argv) == 3:
        ADDR = argv[1]
        PORT = int(argv[2])

    client = Client(ADDR, PORT)

    # encryption
    if "DES" in argv:
        client.sock.send("DES")
        client.encryption = ClientDES()
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
