## Description

Un serveur et plusieurs client. Le serveur tient le role de salon de chat.
Les clients se connectent au serveur  et  établissent échange de clefs selon le protocole spécifié par le client. (Diffie Hellman ou RSA)
La clef publique sera détenue par le client, la clef privée par le serveur.

## #### role, single access point, session, proxy, strategie


###### TODO
refaire l'authentification. Seulement par mot de passe pour l'instant. Interfacable

###### Store passwords and logins in a database on server side

####### Client: two threads Main and Send. main forks and makes reception.



## Role implementation:
Roles are used on server side only.

The client can try to tipe text but relying on his role /session, his messages will be printed or not.

Each client that connects to the server will have a session attached to him on server side.

## RFC:
Server is listening on his port.

Client connects.

Chiffrement des communications -> Inutile
chiffrement lors de l'échange de mots de passes?

