import signal
import sys
from datetime import datetime


class Serveur:
    def __init__(self, socket):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []  # Liste des clients connectés
        self.pseudos = []  # Liste des pseudos
        self.pseudo = None
        self.not_stop = True

    def liaison(self, addr):
        self.socket.bind(addr)
        self.socket.listen()

    def log(self, message, datetime):
        with open('chat-connexion.txt', 'a') as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

    def send_to_clients(self, message, sender, pseudo):
        """
        Envoie un message à tous les clients connectés
        """
        for client in self.clients:
            if sender == "connexion":
                client.send(message.encode())
            elif client == sender:
                msg_sender = f"Moi : {message}"
                client.send(msg_sender.encode())
            else:
                msg = f"{pseudo} : {message}"
                client.send(msg.encode())
        if sender != "connexion":
            print(f"{pseudo} : {message}")

    def handle_client(self, client, pseudo, address, Thread):
        """
        gère l'envoi de message au client connecté et la déconnaxion
        """
        while self.not_stop:
            try:
                message = client.recv(1024).decode()  # Réception du message
                if message != "":
                    # si c'est le pseudo
                    if message.split(':')[0] == 'pseudo':
                        pseudo = message.split(':')[1]
                        self.pseudos.append(pseudo)
                        self.send_to_clients(f"{pseudo} s'est connectée", "connexion",
                                             pseudo="")  # Envoi du message aux autres clients
                        self.log(f"Le client {pseudo} s'est connecté.", datetime)  # écrit dans le fichier la connexion
                    elif message.lower() == "exit":
                        self.remove(client, pseudo, address)
                        break
                    else:
                        self.send_to_clients(message, client, pseudo)  # Envoi du message aux autres clients
                else:
                    self.remove(client, pseudo, address)
                    break

            except:
                self.shutdown()
                break

    def remove(self, client, pseudo, address):
        """
        Supprime un client de la liste des clients connectés.
        """
        client.close()  # ferme la connexion
        if client in self.clients:
            self.clients.remove(client)  # l'enlève de la liste
        self.send_to_clients(f"{pseudo} s'est déconnectée", "connexion",
                             pseudo="")  # envoi à tous les clients
        self.log(f"Le client {pseudo} s'est déconnecté.", datetime)  # écrit dans le fichier la déconnexion
        print(f"Le client {address[0]} s'est déconnectée")
        return

    def shutdown(self):
        clients_copy = list(self.clients)
        for client in clients_copy:
            try:
                self.send_to_clients("Le serveur est en train de se fermer.\n", "connexion", pseudo=None)
                client.close()
            except:
                pass
        print("Le serveur est en train de se fermer...")
        self.socket.close()
        self.not_stop = False
        return
