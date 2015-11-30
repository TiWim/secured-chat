#! /usr/bin/python2.7

import md5
from auth.RSA import RSA
from auth.Pass import Pass


class Role:
    nick = ""
    encryption = ""
    lastActivity = ""
    logged = False

    def __init__(self, socket, address):
        self.level = 1
        self.clientSock = socket
        self.address = address

    def identify(self, data):
        """
        Method to autenticate on the server
        Callable with the command:
        /identify password
        passwords are hashed with md5 algorithm
        """
        logged = False
        answer = ""
        password = md5.new(password).hexdigest()

        # we open the file to check if the person exists
        with open("logins.txt", "r") as liste:
            data = liste.readlines()
            for line in data:
                line = line.strip().split(" ")
                # if it matches, we pick-up the level.
                if line[1] == nick and line[2] == password:
                    self.level = int(line[0])
                    logged = True

        if logged:
            answer = "Login sucessfull"
        else:
            answer = "Wrong login or password"
        return answer

    def changeNick(self, newnick):
        """
        Method to change your nick.
        We have to check if the nick is not already used
        """
        self.nick = newnick

    def help(self):
        pass
