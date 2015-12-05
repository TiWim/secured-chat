#! /usr/bin/python2.7

from session.Spectator import Spectator
from session.Admin import Admin

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

    def recvMsg(self, userList, queue):
        """
        client send message to server
        Here, we have to check its rights to know what to do from the message.
        Every message should begin with the nickname, followed by an action or
        the message to post.

        This is also a message dispatcher
        """
        sock = self.clientSock
        userListning = True
        role = self.role
        while userListning:
            response = sock.recv(3000)
            data = ""
            try:
                data = self.encryption.decipher(response)
            except:
                # If there is any problem, we disconnect the user
                # Normally, it happens if the user disconnected
                print "Exception in RSA.decipher()!"
                break

            print data
            data = data.split(" ")

            if len(data) == 1:
                # not concerned here by these packets
                print data
                continue

            elif data[1] == "/identify" and len(data) == 3:
                response = ""
                authentication = ""
                print "Identification"
                if "RSA" in data:
                    authentication = RSAauth()
                else:
                    authentication = Pass()

                response = authentication.identify(data, self)
                print response

                # change Session class
                if self.level == 10:
                    print "coucou"
                    # change this
                    role = Admin()

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
                userListning = False

            elif data[1] == "/ban" and self.level > 5 and len(data) == 3:
                queue.put(str(" " + data[2] + " has been banned").split(" "))
                role.ban(data[2])

            elif self.level > 1:
                print "sending to all"
                queue.put(data)

            else:
                print "No right to talk"
                sock.send(self.encryption.encipher("You have no right to talk!"))

        self.close(userList)

    def close(self, userList):
        """
        not working yet
        """
        print "recv close"
        self.clientSock.send("OK")
        self.clientSock.close()
        userList.remove(self)
        exit()
