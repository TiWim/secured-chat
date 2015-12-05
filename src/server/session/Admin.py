#! /usr/bin/python2.7

import os.path
from Role import Role


class Admin(Role):

    def __init__(self, client):
        self.level = 10
        self.clientSock = client.clientSock
        self.address = client.address
        self.nick = client.nick
        self.encryption = client.encryption

    def setOp(self, nick, userlist):
        """
        set the user <nick> the op rights ( 8 )
        the op user has then the rights of a room op excluding the right to ban or
        to kick the main op
        """
        print "Opnick not implemented"

    def kick(self, nick, userlist):
        print "kicking", nick
        print "Kick not implemented"

    def ban(self, userlist, nick="", ip=""):
        """
        Blacklist the nick or the ip
        store all in a file "ban_list"
        """
        print "Ban not implemented"

    def unban(self, nick="", ip=""):
        """
        Unban by nick or ip and suppress the entry
        """
        print "Unban not implemented"

    def banlist(self):
        """
        list all banned ips or names
        """
        if os.path.isfile("ban_list"):
            with open("ban_list", "r") as liste:
                return ''.join(liste.readlines())
        # call with : print a.banlist().strip()
