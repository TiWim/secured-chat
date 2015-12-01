#! /usr/bin/python2.7

import md5
from string import ascii_letters
from Role import Role


class Spectator(Role):

    def __init__(self, clientSock, address):
        self.clientSock = clientSock
        self.address = address
        self.level = 1

    def register(self, login, password):
        """
        create a new account
        and store the login, the password and the role in the database
        We have to check if the login exists.
        """

        create = True
        answer = ""

        # If login has a valid form
        if all(c in ascii_letters+'_-0123456789' for c in login):

            # we read the database
            with open("logins.txt", "a+") as liste:
                data = liste.readlines()

                # and we check that the login is not already used
                for line in data:
                    line = line.split(" ")
                    if line[1] == login:
                        create = False

                # if it is not used, we can create the user
                if create:
                    password = md5.new(password).hexdigest()
                    liste.write("3 " + login + " " + password + "\n")

        if create:
            answer = "Registration successfull"
        else:
            answer = "Registration failed, please choose an other login"

        return answer
