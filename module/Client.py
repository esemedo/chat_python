import socket
import sys


class Client:
    def __init__(self, socket):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket client
        self.not_stop = True

    def connection(self, addrr):
        self.socket.connect(addrr)

    def comparison(self, p, pseudos_tab):
        """
            Regarde si le pseudo entré existe déjà
        """
        if len(pseudos_tab) != 0:
            for pseudo in pseudos_tab:
                if pseudo == p:
                    return True
        return False

    def send(self, messagePseudo, p):
        """
        Envoi des messages au serveur.
        """
        while self.not_stop:
            try:
                if p is None:
                    message = input("Entrez un pseudo : ")
                    if len(message) < 20 and message != "":
                        if not self.comparison(message, messagePseudo):
                            p = f"pseudo:{message}"
                            self.socket.send(p.encode('utf-8'))
                        else:
                            print("Le pseudo existe déjà")
                    else:
                        print("Le pseudo ne doit ni être vide ni excéder 20 caractères")
                else:
                    message = input("")
                    if message != "":
                        if message.upper() == 'EXIT':  # Si l'utilisateur entre "EXIT", déconnexion du client
                            self.not_stop = False
                            self.socket.close()
                            break
                        self.socket.send(message.encode('utf-8'))
            except (BrokenPipeError, KeyboardInterrupt, ConnectionResetError, OSError, ConnectionAbortedError):
                print("La connexion a été interrompue de manière inattendue.")
                self.not_stop = False
                self.socket.close()
                break

    def receive(self):
        """
        Réception des messages du serveur.
        """
        while self.not_stop:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                print(message)
                if message == "Le serveur est en train de se fermer.\n":
                    self.socket.close()
                    self.not_stop = False
                    break
            except (BrokenPipeError, KeyboardInterrupt, ConnectionResetError, OSError, ConnectionAbortedError):
                print("La connexion a été interrompue de manière inattendue.receive")
                self.not_stop = False
                self.socket.close()
                break
