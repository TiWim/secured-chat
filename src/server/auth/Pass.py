#! /usr/bin/python2.7
from Auth import Auth
import md5

class Pass(Auth):

    def identify(self, data, client):
        """
        Method to autenticate on the server
        Callable with the command:
        /identify password
        passwords are hashed with md5 algorithm
        """
        logged = False
        answer = ""
        nick = data[0]
        password = md5.new(data[2]).hexdigest()

        # we open the file to check if the person exists
        with open("logins.txt", "r") as liste:
            data = liste.readlines()
            for line in data:
                line = line.strip().split(" ")
                # if it matches, we pick-up the level.
                if line[1] == nick and line[2] == password:
                    client.level = int(line[0])
                    logged = True

        if logged:
            answer = "Login sucessfull"
        else:
            answer = "Wrong login or password"
        return answer
