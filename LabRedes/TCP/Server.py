from socket import *
import threading
import time

clients = []

serverPort = 12000

serverSocket = socket(AF_INET,SOCK_STREAM)

serverSocket.bind(('',serverPort))

serverSocket.listen(1)


def registerUser(username, addr): 
    clients.append({'username': username, 'addr': addr})
    
def Client(clientSocket, addr):
    while(True):
        try:
            clientSocket.send('Insert a command:'.encode())
            command = clientSocket.recv(1024).decode()
            if(command):
                clientSocket.send('Oii'.encode())

        except  (e):
            if not threading.main_thread().is_alive(): break    


def listen():
    while (True):
        print("Listening ...")

        try:
            clientSocket, addr = serverSocket.accept()
            print(F"Listening socket: {clientSocket.getsockname()}")
            threading.Thread(target=Client, args=(clientSocket, addr)).start()
           

            # elif(command.upper() == 'LOG'): 
            #     clientSocket.send('INSERT USERNAME:'.encode())
            #     username = clientSocket.recv(1024).decode()
            #     registerUser(username, addr)
            #     print('Registrado com sucesso')

            # elif(command.upper() == 'MSG'):
            #     clientSocket.send('DIGITE A MENSAGEM:'.encode())
            #     message = clientSocket.recv(1024).decode()
            #     for client in clients:
            #         client_addr = client['addr']
            #         if(client_addr != addr):
            #             clientSocket.send(message.encode())

        except  (e):
            if not threading.main_thread().is_alive(): break


def run () :
    print("Starting Server...")
    threading.Thread(target=listen(), args=(1,)).start()


run()








