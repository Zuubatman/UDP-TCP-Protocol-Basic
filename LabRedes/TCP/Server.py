from socket import *
import threading

clients = []

serverPort = 12000

serverSocket = socket(AF_INET,SOCK_STREAM)

serverSocket.bind(('',serverPort))

serverSocket.listen(1)

#Função que trata o registro de usuários  
def registerUser(username, clientSocket):
    for c in clients: 
        if c['username'] == username:  
            return False 
            
    clients.append({'username': username, 'clientSocket': clientSocket})
    return True

#Função que trata o envio de broadcasts     
def broadCast(message, user_name):
    for c in clients:  
        if c['username'] != user_name:
            message2 = "Broadcast from <" + user_name + ">: " + message
            c['clientSocket'].send(message2.encode())
            

#Função que trata o envio de mensagens privadas 
def privateMessage(userDestination, user_name, message):
    for c in clients:  
        if c['username'] == userDestination:
            message = "<" + user_name + ">: " + message
            c['clientSocket'].send(message.encode())

#Função que trata o envio de arquivos            
def sendFilePrivate(user_name, userDestination, fileContent):
    for c in clients:
        if c['username'] == userDestination:
            message = "<" + user_name + "> Enviou um arquivo: \n" + fileContent + " \n<file>"
            c['clientSocket'].send(message.encode())

#Thread de interação com o cliente             
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

            elif(command.upper().strip() == 'HELP'):
                clientSocket.send('Commands available: \nREG - Register user\nALL - Broadcast Message\nPM - Private message\nPMF - Private message with file'.encode())
     
            elif(command.upper().strip() == "REG"):
                clientSocket.send('Insert username:'.encode())
                username = clientSocket.recv(1024).decode()
                register_status = registerUser(username, clientSocket)
                
                if(register_status):
                    user_name = username
                    clientSocket.send('Register Successful!'.encode())
                else:
                    clientSocket.send('Username Already Registered'.encode())
                
            elif(command.upper().strip()  == "ALL"):
                clientSocket.send('Insert message:'.encode())
                message = clientSocket.recv(1024).decode()
                broadCast(message, user_name)
                clientSocket.send('Message Sent!'.encode())
                
            elif(command.upper().strip()  == "PM"):
                clientSocket.send('Insert user destination:'.encode())
                userDestination = clientSocket.recv(1024).decode()
                clientSocket.send('Insert Message:'.encode())
                message = clientSocket.recv(1024).decode()
                privateMessage(userDestination, user_name, message)
                clientSocket.send('Message Sent!'.encode())
                
            elif( "<file>" in command):
                clientSocket.send('File received!'.encode())
                clientSocket.send('Insert user destination:'.encode())
                userDestination = clientSocket.recv(1024).decode()
                sendFilePrivate(user_name, userDestination, command)
                clientSocket.send('File Sent!'.encode())
                
                
        except  (e):
            if not threading.main_thread().is_alive(): break    

#Thread para ouvir os clientes
def listen():
    print("Server is Listening...")
    while (True):
        try:
            clientSocket, addr = serverSocket.accept()
            print(F"Listening socket: {clientSocket.getsockname()}")
            #Servidor inicia uma thread para se comunicar com cada cliente que estabelece uma nova conexão
            threading.Thread(target=client, args=(clientSocket, addr)).start()

        except  (e):
            if not threading.main_thread().is_alive(): break


def run () :
    print("Starting Server...")
    threading.Thread(target=listen()).start()


run()








