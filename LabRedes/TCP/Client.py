from socket import *
import threading

serverName = 'localhost'

serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)

#Thread para o cliente ouvir as respostas do Servidor
def listen():
    while(True):
        try:
            response = clientSocket.recv(1024).decode()

            print (response)

        except  ():
            if not threading.main_thread().is_alive(): break
        
#Thread para enviar respostas para o servidor         
def sendToServer():
    while(True):
        command = input()
        
        if(command.upper().strip()  == "PMF"):
            filePath = input("Insert file path:")
            with open(filePath, 'rb') as file:
                content = file.read()
               
            message = '<file> \n' + content.decode() 
            clientSocket.send(message.encode())
        
        elif(command.upper().strip()  == "END"):
            clientSocket.send(command.encode())
            clientSocket.close()
    
        else:
            clientSocket.send(command.encode())

#Conexão com o servidor e iicialização das Threads
def run():
    print("Starting Client...")
    clientSocket.connect((serverName,serverPort))
    print(F"Connected with server: {serverName}")
    threading.Thread(target=listen).start()
    threading.Thread(target=sendToServer).start()

run()    