from socket import *
import threading

serverPort = 40000

serverSocket = socket(AF_INET, SOCK_DGRAM)

serverSocket.bind(('', serverPort))

serverSocket.settimeout(2)

clients = []

def registerUser(username, clientAddress):
    for c in clients: 
        if c['username'] == username:  
            return False 
            
    clients.append({'username': username, 'clientAddress': clientAddress})
    return True
    
def broadCast(message, client_address):
    senderUsername = None 
    for c1 in clients:
        if c1['clientAddress'] == client_address:
            senderUsername = c1['username']
    
    for c in clients:  
        if c['clientAddress'] != client_address:
            message2 = "Broadcast from <" + senderUsername + ">: " + message
            serverSocket.sendto(message2.encode(), c['clientAddress'])
            
def privateMessage(message, user_destination, client_address):
    senderUsername = None 
    for c1 in clients:
        if c1['clientAddress'] == client_address:
            senderUsername = c1['username']
    
    for c in clients:  
        if c['username'] == user_destination:
            message = "<" + senderUsername + ">: " + message
            serverSocket.sendto(message.encode(), c['clientAddress'])
            
def sendFilePrivate(client_address, userDestination, fileContent):
    senderUsername = None 
    for c1 in clients:
        if c1['clientAddress'] == client_address:
            senderUsername = c1['username']
            
    for c in clients:
        if c['username'] == userDestination:
            message = "<" + senderUsername + "> Enviou um arquivo: \n" + fileContent + " \n<file>"
            serverSocket.sendto(message.encode(), c['clientAddress'])
                        
def client(command, clientAddress):
    command = command.decode().rstrip()
    
    if(command.upper().strip() == 'END'):
        print("Encerrado")
        # print(F"Closing connection with {clientSocket.getsockname()}")
        # clientSocket.close()
        # 
    elif('help' in command):
        serverSocket.sendto('Commands available: \nREG [username] - Register user\nALL [message] - Broadcast message\nPM [destination] [message] - Private message\nPMF [destination] - Private message with file'.encode(), clientAddress)        
    
    elif(command.split(' ')[0] == 'reg'):
        dataArr = command.split(' ')
        data = dataArr[1]
        register_status = registerUser(data, clientAddress)
            
        if(register_status):
            serverSocket.sendto('Register Successful!'.encode(), clientAddress)
        else:
            serverSocket.sendto('Username Already Registered'.encode(), clientAddress)
                    
    elif(command.split(' ')[0] == 'all'):
            dataArr = command.split(' ')
            data = ' '.join(dataArr[1:])
            broadCast(data, clientAddress)
            serverSocket.sendto('Message Sent!'.encode(), clientAddress)
                    
    elif(command.split(' ')[0] == 'pm'):
            dataArr = command.split(' ')
            userDestination = dataArr[1]
            data = ' '.join(dataArr[2:])
            privateMessage(data, userDestination, clientAddress)
            serverSocket.sendto('Message Sent!'.encode(), clientAddress)
                    
    elif(command.split(' ')[0] == 'file'):
            serverSocket.sendto('File received!'.encode(), clientAddress)
            dataArr = command.split(' ')
            userDestination = dataArr[1]
            data = ' '.join(dataArr[2:])
            sendFilePrivate(clientAddress, userDestination, data)
                
        
def listen():
    print("Server is Listening...")
    while (True):

        try:
            command, clientAddress = serverSocket.recvfrom(2048)
            print(F"Listening Address: {clientAddress}")
            client(command, clientAddress)

        except timeout:      
            continue
        
        except  (e):
            print(e)


def run () :
    print("Starting Server...")
    threading.Thread(target=listen()).start()


run()
