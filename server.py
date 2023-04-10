import socket
from module.Serveur import Serveur
import json
from threading import Thread

IP = 'localhost'  # Adresse IP locale
PORT = 8080  # Port d'écoute

# Instance de la classe serveur
s = Serveur(socket)
# Liaison du serveur à l'adresse et au port spécifiés + mise en attente de la connexion
s.liaison((IP, PORT))
server = s.socket
print("Lancement du serveur...")

while s.not_stop:
    try:
        # Attente de connexions entrantes
        client, address = s.socket.accept()
        # envoi la liste des pseudos déjà utiliser
        client.send(json.dumps(s.pseudos).encode())
        print("Un client est connecté depuis", address[0])
        # Ajout du client à la liste des clients connectés
        s.clients.append(client)
        # Création d'un thread pour gérer la connexion du client
        thread = Thread(target=s.handle_client, args=(client, s.pseudo, address, Thread))
        thread.start()
    except (ConnectionAbortedError, KeyboardInterrupt):
        s.shutdown()
        break
