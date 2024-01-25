from socket import *
from threading import Thread
import sys

BUFFER_SIZE = 1024
TARGET_HOST = "localhost"
TARGET_PORT = 8888

# Codici di stato
SUCCESS_CODE = 200
NOT_FOUND_CODE = 404
ERROR_CODE = 500

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

name = input("Inserisci il tuo username: ")

client_thread = ClientThread(TARGET_HOST, TARGET_PORT)
client_thread.start()
