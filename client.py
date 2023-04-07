import json
import socket
import threading
import sys
from module.Client import Client


# liste de pseudo : dès qu'un pseudo est entrer sauvegarder puis regarder si celui entrer est déjà dedans
IP = 'localhost'  # Adresse IP du serveur
PORT = 8081  # Port d'écoute du serveur

# Instance de la classe CLient
client_instance = Client(socket)
client = client_instance.socket
# Connexion au serveur
client_instance.connection( (IP, PORT))
# pseudo déjà existant
messagePseudo = json.loads(client.recv(1024).decode('utf-8'))
p = None


# Création de deux threads pour gérer la réception et l'envoi des messages
receive_thread = threading.Thread(target=client_instance.receive, args=[sys])
receive_thread.start()

send_thread = threading.Thread(target=client_instance.send, args=(messagePseudo,p, sys))
send_thread.start()

