from socket import *
from threading import Thread
import sys

#---------------------------------------------------------
BUFFER_SIZE = 1024  # La dimensione massima di dati da ricevere, in byte
HOST = "localhost"
LOCAL_PORT = 8888

TARGET_HOST = "localhost"
TARGET_PORT = 8888

# Codici di stato
SUCCESS_CODE = 200
NOT_FOUND_CODE = 404
ERROR_CODE = 500
#---------------------------------------------------------

class ClientThread(Thread):
    def __init__(self, server_host, server_port):
        super().__init__()
        self.server_host = server_host
        self.server_port = server_port
        self.active = True

    def run(self):
        print("Thread CLIENT attivato\n")
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((self.server_host, self.server_port))
        client_socket.send(name.encode())
        while True:
            msg = input(name + " >> ")
            while not msg:
                msg = input(name + " >> ")
                
            if msg == ".q":
                print("Uscita dal client\n")
                client_socket.send(str(SUCCESS_CODE).encode())  # Invia un codice di successo
                break
            else:
                client_socket.send(msg.encode())
                response_code = int(client_socket.recv(BUFFER_SIZE).decode('utf-8'))
                if response_code != SUCCESS_CODE:
                    print(f"Errore durante l'invio del messaggio. Codice di stato: {response_code}")
                    break
        client_socket.close()

class ServerThread(Thread):
    def __init__(self, host, port, nome="Server"):
        super().__init__()
        self.indirizzo = (host, port)

        # Crea un oggetto socket
        # AF_INET indica che si sta utilizzando la famiglia di indirizzi IPv4 (Address Family Internet)
        # SOCK_STREAM indica che si sta utilizzando un socket di tipo stream cioè una connessione TCP
        self.server_socket = socket(AF_INET, SOCK_STREAM)

        # Associa un indirizzo (IP e numero di porta) a un socket
        self.server_socket.bind(self.indirizzo)

        # Mette in ascolto il socket e abilita la ricezione di connessioni in entrata
        self.server_socket.listen()

        self.attivo = True
        self.nome = nome

    def run(self):
        print("Server attivato\n")
        while self.attivo:
            # Attende/accetta una connessione da un client; fornisce una istanza di socket (server) e IP+porta del client
            client, indirizzo_client = self.server_socket.accept()

            # Riceve il nome dell'interlocutore
            nuovo_nome = client.recv(BUFFER_SIZE).decode("utf-8")
            self.nome = nuovo_nome

            while True:
                dati = client.recv(BUFFER_SIZE).decode(
                    "utf-8"
                )  # Converte i byte ricevuti, utilizzando la codifica UTF-8
                if not dati:
                    break
                print("\n", self.nome, " >> ", dati)
                client.send(b"OK")  # Invia una conferma al client
                sys.stdout.write(self.nome + " >> ")

            client.close()

        print("Server terminato!\n")

    def stop(self):
        self.attivo = False
        self.server_socket.close()
        print("Server disattivato!\n")
#---------------------------------------------------------
name = input("Inserisci il tuo username: ")

client_thread = ClientThread(TARGET_HOST, TARGET_PORT)
client_thread.start()

server_thread = ServerThread(HOST, LOCAL_PORT)
server_thread.start()
#---------------------------------------------------------