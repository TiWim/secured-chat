#! /usr/bin/python2.7
import os.path
from Auth import Auth
import rsa
import cPickle

FOLDER = "keys"


class RSAauth(Auth):

    def identify(self, data, client):
        """
        Method to autenticate on the server with a RSA key
        Callable with the command:
        /identify RSA
        authentify the user with his private key. We have to pick his public
        key, cipher a little challenge,
        send it to the user and compare the answer.
        """
        answer = ""
        sock = client.clientSock
        nick = data[0]
        identified = False
        logged = False
        print "begin"
        keypass = FOLDER + "/" + nick + ".pub"
        if os.path.isfile(keypass):
            with open(keypass, "r") as fichier:
                pubkey = cPickle.loads(fichier.read())
                challenge = "hello"
                encript = rsa.encrypt(challenge, pubkey)
                print "sending challenge"
                sock.send("RSA " + encript)
                print "chall sent"
                response = sock.recv(2000)
                if response == challenge:
                    print "Yeah"
                    identified = True
        else:
            print "Wrong path"

        with open("logins.txt", "r") as liste:
            data = liste.readlines()
            for line in data:
                line = line.strip().split(" ")
                if line[1] == nick and identified:
                    client.level = int(line[0])
                    logged = True

        if logged:
            answer = "Login sucessfull"
        else:
            answer = "Wrong login or password"
        return answer

    def register(self, nick, sock):
        pubkey = sock.recv(3000)
        with open(FOLDER + "/" + nick + '.pub', 'w') as key_file:
            key_file.write(pubkey)
