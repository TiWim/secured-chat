#! /usr/bin/python2.7


class Role:
    nick = ""
    lastActivity = ""
    logged = False

    def __init__(self):
        self.level = 1

    def changeNick(self, newnick):
        """
        Method to change your nick.
        We have to check if the nick is not already used
        """
        self.nick = newnick
        return newnick

    def help(self):
        pass
