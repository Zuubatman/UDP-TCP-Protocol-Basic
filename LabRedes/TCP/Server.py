from socket import *
import threading
import time

clients = []

serverPort = 12000

serverSocket = socket(AF_INET,SOCK_STREAM)

serverSocket.bind(('',serverPort))

serverSocket.listen(1)


def registerUser(username, clientSocket):
    for c in clients: 
        if c['username'] == username:  
            return False 
            
    clients.append({'username': username, 'clientSocket': clientSocket})
    return True
    
def broadCast(message, user_name):
    for c in clients:  
        if c['username'] != user_name:
            message2 = "Broadcast from: <" + user_name + ">: " + message
            c['clientSocket'].send(message2.encode())
            
def privateMessage(userDestination, user_name, message):
    for c in clients:  
        if c['username'] == userDestination:
            message = "<" + user_name + ">: " + message
            c['clientSocket'].send(message.encode())
            
def client(clientSocket, addr):
    user_name = None
    while(True):
        try:
            clientSocket.send('Insert a command:'.encode())
            command = clientSocket.recv(1024).decode()

            if(command.upper().strip() == 'END'):
                print(F"Closing connection with {clientSocket.getsockname()}")
                clientSocket.close()
                break
     
            elif(command.upper().strip() == "REG"):
                clientSocket.send('Insert username:'.encode())
                username = clientSocket.recv(1024).decode()
                register_status = registerUser(username, clientSocket)
                
                if(register_status):
                    user_name = username
                    clientSocket.send('Register Successful:'.encode())
                else:
                    clientSocket.send('Username Already Registered'.encode())
                
            elif(command.upper().strip()  == "ALL"):
                clientSocket.send('Insert message:'.encode())
                message = clientSocket.recv(1024).decode()
                broadCast(message, user_name)
                clientSocket.send('Message Sent'.encode())
                
            elif(command.upper().strip()  == "PM"):
                clientSocket.send('Insert user:'.encode())
                userDestination = clientSocket.recv(1024).decode()
                clientSocket.send('Insert Message:'.encode())
                message = clientSocket.recv(1024).decode()
                privateMessage(userDestination, user_name, message)
                
                
        except  (e):
            if not threading.main_thread().is_alive(): break    


def listen():
    print("Server is Listening...")
    while (True):

        try:
            clientSocket, addr = serverSocket.accept()
            print(F"Listening socket: {clientSocket.getsockname()}")
            threading.Thread(target=client, args=(clientSocket, addr)).start()

        except  (e):
            if not threading.main_thread().is_alive(): break


def run () :
    print("Starting Server...")
    threading.Thread(target=listen(), args=(1,)).start()


run()








