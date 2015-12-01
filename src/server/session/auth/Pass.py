#! /usr/bin/python2.7
from Auth import Auth


class Pass(Auth):

    def identify(self, data):
        logged = False
        answer = ""
        data = data.split(" ")
        nick = data[0]
        password = data[2]

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
