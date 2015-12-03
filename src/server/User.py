from socket import *
from threading import Thread
from sys import argv
from Queue import Queue

from session.Spectator import Spectator
from session.Admin import Admin

from cipher.RSA import RSA
from cipher.DES import DES
from cipher.Plain import Plain

from auth.RSAauth import RSAauth
from auth.Pass import Pass


class User():
    """
    Server is multi threaded. It means that the object is shared between different threads.
    """
    encryption = ""
    role = Spectator()
    nick = ""
    level = 0

    def __init__(self, sock, address):
        self.clientSock = sock
        self.address = address

    def recvMsg(self, queue):
        """
        client send message to server
        Here, we have to check its rights to know what to do from the message.
        Every message should begin with the nickname, followed by an action or
        the message to post.
        """
        sock = self.clientSock
        listening = True
        role = self.role
        while listening:
            response = sock.recv(3000)
            data = ""
            data = self.encryption.decipher(response)
            data = data.split(" ")
            print data

            if len(data) == 1:
                print data
                # not concerned here by these packets
                continue

            elif data[1] == "/identify" and len(data) == 3:
                response = ""
                authentication = ""
                print "Identification"
                if "RSA" in data:
                    authentication = RSAauth()
                else:
                    authentication = Pass()
                print authentication
                response = authentication.identify(data, self)
                print response
                # change Session class
                if self.level == 10:
                    print "coucou"
                    # change this
                    #self.liste.remove(client)
                    #client = Admin(client)
                    #self.addClient(client)

            elif data[1] == "/register" and len(data) == 3:
                result = role.register(data[0], data[2], sock)

            elif data[1] == "/nick":
                self.nick = role.changeNick(data[2])
                # verify nicks
                if self.nick == data[2]:
                    sock.send(self.encryption.encipher("newNick:" + data[2]))
                    queue.put(str(" " + data[0] + " is now known as " + data[2]).split(" "))

            elif data[1] == "/quit":
                sock.send("quit")
                listening = False

            elif data[1] == "/ban" and self.level > 5 and len(data) == 3:
                queue.put(str(" " + data[2] + " has been banned").split(" "))
                role.ban(data[2])

            elif self.level > 1:
                print "sending to all"
                queue.put(data)

            else:
                print "No right to talk"
                sock.send(self.encryption.encipher("You have no right to talk!"))

        self.close()

    def close(self):
        """
        not working yet
        """
        print "recv close"
        self.clientSock.send("OK")
        self.clientSock.close()
        #self.liste.remove(client)
        exit()
